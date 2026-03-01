import asyncio, os, time
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())
from openai import AsyncOpenAI


async def test():
    client = AsyncOpenAI(
        base_url="https://models.github.ai/inference", api_key=os.getenv("GITHUB_TOKEN")
    )
    t = time.perf_counter()
    r = await client.chat.completions.create(
        model="Phi-4",
        messages=[
            {
                "role": "system",
                "content": 'You are a risk assessor. Respond only with valid JSON matching: {"llm_score":<0-100>,"reasoning":"...","risk_factors":[],"compensating_factors":[]}',
            },
            {"role": "user", "content": "Rate: credit_score=720, dti=0.28, ltv=0.80"},
        ],
        max_tokens=300,
        temperature=0.3,
        timeout=60,
    )
    elapsed = time.perf_counter() - t
    print(f"Time: {elapsed:.1f}s")
    print("Tokens:", r.usage.completion_tokens if r.usage else "N/A")
    print("Response:", r.choices[0].message.content[:300])


asyncio.run(test())
