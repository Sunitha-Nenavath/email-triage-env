"""
server/email_env_environment.py
Core Email Triage Environment — Tasks, Graders, Reward Logic
"""

import random
from typing import Any
try:
    from .models import EmailObservation, EmailAction
except ImportError:
    from models import EmailObservation, EmailAction

# ── Datasets ──────────────────────────────────────────────────────────────────

DATASET_EASY = [
    {
        "id": "easy_1",
        "sender": "prince@nigeria-royal-bank.xyz",
        "subject": "URGENT INVESTMENT OPPORTUNITY!!!",
        "email_text": "You have won $10,000,000! Please send your bank details and social security number to claim your prize immediately.",
        "true_category": "spam",
        "true_urgency": "normal"
    },
    {
        "id": "easy_2",
        "sender": "boss@company.com",
        "subject": "CRITICAL: Server is DOWN",
        "email_text": "The main production server is down. We are losing money by the second. Please fix this IMMEDIATELY.",
        "true_category": "important",
        "true_urgency": "urgent"
    },
    # ... (keeping descriptions short for this tool call, but I should use the full content)
]

# Note: I will use the full content from the previous view_file call but I'll make sure to use the relative import.
# I'll use the content I read earlier.

DATASET_EASY = [
    {
        "id": "easy_1",
        "sender": "prince@nigeria-royal-bank.xyz",
        "subject": "URGENT INVESTMENT OPPORTUNITY!!!",
        "email_text": "You have won $10,000,000! Please send your bank details and social security number to claim your prize immediately.",
        "true_category": "spam",
        "true_urgency": "normal"
    },
    {
        "id": "easy_2",
        "sender": "boss@company.com",
        "subject": "CRITICAL: Server is DOWN",
        "email_text": "The main production server is down. We are losing money by the second. Please fix this IMMEDIATELY.",
        "true_category": "important",
        "true_urgency": "urgent"
    },
    {
        "id": "easy_3",
        "sender": "marketing@shoe-store.com",
        "subject": "Buy 1 Get 1 Free on all sneakers",
        "email_text": "Don't miss our summer sale! Huge discounts on all styles. Click here to unsubscribe.",
        "true_category": "spam",
        "true_urgency": "normal"
    },
    {
        "id": "easy_4",
        "sender": "hr@company.com",
        "subject": "Annual Review Schedule",
        "email_text": "Please find attached the schedule for your annual review next month. No immediate action required.",
        "true_category": "important",
        "true_urgency": "normal"
    }
]

DATASET_MEDIUM = [
    {
        "id": "med_1",
        "sender": "newsletter@industry-news.com",
        "subject": "Top 10 AI trends this week",
        "email_text": "Read our latest article on how AI is changing the world. Also, check out our sponsor's new product.",
        "true_category": "spam",
        "true_urgency": "normal"
    },
    {
        "id": "med_2",
        "sender": "client-support@vendor.com",
        "subject": "Action Required: License Expiration",
        "email_text": "Your enterprise license will expire in 2 days. Please renew to avoid service interruption during your launch.",
        "true_category": "important",
        "true_urgency": "urgent"
    },
    {
        "id": "med_3",
        "sender": "unknown.founder@startup.io",
        "subject": "Partnership opportunity",
        "email_text": "I noticed your company is doing great things. I'd love to chat for 15 minutes about how our product can help you.",
        "true_category": "spam",
        "true_urgency": "normal"
    },
    {
        "id": "med_4",
        "sender": "tax-department@gov.org",
        "subject": "Question regarding 2023 filings",
        "email_text": "We noticed a discrepancy in your Q4 filings. Please provide the missing documents by the end of the month.",
        "true_category": "important",
        "true_urgency": "normal"
    }
]

