FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

EXPOSE 7860
ENV PYTHONPATH=/app

# Auto-detect if app is nested inside server or flattened in root
CMD ["python", "server/app.py"]
