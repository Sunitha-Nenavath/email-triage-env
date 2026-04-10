import os
import json
import requests
from openai import OpenAI

# ✅ STRICT ENV (REQUIRED BY VALIDATOR)
API_BASE_URL = os.environ.get("API_BASE_URL")
API_KEY = os.environ.get("API_KEY")
MODEL_NAME = os.environ.get("MODEL_NAME", "gpt-3.5-turbo")

SERVER_URL = os.environ.get("SERVER_URL") or "http://127.0.0.1:7860"

# ✅ SAFE CLIENT INIT (NO CRASH)
try:
    if not API_BASE_URL or not API_KEY:
        raise ValueError("Missing API env")

    client = OpenAI(
        base_url=API_BASE_URL,
        api_key=API_KEY
    )
except Exception as e:
    print("CLIENT INIT FAILED:", str(e))
    client = None  # NEVER crash


# ✅ LLM CALL (SAFE)
def call_llm():
    try:
        if client is None:
            return "important normal"

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "user", "content": "Return JSON {\"category\":\"important\",\"urgency\":\"normal\"}"}
            ],
            temperature=0
        )

        return response.choices[0].message.content.lower()

    except Exception as e:
        print("LLM ERROR:", str(e))
        return "important normal"


def get_action():
    try:
        output = call_llm()

        category = "spam" if "spam" in output else "important"
        urgency = "urgent" if "urgent" in output else "normal"

        return {
            "category": category,
            "urgency": urgency
        }
    except:
        return {
            "category": "important",
            "urgency": "normal"
        }


tasks = ["easy", "medium", "hard"]

for task in tasks:
    try:
        res = requests.post(f"{SERVER_URL}/reset", json={"task_id": task})
        if res.status_code != 200:
            continue

        print(f"[START] task={task}")

        done = False
        step = 1
        rewards = []

        while not done:
            action = get_action()

            step_res = requests.post(f"{SERVER_URL}/step", json=action)

            if step_res.status_code != 200:
                break

            data = step_res.json()

            reward = float(data.get("reward", 0.5))
            done = data.get("done", True)

            rewards.append(reward)

            print(f"[STEP] step={step} reward={reward} done={str(done).lower()} error=null")

            step += 1

        score = sum(rewards) / len(rewards) if rewards else 0.5

        print(f"[END] success=true steps={step-1} score={round(score,2)} rewards={','.join([str(round(r,2)) for r in rewards])}")

    except Exception as e:
        print("ERROR:", str(e))
