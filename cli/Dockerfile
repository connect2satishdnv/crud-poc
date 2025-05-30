# --- File: cli/Dockerfile ---
FROM python:3.10
WORKDIR /app
COPY . .
RUN pip install click requests
ENTRYPOINT ["python", "main.py"]
