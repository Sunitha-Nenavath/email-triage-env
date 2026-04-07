"""
server/models.py
Pydantic typed models for Email Triage OpenEnv Environment
"""

from pydantic import BaseModel, ConfigDict
from typing import Any, Optional, Literal

# ── Email Action Model ────────────────────────────────────────────────────────

class EmailAction(BaseModel):
    category: Literal["spam", "important"]
    urgency: Literal["urgent", "normal"]

# ── Email Observation Model ───────────────────────────────────────────────────

class EmailObservation(BaseModel):
    email_text: str
    sender: str
    subject: str

# ── Task info model ───────────────────────────────────────────────────────────

class TaskInfo(BaseModel):
    description: str
    action_format: dict[str, Any]
    difficulty: str

# ── API request/response models ───────────────────────────────────────────────

class StepRequest(BaseModel):
    action: EmailAction

class StepResponse(BaseModel):
    state: dict[str, Any]
    reward: float
    done: bool
    info: dict[str, Any]

class ResetResponse(BaseModel):
    state: dict[str, Any]

class StateResponse(BaseModel):
    task_id: Optional[str]
    step_count: int
    is_active: bool

class TasksResponse(BaseModel):
    tasks: list[str]
    descriptions: dict[str, Any]