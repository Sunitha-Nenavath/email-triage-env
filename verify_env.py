import requests
import json

URL = "http://127.0.0.1:7860"

def test():
    print("Testing /reset...")
    res = requests.post(f"{URL}/reset", json={"task_id": "easy"})
    print(f"Status: {res.status_code}")
    data = res.json()
    print("Response data:")
    print(json.dumps(data, indent=2))
    
    # Check if observation has the nested email object
    obs = data.get("observation", {})
    if "email" in obs and "task_id" in obs:
        print("[SUCCESS] Observation structure: Correct (nested 'email' and 'task_id')")
    else:
        print("[FAILURE] Observation structure: Incorrect")
        
    print("\nTesting /step...")
    action = {"category": "spam", "urgency": "normal"}
    res = requests.post(f"{URL}/step", json=action)
    print(f"Status: {res.status_code}")
    step_data = res.json()
    print("Response data:")
    print(json.dumps(step_data, indent=2))
    
    reward = step_data.get("reward")
    if reward is not None and 0.0 < reward < 1.0:
        print(f"✅ Reward: Correct ({reward})")
    else:
        print(f"❌ Reward: Incorrect ({reward})")

if __name__ == "__main__":
    try:
        test()
    except Exception as e:
        print(f"Test failed: {e}")
