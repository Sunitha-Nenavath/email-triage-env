FROM python:3.11-slim

WORKDIR /app

# Copy requirements from server dir if it exists, otherwise define directly or we copy all first
COPY server/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

EXPOSE 7860

# We need the base directory in PYTHONPATH so it can find `models.py`
ENV PYTHONPATH=/app

CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]
