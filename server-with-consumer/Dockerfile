FROM node:22.12.0-slim

WORKDIR /app

COPY . /app
RUN npm install

CMD ["sh", "-c", "sleep 10 && npm start"]
