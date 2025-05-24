to_image: |
  FROM python:3.11-slim
  WORKDIR /app
  COPY . /app
  RUN pip install fastapi uvicorn transformers speechbrain fer openai pydantic PyYAML
  CMD ["uvicorn", "evaluator_service:app", "--host", "0.0.0.0", "--port", "8000"]