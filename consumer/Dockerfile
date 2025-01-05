FROM python:3.9-slim

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

CMD ["sh", "-c", "sleep 5 && python entry.py"]
