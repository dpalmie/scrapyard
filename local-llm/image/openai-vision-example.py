import base64
from pathlib import Path

from openai import OpenAI

# Start exactly ONE of these servers before running the matching function:
#   mlx:      uv run mlx_vlm.server --model mlx-community/gemma-4-e4b-it-4bit --port 8080
#   ollama:   ollama pull gemma4:e4b && ollama serve
#   llamacpp: llama-server -hf ggml-org/gemma-4-E4B-it-GGUF --port 8080

IMAGE_PATH = Path(__file__).parent / "inputs" / "test1.png"
PROMPT = "What is in this image?"

BACKENDS = {
    "mlx": {
        "base_url": "http://localhost:8080/v1",
        "model": "mlx-community/gemma-4-e4b-it-4bit",
        "api_key": "mlx",
    },
    "ollama": {
        "base_url": "http://localhost:11434/v1",
        "model": "gemma4:e4b",
        "api_key": "ollama",
    },
    "llamacpp": {
        "base_url": "http://localhost:8080/v1",
        "model": "ggml-org/gemma-4-E4B-it-GGUF",
        "api_key": "llamacpp",
    },
}


def _data_url(path: Path) -> str:
    b64 = base64.b64encode(path.read_bytes()).decode()
    return f"data:image/png;base64,{b64}"


def _ask(backend: str) -> str:
    cfg = BACKENDS[backend]
    client = OpenAI(base_url=cfg["base_url"], api_key=cfg["api_key"])
    response = client.chat.completions.create(
        model=cfg["model"],
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": PROMPT},
                    {
                        "type": "image_url",
                        "image_url": {"url": _data_url(IMAGE_PATH)},
                    },
                ],
            }
        ],
    )
    return response.choices[0].message.content


def run_mlx():
    return _ask("mlx")


def run_ollama():
    return _ask("ollama")


def run_llamacpp():
    return _ask("llamacpp")


if __name__ == "__main__":
    print(run_mlx())
    # print(run_ollama())
    # print(run_llamacpp())
