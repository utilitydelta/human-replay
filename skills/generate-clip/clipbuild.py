#!/usr/bin/env python3
"""Build one narrated clip: synthesise, render, mux, subtitle.

    python clipbuild.py clip.py PooledConnectionDesync --preview
    python clipbuild.py clip.py PooledConnectionDesync

The audio is built first so the scene can hold each beat for as long as its
line takes to say. The scene writes back the exact second each beat started,
and this script lays the wavs at those offsets. Audio and video come out the
same length with no drift, and re-timing a beat means editing the sentence.

Voice models are cached in ~/.cache/human-replay/voices and shared by every
sandbox, because piper downloads them from the network rather than from uv.
"""

import argparse
import importlib.util
import json
import os
import subprocess
import sys
import wave

CACHE = os.path.expanduser("~/.cache/human-replay/voices")
DEFAULT_VOICE = "en_GB-alan-medium"


def sh(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode != 0:
        print(" ".join(str(c) for c in cmd))
        print(r.stdout[-2000:], r.stderr[-2000:], sep="\n")
        sys.exit(1)
    return r


def load_lines(clip_path):
    """Import the clip module for its narrate() call, without rendering."""
    spec = importlib.util.spec_from_file_location("clipmod", clip_path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["clipmod"] = mod
    spec.loader.exec_module(mod)
    import clipkit
    if not clipkit._LINES:
        sys.exit(f"{clip_path} never called narrate(). Nothing to say.")
    return dict(clipkit._LINES)


def ensure_voice(name):
    onnx = os.path.join(CACHE, f"{name}.onnx")
    if not os.path.exists(onnx):
        os.makedirs(CACHE, exist_ok=True)
        print(f"--> fetching voice {name} (once, shared by every sandbox)")
        sh([sys.executable, "-m", "piper.download_voices", name, "--download-dir", CACHE])
    return onnx


def synthesise(lines, voice_dir, onnx, rate):
    from piper import PiperVoice, SynthesisConfig
    os.makedirs(voice_dir, exist_ok=True)
    voice = PiperVoice.load(onnx)
    cfg = SynthesisConfig(length_scale=rate)
    durations = {}
    for key, text in lines.items():
        path = os.path.join(voice_dir, f"{key}.wav")
        with wave.open(path, "wb") as w:
            voice.synthesize_wav(text, w, syn_config=cfg)
        with wave.open(path) as w:
            durations[key] = w.getnframes() / w.getframerate()
    with open(os.path.join(voice_dir, "durations.json"), "w") as f:
        json.dump(durations, f, indent=2)
    total = sum(durations.values())
    print(f"--> {len(durations)} lines, {total:.1f}s of narration")
    return durations


def probe_duration(path):
    r = sh(["ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "csv=p=0", path])
    return float(r.stdout.strip())


def build_track(voice_dir, timing, video_seconds, out_path):
    import numpy as np
    rate = None
    laid = []
    for b in timing["beats"]:
        path = os.path.join(voice_dir, f"{b['key']}.wav")
        with wave.open(path) as w:
            r = w.getframerate()
            data = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)
            if w.getnchannels() == 2:
                data = data.reshape(-1, 2).mean(axis=1).astype(np.int16)
        if rate is None:
            rate = r
        elif r != rate:
            sys.exit(f"sample rate mismatch in {path}")
        laid.append((b["start"], data))

    track = np.zeros(int(video_seconds * rate) + rate, dtype=np.int32)
    for start, data in laid:
        i = int(round(start * rate))
        track[i:i + len(data)] += data.astype(np.int32)
    track = np.clip(track, -32768, 32767).astype(np.int16)[:int(video_seconds * rate)]

    with wave.open(out_path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(track.tobytes())


def write_srt(path, timing):
    def ts(sec):
        h, rem = divmod(sec, 3600)
        m, s = divmod(rem, 60)
        return f"{int(h):02}:{int(m):02}:{s:06.3f}".replace(".", ",")
    with open(path, "w") as f:
        for n, b in enumerate(timing["beats"], 1):
            f.write(f"{n}\n{ts(b['start'])} --> {ts(b['start'] + b['audio'])}\n"
                    f"{b['text']}\n\n")
    return len(timing["beats"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("clip")
    ap.add_argument("scene")
    ap.add_argument("--preview", action="store_true", help="480p15 instead of 1080p60")
    ap.add_argument("--voice", default=DEFAULT_VOICE)
    ap.add_argument("--rate", type=float, default=0.95,
                    help="piper length scale; lower is faster")
    ap.add_argument("--voice-dir", default="voice")
    args = ap.parse_args()

    lines = load_lines(args.clip)
    onnx = ensure_voice(args.voice)
    synthesise(lines, args.voice_dir, onnx, args.rate)

    quality = "-ql" if args.preview else "-qh"
    print(f"--> rendering {args.scene} ({'480p15' if args.preview else '1080p60'})")
    sh([sys.executable, "-m", "manim", quality, "--disable_caching", args.clip, args.scene])

    stem = os.path.splitext(os.path.basename(args.clip))[0]
    res = "480p15" if args.preview else "1080p60"
    silent = os.path.join("media", "videos", stem, res, f"{args.scene}.mp4")
    if not os.path.exists(silent):
        sys.exit(f"rendered file not found at {silent}")

    with open(os.path.join(args.voice_dir, f"timing_{args.scene}.json")) as f:
        timing = json.load(f)

    vdur = probe_duration(silent)
    wav = os.path.join(args.voice_dir, f"{args.scene}.wav")
    build_track(args.voice_dir, timing, vdur, wav)

    out = f"{args.scene}.mp4"
    sh(["ffmpeg", "-y", "-v", "error", "-i", silent, "-i", wav,
        "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-ar", "48000",
        "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-shortest", out])
    n = write_srt(f"{args.scene}.srt", timing)

    print(f"\ndone: {out}  ({vdur:.1f}s)")
    print(f"      {args.scene}.srt  ({n} cues)")
    last = timing["beats"][-1]
    tail = vdur - (last["start"] + last["audio"])
    if tail < -0.05:
        print(f"WARNING: narration runs {-tail:.1f}s past the end of the video")


if __name__ == "__main__":
    main()
