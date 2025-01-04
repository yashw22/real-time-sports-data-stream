const { Kafka } = require("kafkajs");

const kafka = new Kafka({
  clientId: "game-consumer",
  brokers: ["broker:9092"],
});

const consumer = kafka.consumer({ groupId: "game-consumer-group" });

let latestMessage = {};

async function consumeMessages() {
  await consumer.connect();
  await consumer.subscribe({ topic: "cricket", fromBeginning: true });

  await consumer.run({
    eachMessage: async ({ topic, partition, message }) => {
      latestMessage = JSON.parse(message.value.toString());
      console.log("Consumed message:", JSON.stringify(latestMessage));
    },
  });
}

async function getLatestMessage() {
  return latestMessage;
}

module.exports = {
  consumeMessages,
  getLatestMessage,
};
