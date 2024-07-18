FROM python:3.9-slim

WORKDIR /app

COPY benchmark.py /app/benchmark.py

RUN pip install numpy psutil prometheus_client requests

CMD ["python", "/app/benchmark.py"]
