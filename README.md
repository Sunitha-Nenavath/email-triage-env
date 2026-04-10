---
title: Email Triage Env
emoji: 📧
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
---

# 📧 Email Triage Environment

An OpenEnv-compatible real-world environment where an AI agent learns to triage corporate emails.

## Overview

Companies receive hundreds of emails daily. This environment simulates the task of:
1. **Classifying** emails into categories (`spam` vs `important`)
2. **Determining** email urgency (`urgent` vs `normal`)

---

## Tasks

| Task ID  | Difficulty | Description |
|----------|------------|-------------|
| `easy`   | Easy       | Classify obvious spam/important emails and their urgency |
| `medium` | Medium     | Classify a mix of promotional, informational, and critical emails |
| `hard`   | Hard       | Classify ambiguous, real-world emails such as phishing attempts or subtle communications |

---

## Action Space (All Tasks)

```json
{
  "category": "spam | important",
  "urgency": "urgent | normal"
}
```

---

## Observation Space

```json
{
  "task_id": "easy",
  "email": {
    "subject": "URGENT INVESTMENT OPPORTUNITY!!!",
    "email_text": "You have won $10,000,000...",
    "sender": "prince@nigeria-royal-bank.xyz"
  }
}
```

---

## Reward Function

- +0.5 if `category` is correct.
- +0.5 if `urgency` is correct.
- Total score range: `0.0` to `1.0`.

---

## Setup & Run Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Start the environment server
.\runenv.bat

# Run baseline inference (in another terminal)
export API_BASE_URL=https://api-inference.huggingface.co/v1
export MODEL_NAME=meta-llama/Llama-3.1-8B-Instruct
export HF_TOKEN=your_hf_token_here

python inference.py
```

---

## Docker

```bash
docker build -t email-triage-env .
docker run -p 7860:7860 email-triage-env
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/reset` | Reset environment (pass `{"task_id": "easy"}` as JSON body) |
| POST | `/step` | Submit action, get reward |
| GET | `/state` | Get current state |
| GET | `/tasks` | List all tasks |

---

## Deployment (Hugging Face Spaces)

```bash
# Login to HF
huggingface-cli login

# Push to Spaces
openenv push --repo-id your-username/email-triage-env
```

---

## Environment Variables

| Variable | Description |
|----------|-------------|
| `API_BASE_URL` | LLM API endpoint (e.g. HF Inference API) |
| `MODEL_NAME` | Model identifier for inference |
| `HF_TOKEN` | Hugging Face token / API key |