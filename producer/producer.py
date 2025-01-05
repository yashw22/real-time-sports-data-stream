from kafka import KafkaProducer  # type: ignore
from kafka.admin import KafkaAdminClient, NewTopic  # type: ignore
import json
import logging
import os

from simulations import run_cricket_sim, run_game_sim

BROKER_SERVER = os.getenv("BROKER_SERVER")

def create_topic_if_not_exists(admin_client, topic, partitions=1, replication_factor=1):
    try:
        existing_topics = admin_client.list_topics()
        if topic not in existing_topics:
            new_topic = NewTopic(
                name=topic, num_partitions=partitions, replication_factor=replication_factor)
            admin_client.create_topics([new_topic])
            logging.info(f"Created topic: {topic}")
        else:
            logging.info(f"Topic {topic} already exists.")
    except Exception as e:
        logging.error(f"Error while creating topic {topic}: {e}")

def setup_producer(topic, game_id, game_step_time):
    admin_client = None
    producer = None
    try:
        admin_client = KafkaAdminClient(
            bootstrap_servers=BROKER_SERVER, client_id=f'{game_id}_game_simulator')
        create_topic_if_not_exists(admin_client, topic)
        producer = KafkaProducer(bootstrap_servers=BROKER_SERVER, key_serializer=str.encode,
                                 value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        logging.info(f"Starting [{game_id}] simulation.")

        if topic == 'cricket':
            run_cricket_sim(producer, topic, game_id, game_step_time)
        else:
            run_game_sim(producer, topic, game_id, game_step_time)
        
    except Exception as e:
        logging.error(
            f"Error during [{game_id}] game setup: {e}")
    finally:
        if producer:
            producer.close()
        if admin_client:
            admin_client.close()
