import sys
import os

# Ensure both the current directory and parent directory are in sys.path
# This handles both local nested structure and flat Hugging Face deployments
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI
from pydantic import BaseModel
try:
    from models import EmailAction
except ImportError:
    # Fallback if somehow models is relative
    from email_env.models import EmailAction

try:
    from server.email_env_environment import EmailTriageEnv
except ImportError:
    from email_env_environment import EmailTriageEnv

app = FastAPI()
env = EmailTriageEnv()

class ResetRequest(BaseModel):
    task_id: str = "easy"

@app.get("/")
def health():
    return {"status": "ok", "environment": "email-triage", "version": "1.0.0"}

@app.get("/state")
def get_state():
    return env.state()

@app.get("/tasks")
def tasks():
    return {
        "tasks": list(EmailTriageEnv.TASK_DESCRIPTIONS.keys()),
        "descriptions": EmailTriageEnv.TASK_DESCRIPTIONS
    }

@app.post("/reset")
def reset(req: ResetRequest = None):
    task_id = req.task_id if req else "easy"
    return env.reset(task_id=task_id)

@app.post("/step")
def step(action: EmailAction):
    return env.step(action)

def main():
    import uvicorn
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860, reload=False)

if __name__ == "__main__":
    main()