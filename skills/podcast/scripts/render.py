# /// script
# requires-python = ">=3.12,<3.13"
# dependencies = ["kokoro==0.9.4", "transformers>=4.45", "misaki[en]>=0.9.4", "soundfile", "numpy"]
# ///
"""Render a checked podcast script to an m4a with one chapter marker per chapter.

  uv run render.py <script.md> <out.m4a> [--engine kokoro] [--only N]

Run `podcast.py lint` first; render refuses a script that fails it. Source tags are stripped;
front matter `pronounce` (IPA, for kokoro) rewrites names inline. `--only N` renders the first N
lines, to audition voices. Needs ffmpeg on PATH.
"""
import argparse
import os
import pathlib
import re
import subprocess
import sys
import tempfile

import numpy as np
import soundfile as sf

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import podcast  # noqa: E402

RATE = 24000
# Kokoro's own full stop is about 0.3 s, so a gap of that size after every line marks nothing. Turns get a little
# more, a short reply a little less, and a {beat} or {think} a real pause. First values; set them by ear.
GAP_LINE, GAP_QUICK, GAP_CHAPTER = 0.4, 0.2, 1.2
GAP_MARK = {"beat": 1.2, "think": 2.5}
SPEED = {"slow": 0.9, "quick": 1.08}
QUICK_WORDS = 8


def gap(line):
    marked = [GAP_MARK[m] for m in line["marks"] if m in GAP_MARK]
    if marked:
        return max(marked)
    return GAP_QUICK if len(line["text"].split()) <= QUICK_WORDS else GAP_LINE


def speed(line):
    return next((SPEED[m] for m in line["marks"] if m in SPEED), 1.0)


def kokoro_voice(meta):
    from kokoro import KPipeline

    pipe = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
    voices = meta.get("voices", {"A": "af_heart", "B": "am_michael"})
    marks = {w: f"[{w}]({ipa})" for w, ipa in meta.get("pronounce", {}).items()}

    def say(speaker, text, speed=1.0):
        for word, mark in marks.items():
            text = re.sub(rf"\b{re.escape(word)}\b", mark, text)
        parts = [a for _, _, a in pipe(text, voice=voices[speaker], speed=speed)]
        return np.concatenate(parts) if parts else np.zeros(0, dtype=np.float32)

    return say


ENGINES = {"kokoro": kokoro_voice}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("script")
    ap.add_argument("out")
    ap.add_argument("--engine", default="kokoro", choices=sorted(ENGINES))
    ap.add_argument("--only", type=int)
    args = ap.parse_args()

    if podcast.lint(args.script) and not args.only:
        sys.exit("render: fix the lint problems first")
    meta, chapters, _ = podcast.parse(args.script)
    say = ENGINES[args.engine](meta)

    pieces, marks, t, done = [], [], 0.0, 0
    for ch in chapters:
        if args.only and done >= args.only:
            break
        marks.append((t, ch["title"]))
        for ln in ch["lines"]:
            if args.only and done >= args.only:
                break
            audio = say(ln["speaker"], ln["text"], speed(ln))
            pause = gap(ln)
            pieces += [audio, np.zeros(int(pause * RATE), dtype=np.float32)]
            t += len(audio) / RATE + pause
            done += 1
        pieces.append(np.zeros(int(GAP_CHAPTER * RATE), dtype=np.float32))
        t += GAP_CHAPTER

    with tempfile.TemporaryDirectory() as tmp:
        wav = os.path.join(tmp, "all.wav")
        sf.write(wav, np.concatenate(pieces), RATE)
        meta_file = os.path.join(tmp, "chapters.txt")
        with open(meta_file, "w") as fh:
            fh.write(f";FFMETADATA1\ntitle={meta.get('title', '')}\ncomment=commit {meta.get('commit', '')}\n")
            ends = [m[0] for m in marks[1:]] + [t]
            for (start, title), end in zip(marks, ends):
                fh.write(f"[CHAPTER]\nTIMEBASE=1/1000\nSTART={int(start * 1000)}\nEND={int(end * 1000)}\ntitle={title}\n")
        # Encode beside the target and swap it in: ffmpeg writing in place truncates a file a player may have open.
        partial = os.path.join(os.path.dirname(os.path.abspath(args.out)), f".{os.path.basename(args.out)}.partial.m4a")
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", wav, "-i", meta_file, "-map_metadata", "1",
                        "-c:a", "aac", "-b:a", "96k", partial], check=True)
        os.replace(partial, args.out)
    print(f"{args.out}: {t / 60:.1f} min, {done} lines, {len(marks)} chapters")


if __name__ == "__main__":
    main()
