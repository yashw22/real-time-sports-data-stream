FROM python:3.9-slim

WORKDIR /app
COPY . /app

# RUN chmod +x ./wait-for-kafka.sh
RUN pip install -r requirements.txt

CMD ["sh", "-c", "sleep 5 && python entry.py"]
