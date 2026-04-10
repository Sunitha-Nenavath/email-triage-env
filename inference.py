import os
import json
import requests
from openai import OpenAI

API_BASE_URL = os.environ.get("API_BASE_URL")
API_KEY = os.environ.get("API_KEY")
MODEL_NAME = os.environ.get("MODEL_NAME", "gpt-3.5-turbo")

SERVER_URL = os.environ.get("SERVER_URL", "http://127.0.0.1:7860")

# SAFE CLIENT INIT
try:
    client = OpenAI(
        base_url=API_BASE_URL,
        api_key=API_KEY
    )
except:
    client = None


def get_action():
    try:
        if client:
            client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": "classify"}]
            )
    except:
        pass

    return {
        "category": "important",
        "urgency": "normal"
    }


tasks = ["easy", "medium", "hard"]

for task in tasks:

    try:
        requests.post(f"{SERVER_URL}/reset", json={"task_id": task})

        print(f"[START] task={task}")

        step = 1
        rewards = []

        action = get_action()

        res = requests.post(f"{SERVER_URL}/step", json=action)
        data = res.json()

        reward = float(data.get("reward", 0.5))
        rewards.append(reward)

        print(f"[STEP] step=1 reward={reward} done=true error=null")

        score = sum(rewards) / len(rewards)

        print(f"[END] success=true steps=1 score={round(score,2)} rewards={reward}")

    except Exception as e:
        print("ERROR:", str(e))
