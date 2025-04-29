FROM python:3.9-slim

RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /optimizer

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chown -R appuser:appuser /optimizer

EXPOSE 5001

USER appuser

HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:5001/ || exit 1

CMD ["python", "optimizer/main.py"]