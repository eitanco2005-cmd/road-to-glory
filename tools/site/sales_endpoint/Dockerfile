# Hugging Face Docker Space: the app must listen on port 7860 and run as a non-root user (uid 1000).
FROM python:3.12-slim
RUN useradd -m -u 1000 user
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
# /data is the persistent-storage mount on HF (paid add-on); otherwise files live in /app/data and are
# lost on restart unless HF_DATASET_REPO backup is configured (see README).
RUN mkdir -p /app/data && chown -R user /app
USER user
ENV DATA_DIR=/app/data PYTHONUNBUFFERED=1
EXPOSE 7860
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860", "--proxy-headers", "--forwarded-allow-ips", "*"]
