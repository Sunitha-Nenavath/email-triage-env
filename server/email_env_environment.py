import random
from typing import Any

try:
    from .models import EmailObservation, EmailAction
except ImportError:
    from models import EmailObservation, EmailAction


DATASETS = {
    "easy": [
        {
            "id": "e1",
            "sender": "spam@fake.com",
            "subject": "Win money",
            "email_text": "Claim prize now",
            "true_category": "spam",
            "true_urgency": "normal"
        },
        {
            "id": "e2",
            "sender": "boss@company.com",
            "subject": "Server Down",
            "email_text": "Fix immediately",
            "true_category": "important",
            "true_urgency": "urgent"
        }
    ],
    "medium": [
        {
            "id": "m1",
            "sender": "newsletter@site.com",
            "subject": "Weekly news",
            "email_text": "Latest updates",
            "true_category": "spam",
            "true_urgency": "normal"
        },
        {
            "id": "m2",
            "sender": "support@vendor.com",
            "subject": "License expiring",
            "email_text": "Renew soon",
            "true_category": "important",
            "true_urgency": "urgent"
        }
    ],
    "hard": [
        {
            "id": "h1",
            "sender": "phishing@fake.com",
            "subject": "Account blocked",
            "email_text": "Click to verify",
            "true_category": "spam",
            "true_urgency": "normal"
        },
        {
            "id": "h2",
            "sender": "team@company.com",
            "subject": "Project update",
            "email_text": "Review later",
            "true_category": "important",
            "true_urgency": "normal"
        }
    ]
}


def grade_email(action: EmailAction, email: dict):

    pred_cat = action.category.lower()
    pred_urg = action.urgency.lower()

    true_cat = email["true_category"]
    true_urg = email["true_urgency"]

    score = 0.2

    if pred_cat == true_cat:
        score += 0.3

    if pred_urg == true_urg:
        score += 0.3

    # 🔥 CRITICAL FIX
    score = max(0.01, min(score, 0.99))

    return score, {}


class EmailTriageEnv:

    def __init__(self):
        self.task_id = None
        self.email = None
        self.step_count = 0
        self.done = False

    def reset(self, task_id="easy"):

        self.task_id = task_id
        self.email = random.choice(DATASETS[task_id])
        self.step_count = 0
        self.done = False

        obs = EmailObservation(
            email_text=self.email["email_text"],
            sender=self.email["sender"],
            subject=self.email["subject"]
        )

        return {
            "task_id": task_id,
            "observation": obs.model_dump()
        }

    def step(self, action: EmailAction):

        self.step_count += 1

        reward, _ = grade_email(action, self.email)

        # 🔥 DOUBLE SAFETY
        reward = max(0.01, min(float(reward), 0.99))

        self.done = True

        return {
            "state": {"step": self.step_count},
            "reward": reward,
            "done": True,
            "info": {}
        }

    def state(self):
        return {
            "task_id": self.task_id,
            "step_count": self.step_count,
            "is_active": not self.done
        }
