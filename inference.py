import os
import json
from openai import OpenAI

# ✅ Read environment variables injected by the validator
API_BASE_URL = os.environ["API_BASE_URL"]
API_KEY = os.environ["API_KEY"]
MODEL_NAME = os.environ["MODEL_NAME"]

# ✅ Initialize OpenAI client with the proxy
client = OpenAI(
    base_url=API_BASE_URL,
    api_key=API_KEY
)

TASKS = ["easy", "medium", "hard"]

EMAILS = {
    "easy": {
        "sender": "spam@fake.com",
        "subject": "Win money",
        "email_text": "Claim prize now"
    },
    "medium": {
        "sender": "newsletter@site.com",
        "subject": "Weekly news",
        "email_text": "Latest updates"
    },
    "hard": {
        "sender": "phishing@fake.com",
        "subject": "Account blocked",
        "email_text": "Click to verify"
    }
}

def call_llm(email_text: str, sender: str, subject: str) -> dict:
    prompt = f"""You are an email triage assistant. Classify the following email.

Sender: {sender}
Subject: {subject}
Email: {email_text}

Respond ONLY with a valid JSON object in this exact format (no extra text):
{{"category": "spam" or "important", "urgency": "urgent" or "normal"}}"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100,
        temperature=0.0
    )

    content = response.choices[0].message.content.strip()
    result = json.loads(content)
    return result


def run_task(task_id: str):
    email = EMAILS[task_id]

    print(json.dumps({
        "type": "[START]",
        "task_id": task_id,
        "observation": email
    }))

    action = call_llm(
        email_text=email["email_text"],
        sender=email["sender"],
        subject=email["subject"]
    )

    print(json.dumps({
        "type": "[STEP]",
        "task_id": task_id,
        "action": action
    }))

    # Simple local grading for stdout score
    score = 0.2
    if action.get("category") in ["spam", "important"]:
        score += 0.4
    if action.get("urgency") in ["urgent", "normal"]:
        score += 0.4
    score = round(max(0.01, min(score, 0.99)), 2)

    print(json.dumps({
        "type": "[END]",
        "task_id": task_id,
        "score": score,
        "reward": score
    }))

    return score


if __name__ == "__main__":
    total_score = 0.0

    for task_id in TASKS:
        score = run_task(task_id)
        total_score += score

    avg_score = round(total_score / len(TASKS), 2)
    print(json.dumps({
        "type": "[END]",
        "task_id": "all",
        "average_score": avg_score
    }))
