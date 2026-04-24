from pathlib import Path

import numpy as np
from mlx_audio.audio_io import write as audio_write
from mlx_audio.tts.utils import load_model
from openai import OpenAI

MODEL = "mlx-community/Qwen3-TTS-12Hz-1.7B-Base-bf16"
VOICE = "Ryan"
TEXT = "Hello from a local model. Testing text to audio with MLX on Apple Silicon."

OUT_DIR = Path(__file__).parent / "outputs"
OUT_DIR.mkdir(exist_ok=True)


def run_one_shot() -> Path:
    model = load_model(MODEL)
    segments = list(model.generate(text=TEXT, voice=VOICE, language="English"))
    audio = np.concatenate([np.asarray(s.audio) for s in segments])

    out_path = OUT_DIR / "mlx.wav"
    audio_write(out_path, audio, samplerate=model.sample_rate, format="wav")
    return out_path


def run_openai_format() -> Path:
    # Start server first: uv run mlx_audio.server --port 8000
    client = OpenAI(base_url="http://localhost:8000/v1", api_key="mlx")

    out_path = OUT_DIR / "mlx-openai.wav"
    with client.audio.speech.with_streaming_response.create(
        model=MODEL,
        voice=VOICE,
        input=TEXT,
        response_format="wav",
    ) as response:
        response.stream_to_file(out_path)

    return out_path


if __name__ == "__main__":
    print(run_one_shot())
    # print(run_openai_format())
