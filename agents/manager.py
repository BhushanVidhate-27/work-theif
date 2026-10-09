from openai import OpenAI
from config import OPENROUTER_API_KEY, MANAGER_MODEL
from alerts.telegram import send_alert

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

def review_and_decide(original_task: str, worker_result: str, history: list) -> dict:
    history_text = "\n\n".join(history[-3:])  # last 3 steps only

    prompt = f"""
You are a strict Manager agent.

Original Task: {original_task}

Recent History:
{history_text}

Latest Worker Result:
{worker_result}

Rules:
- If the original task is fully completed → reply with NEXT_TASK: DONE
- Do NOT keep asking for more features unless the original task is incomplete
- Be strict. Prefer finishing over adding extra work.

Reply ONLY in this format:

APPROVED: yes/no
NEXT_TASK: <task or DONE>
REASON: <short reason>
"""

    response = client.chat.completions.create(
        model=MANAGER_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    content = response.choices[0].message.content.strip()
    print(content)

    approved = "APPROVED: yes" in content.upper()

    if not approved:
        send_alert(f"⚠️ Manager rejected the work:\n\n{content}")

    return {
        "approved": approved,
        "raw": content
    }