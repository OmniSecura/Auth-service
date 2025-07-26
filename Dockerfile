FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY src ./src
COPY start_service.py ./start_service.py

ENV PYTHONPATH=/app

CMD ["python", "start_service.py"]