FROM python:3.9-slim

WORKDIR /app
COPY . /app

RUN chmod +x ./wait-for-kafka.sh
RUN pip install kafka-python==2.0.2

CMD ["sh", "-c", "sleep 5 && python start.py"]
