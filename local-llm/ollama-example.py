import asyncio

from ollama import AsyncClient, ChatResponse, chat
from openai import OpenAI

# ollama must be installed and running
# (install with
# curl -fsSL https://ollama.com/install.sh | sh
# or reference https://ollama.com/download
# )
# you have to pull the model you're using
# like `ollama pull gemma4:e2b` from cli


def run_sync_response():
    response: ChatResponse = chat(
        model="gemma4:e2b",  # look at https://ollama.com/search for models
        messages=[
            {
                "role": "user",
                "content": "When I say Hello, you say World. Hello...",
            }
        ],
    )

    return response.message.content


def run_stream_response():
    stream = chat(
        model="gemma4:e2b",
        messages=[
            {
                "role": "user",
                "content": "Why is Houston the greatest city in the USA?",
            }
        ],
        stream=True,
    )

    for chunk in stream:
        print(chunk.message.content, end="", flush=True)


async def run_async_response():
    client = AsyncClient()
    response = await client.chat(
        model="gemma4:e2b",
        messages=[
            {
                "role": "user",
                "content": "Why is Houston the greatest city in the USA?",
            }
        ],
    )
    return response.message.content


async def run_async_stream_response():
    client = AsyncClient()
    stream = await client.chat(
        model="gemma4:e2b",
        messages=[
            {
                "role": "user",
                "content": "Why is Houston the greatest city in the USA?",
            }
        ],
        stream=True,
    )

    async for chunk in stream:
        print(chunk.message.content, end="", flush=True)


def run_openai_format():
    # this works since ollama is background service running on port 11434
    # and supports openai format natively
    client = OpenAI(
        base_url="http://localhost:11434/v1",
        api_key="ollama",
    )

    response = client.chat.completions.create(
        model="gemma4:e2b",
        messages=[
            {"role": "system", "content": "You are a helpful local AI."},
            {"role": "user", "content": "What is the capital of France?"},
        ],
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    # print(run_sync_response())
    # run_stream_response()
    # print(asyncio.run(run_async_response()))
    # asyncio.run(run_async_stream_response())
    print(run_openai_format())
