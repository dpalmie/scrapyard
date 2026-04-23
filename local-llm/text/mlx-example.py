from mlx_vlm import generate, load
from mlx_vlm.prompt_utils import apply_chat_template

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

print(result)
# TODO: is there a way to have this as a running server like ollama?
