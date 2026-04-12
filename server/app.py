"""
server/app.py
Main entry point for the OpenEnv Email Triage Environment
"""

import sys
import os

# Ensure the server directory is in sys.path for relative imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

try:
    from .models import EmailAction, EmailObservation, EmailDetails
    from .email_env_environment import EmailTriageEnv
except ImportError:
    from models import EmailAction, EmailObservation, EmailDetails
    from email_env_environment import EmailTriageEnv

app = FastAPI(title="Email Triage AI Environment")
env = EmailTriageEnv()

class ResetRequest(BaseModel):
    task_id: str = "easy"

@app.get("/")
def health():
    return {
        "status": "ok", 
        "environment": "email-triage", 
        "version": "1.0.0",
        "author": "NENAVATH SUNITHA"
    }

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
    try:
        return env.reset(task_id=task_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/step")
def step(action: EmailAction):
    return env.step(action)

def main():
    """
    Mandatory main function for OpenEnv multi-mode deployment.
    """
    import uvicorn
    # Use the string "app.app:app" if running from the parent directory, 
    # or "app:app" if running from within server/
    port = int(os.environ.get("PORT", 7860))
    uvicorn.run(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()
