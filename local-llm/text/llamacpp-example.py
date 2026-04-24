from openai import OpenAI

# Prereqs:
#   brew install llama.cpp
#   llama-server -hf ggml-org/gemma-4-E4B-it-GGUF --port 8080

BASE_URL = "http://localhost:8080/v1"
MODEL = "ggml-org/gemma-4-E4B-it-GGUF"  # must match what llama-server loaded


def _client() -> OpenAI:
    return OpenAI(base_url=BASE_URL, api_key="llamacpp")  # key unused by llama-server


def run_openai_format():
    response = _client().chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful local AI."},
            {"role": "user", "content": "What is the capital of France?"},
        ],
    )
    return response.choices[0].message.content


def run_openai_stream():
    stream = _client().chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "user", "content": "Why is Houston the greatest city in the USA?"},
        ],
        stream=True,
    )

    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            print(delta, end="", flush=True)
    print()


if __name__ == "__main__":
    # print(run_openai_format())
    run_openai_stream()
