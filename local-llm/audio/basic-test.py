from mlx_audio.tts.utils import load_model

model = load_model("mlx-community/Qwen3-TTS-12Hz-0.6B-Base-bf16")
results = list(
    model.generate(
        text="Hello, welcome to MLX-Audio!",
        voice="Chelsie",
        language="English",
    )
)

audio = results[0].audio
print(audio)
