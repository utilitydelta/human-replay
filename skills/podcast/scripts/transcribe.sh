#!/usr/bin/env bash
# Transcribe podcast episodes with faster-whisper on the GPU, one timestamped .txt per file.
# Skips files already transcribed. About 40 s per 45 min episode on the RTX 5080.
#
#   scripts/transcribe.sh <out-dir> <audio>...
#   scripts/transcribe.sh /tmp/transcripts episode.m4a
set -euo pipefail

out=$1; shift
mkdir -p "$out"
deps=(--no-project --with faster-whisper --with nvidia-cublas-cu12 --with "nvidia-cudnn-cu12==9.*")

# ctranslate2 finds cuBLAS and cuDNN through LD_LIBRARY_PATH, which must be set before the process starts.
libs=$(uv run "${deps[@]}" python -I -c "
import nvidia.cublas, nvidia.cudnn
print(list(nvidia.cublas.__path__)[0] + '/lib:' + list(nvidia.cudnn.__path__)[0] + '/lib')")

LD_LIBRARY_PATH="$libs${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}" uv run "${deps[@]}" python -I - "$out" "$@" <<'EOF'
import os, sys, time
from faster_whisper import WhisperModel

out, files = sys.argv[1], sys.argv[2:]
model = WhisperModel("large-v3-turbo", device="cuda", compute_type="float16")
for f in files:
    dst = os.path.join(out, os.path.splitext(os.path.basename(f))[0] + ".txt")
    if os.path.exists(dst):
        continue
    started = time.time()
    segments, info = model.transcribe(f, language="en", vad_filter=True, beam_size=5)
    with open(dst + ".tmp", "w") as fh:
        for s in segments:
            fh.write(f"[{int(s.start // 60):02d}:{int(s.start % 60):02d}] {s.text.strip()}\n")
    os.replace(dst + ".tmp", dst)
    print(f"{os.path.basename(dst)}: {info.duration / 60:.1f} min in {time.time() - started:.0f} s", flush=True)
EOF
