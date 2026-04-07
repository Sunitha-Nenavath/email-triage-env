from fastapi import FastAPI
from pydantic import BaseModel
from models import EmailAction
from server.email_env_environment import EmailTriageEnv

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