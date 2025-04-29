FROM python:3.10-slim

RUN groupadd -r appuser && useradd -r -g appuser appuser
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*


FROM python:3.10-slim

RUN groupadd -r appuser && useradd -r -g appuser appuser
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chown -R appuser:appuser /app

# Set the PORT environment variable to 3000 as default
ENV PORT=3000

EXPOSE 3000

USER appuser

# Update the health check to use PORT env var
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:${PORT}/health || exit 1

CMD ["python", "-m", "app.app"]