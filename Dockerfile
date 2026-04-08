FROM python:3.11-slim

WORKDIR /app

# This wildcard approach copies requirements whether it's flattened or nested
COPY *requirements.txt server/requirements.tx[t] ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

EXPOSE 7860
ENV PYTHONPATH=/app

# Auto-detect if app is nested inside server or flattened in root
CMD ["sh", "-c", "if [ -f server/app.py ]; then exec uvicorn server.app:app --host 0.0.0.0 --port 7860; else exec uvicorn app:app --host 0.0.0.0 --port 7860; fi"]
