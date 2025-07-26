FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY src ./src

ENV PYTHONPATH=/app

CMD ["uvicorn", "src.server:app", "--host", "0.0.0.0", "--port", "8000"]