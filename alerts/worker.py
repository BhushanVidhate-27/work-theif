from openai import OpenAI
from config import OPENROUTER_API_KEY, WORKER_MODEL

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

def do_work(task: str) -> str:
    response = client.chat.completions.create(
        model=WORKER_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful Worker agent. Complete the given task carefully and return only the result."
            },
            {"role": "user", "content": task}
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content