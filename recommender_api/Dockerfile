FROM python:3.10-slim

RUN groupadd -r appuser && useradd -r -g appuser appuser
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chown -R appuser:appuser /app

ENV PORT=5000

EXPOSE 5000

USER appuser

HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:${PORT}/health || exit 1

CMD ["python", "-m", "app.app"]