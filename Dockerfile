FROM python:3.11-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 libglib2.0-0 ffmpeg && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt backend/requirements.txt ./tmp/
RUN pip install --no-cache-dir -r backend/requirements.txt
COPY . .
ENV PORT=7860 CAPTURE_DIR=/app/captures
EXPOSE 7860
CMD ["python", "app.py"]
