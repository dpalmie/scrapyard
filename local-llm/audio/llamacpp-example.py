import subprocess
from pathlib import Path

# Prereqs:
#   brew install llama.cpp  # provides the `llama-tts` binary
#
# Unlike `llama-server`, which has no TTS HTTP endpoint, TTS in llama.cpp is
# a separate CLI tool (`llama-tts`) that pairs a text LLM (OuteTTS) with a
# vocoder (WavTokenizer) and writes a .wav to disk. `--tts-oute-default`
# pulls both models from Hugging Face on first run.

TEXT = "Hello from a local model. Testing text to audio with llama dot c p p."
OUT_DIR = Path(__file__).parent / "outputs"
OUT_DIR.mkdir(exist_ok=True)
OUT_PATH = OUT_DIR / "llamacpp.wav"


def run_cli() -> Path:
    cmd = [
        "llama-tts",
        "--tts-oute-default",
        "-p",
        TEXT,
        "-o",
        str(OUT_PATH),
    ]
    # check=True raises CalledProcessError on non-zero exit, which is what we
    # want: a silent failure would leave a stale or missing wav.
    subprocess.run(cmd, check=True)
    return OUT_PATH


if __name__ == "__main__":
    print(run_cli())
