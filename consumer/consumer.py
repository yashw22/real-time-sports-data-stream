import os
import logging
import json
from kafka import KafkaConsumer  # type: ignore

from cricket import consume_cricket_data

BROKER_SERVER = os.getenv("BROKER_SERVER")
KAFKA_PARTITIONS = os.getenv("KAFKA_PARTITIONS")

def setup_consumer(topic, game_id):
    consumer = None
    try:
        consumer = KafkaConsumer(
            topic,
            group_id=f"{game_id}_group",
            bootstrap_servers=BROKER_SERVER,
            auto_offset_reset='earliest',
            value_deserializer=lambda v: json.loads(v.decode('utf-8')),
        )
        logging.info(f"'{topic}' Consumer started. Waiting for messages...")
        for message in consumer:
            if message.value['game_id'] != game_id:
                continue

            if topic == 'cricket':
                consume_cricket_data(message.value)
            # else:
            #     consume_game_data(topic, game_id)

            # data = message.value
            # logging.info(f"Consumed message: {game_id} {data}")

    except Exception as e:
        logging.error(
            f"Error consuming messages from '{topic}, {game_id}': {e}")
    finally:
        consumer.close()
