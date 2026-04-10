"""
server/tasks.py
Helper for task descriptions
"""

def get_task(task_id: str):
    return {
        "easy": "Basic email classification",
        "medium": "Moderate spam filtering",
        "hard": "Advanced phishing detection"
    }.get(task_id, "Unknown task")