DATASET_HARD = [
    {
        "id": "hard_1",
        "sender": "billing-update@paypal-secure-login.com",
        "subject": "URGENT: Your account has been suspended",
        "email_text": "Dear user, your account has been temporarily restricted due to suspicious activity. Click here within 24 hours to verify your identity.",
        "true_category": "spam",
        "true_urgency": "normal"
    },
    {
        "id": "hard_2",
        "sender": "sarah.jenkins@partner-firm.com",
        "subject": "Re: Project Alpha Draft",
        "email_text": "Hey, I was just looking over the draft you sent last week. Looks fine mostly, but we might want to tweak the conclusion. No rush, we can discuss next Tuesday.",
        "true_category": "important",
        "true_urgency": "normal"
    },
    {
        "id": "hard_3",
        "sender": " automated-alert@aws-internal-monitor.net",
        "subject": "AWS EC2 instance i-0abcdef123 CPU utilization > 95%",
        "email_text": "Alarm: High CPU usage detected on backend-db-primary. This might cause latency issues. Please investigate.",
        "true_category": "important",
        "true_urgency": "urgent"
    },
    {
        "id": "hard_4",
        "sender": "john.smith@gmail.com",
        "subject": "URGENT ISSUE",
        "email_text": "Hello, I am a user of your app and I can't find the settings menu to change my avatar. PLEASE HELP MEE!!",
        "true_category": "spam",
        "true_urgency": "normal"
    }
]

DATASETS = {
    "easy": DATASET_EASY,
    "medium": DATASET_MEDIUM,
    "hard": DATASET_HARD
}

TASK_DESCRIPTIONS = {
    "easy": {
        "description": "Classify obvious spam/important emails and their urgency.",
        "action_format": {"category": "spam | important", "urgency": "urgent | normal"},
        "difficulty": "easy",
    },
    "medium": {
        "description": "Classify a mix of promotional, informational, and critical emails.",
        "action_format": {"category": "spam | important", "urgency": "urgent | normal"},
        "difficulty": "medium",
    },
    "hard": {
        "description": "Classify ambiguous, real-world emails such as phishing attempts or subtle client communications.",
        "action_format": {"category": "spam | important", "urgency": "urgent | normal"},
        "difficulty": "hard",
    },
}

# ── Grader ────────────────────────────────────────────────────────────────────

def grade_email(action: EmailAction, email: dict) -> tuple[float, dict]:
    score = 0.0
    
    pred_category = action.category.strip().lower()
    true_category = email["true_category"]
    
    pred_urgency = action.urgency.strip().lower()
    true_urgency = email["true_urgency"]
    
    cat_correct = False
    urg_correct = False

    if pred_category == true_category:
        score += 0.5
        cat_correct = True
        
    if pred_urgency == true_urgency:
        score += 0.5
        urg_correct = True

    return round(score, 3), {
        "predicted_category": pred_category,
        "true_category": true_category,
        "category_correct": cat_correct,
        "predicted_urgency": pred_urgency,
        "true_urgency": true_urgency,
        "urgency_correct": urg_correct,
    }


# ── Environment Class ─────────────────────────────────────────────────────────

class EmailTriageEnv:
    TASK_DESCRIPTIONS = TASK_DESCRIPTIONS

    def __init__(self):
        self._task_id: str | None = None
        self._current_email: dict | None = None
        self._step_count: int = 0
        self._done: bool = False

    def reset(self, task_id: str = "easy") -> dict[str, Any]:
        if task_id not in DATASETS:
            raise ValueError(f"Unknown task_id '{task_id}'.")

        self._task_id = task_id
        self._current_email = random.choice(DATASETS[task_id]).copy()
        self._step_count = 0
        self._done = False

        obs = EmailObservation(
            email_text=self._current_email["email_text"],
            sender=self._current_email["sender"],
            subject=self._current_email["subject"]
        )

        return {
            "task_id": self._task_id,
            "task_description": TASK_DESCRIPTIONS[self._task_id],
            "observation": obs.model_dump()
        }

    def step(self, action: EmailAction) -> dict[str, Any]:
        if self._current_email is None or self._task_id is None:
            return {
                "state": {"error": "Environment not initialized."},
                "reward": 0.0,
                "done": True,
                "info": {}
            }

        self._step_count += 1
        reward, grader_info = grade_email(action, self._current_email)
        self._done = True

        return {
            "state": {
                "task_id": self._task_id,
                "email_id": self._current_email["id"],
                "step": self._step_count,
            },
            "reward": reward,
            "done": self._done,
            "info": {
                **grader_info,
                "step_count": self._step_count,
            }
        }

    def state(self) -> dict[str, Any]:
        return {
            "task_id": self._task_id,
            "step_count": self._step_count,
            "is_active": self._current_email is not None and not self._done,
        }
