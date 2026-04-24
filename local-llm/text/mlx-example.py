from mlx_vlm import generate, load
from mlx_vlm.prompt_utils import apply_chat_template
from openai import OpenAI


def run_one_shot():
    # look at https://huggingface.co/mlx-community for more models
    model, processor = load("mlx-community/gemma-4-e2b-it-4bit")

    prompt = apply_chat_template(
        processor,
        model.config,
        "Write a story about Einstein",
    )

    result = generate(
        model=model,
        processor=processor,
        prompt=prompt,
        max_tokens=500,
        temperature=1.0,
        top_p=0.95,
        top_k=64,
        # verbose=True,
    )

    return result


def run_openai_format():
    # mlx-vlm ships its own FastAPI server with an OpenAI-compatible
    # /v1/chat/completions endpoint. Start it in another terminal first:
    #   uv run mlx_vlm.server --model mlx-community/gemma-4-e2b-it-4bit --port 8080
    # (omit --model to have the server lazy-load on first request, ollama-style)
    client = OpenAI(
        base_url="http://localhost:8080/v1",
        api_key="mlx",  # server doesn't validate, but the client requires a value
    )

    response = client.chat.completions.create(
        model="mlx-community/gemma-4-e2b-it-4bit",
        messages=[
            {"role": "system", "content": "You are a helpful local AI."},
            {"role": "user", "content": "What is the capital of France?"},
        ],
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    # print(run_one_shot())
    print(run_openai_format())
