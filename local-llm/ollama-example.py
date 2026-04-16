import asyncio

from ollama import AsyncClient, ChatResponse, chat

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


if __name__ == "__main__":
    # print(run_sync_response())
    # run_stream_response()
    # print(asyncio.run(run_async_response()))
    asyncio.run(run_async_stream_response())
