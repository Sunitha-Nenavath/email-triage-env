import os
import sys
import json
import requests
from openai import OpenAI
from pydantic import BaseModel

# 1. Hardware Env Vars Handling
# Use 'or' instead of default in getenv to handle cases where var is set but empty ("")
API_BASE_URL = os.getenv("API_BASE_URL") or "https://api.openai.com/v1"
MODEL_NAME = os.getenv("MODEL_NAME") or "gpt-3.5-turbo"
HF_TOKEN = os.getenv("HF_TOKEN") or ""

# 2. Client Initialization with Error Handling
try:
    if not API_BASE_URL.startswith("http"):
        # Ensure it's a valid URL format for httpx
        API_BASE_URL = "https://api.openai.com/v1"

    print(f"Initializing OpenAI client with Base URL: {API_BASE_URL} and Model: {MODEL_NAME}")
    
    client = OpenAI(
        api_key=HF_TOKEN if HF_TOKEN else "dummy-key",
        base_url=API_BASE_URL,
    )
except Exception as e:
    print(f"Critical Error: Failed to initialize OpenAI client: {e}")
    # Fallback to default if everything else fails
    client = OpenAI(api_key="dummy-key")

# Evaluator typically provides SERVER_URL, fallback to 7860 (Dockerfile port)
SERVER_URL = os.getenv("SERVER_URL") or "http://127.0.0.1:7860"

def get_action_from_llm(email_text: str, subject: str, sender: str) -> dict:
    prompt = f"""
    You are an AI Email Assistant. 
    Classify the following email into a category (spam or important) and determine its urgency (urgent or normal).
    
    Sender: {sender}
    Subject: {subject}
    Email Text: {email_text}

    Respond ONLY in valid JSON format with keys "category" and "urgency".
    category must be either "spam" or "important".
    urgency must be either "urgent" or "normal".
    """

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a helpful email triage assistant. Output only JSON."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.0
        )
        content = response.choices[0].message.content
        return json.loads(content)
    except Exception as e:
        # Fallback in case of API issues
        return {"category": "important", "urgency": "normal"}

tasks = ["easy", "medium", "hard"]

for task_id in tasks:
    # 1. Reset Env
    res = requests.post(f"{SERVER_URL}/reset", json={"task_id": task_id})
    if res.status_code != 200:
        print(f"Error resetting env for task {task_id}: {res.text}")
        continue
    
    reset_data = res.json()
    obs = reset_data.get("observation", {})
    
    print(f"[START] task_id={task_id}")
    
    total_reward = 0.0
    done = False
    step_count = 1
    
    while not done:
        # 2. Get action from LLM
        action_dict = get_action_from_llm(
            email_text=obs.get("email_text", ""),
            subject=obs.get("subject", ""),
            sender=obs.get("sender", "")
        )
        
        # Ensure fallback format
        if "category" not in action_dict or "urgency" not in action_dict:
            action_dict = {"category": "important", "urgency": "normal"}
            
        action_payload = {
            "category": action_dict["category"],
            "urgency": action_dict["urgency"]
        }
        
        # 3. Step Env
        step_res = requests.post(f"{SERVER_URL}/step", json=action_payload)
        if step_res.status_code != 200:
            print(f"Error stepping env: {step_res.text}")
            break
            
        step_data = step_res.json()
        reward = step_data.get("reward", 0.0)
        done = step_data.get("done", True)
        
        print(f"[STEP] step={step_count} reward={reward} action={json.dumps(action_payload)}")
        
        total_reward += float(reward)
        step_count += 1
        
        if done:
            break
            
    print(f"[END] task_id={task_id} total_reward={total_reward}")