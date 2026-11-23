from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",
)


completion = client.chat.completions.create(
    model="nvidia/nemotron-3-ultra-550b-a55b:free",
    messages=[{"role": "user", "content": "What is the meaning of life?"}],
)

print(completion.choices[0].message.content)