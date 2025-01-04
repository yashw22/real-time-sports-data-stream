from kafka import KafkaProducer  # type: ignore
from kafka.admin import KafkaAdminClient, NewTopic  # type: ignore
import json
import sys
import time
import logging

BOOTSTRAP_SERVER = None

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)


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


def run_game(producer, topic, game_id, game_step_time, game_duration):
    try:
        start_time = time.time()

        idx = 0
        while time.time() - start_time < game_duration:
            idx += 1
            message = {"game_id": game_id, "count": idx, "timestamp": time.strftime(
                "%Y-%m-%d %H:%M:%S", time.gmtime()), }
            producer.send(topic, value=message)
            logging.info(f"Published message: {message}")
            time.sleep(game_step_time)

        logging.info(f"Simulation for {game_id} completed.")
    except Exception as e:
        logging.error(
            f"Error occurred during simulation for game {game_id}: {e}")


def game_setup(topic, game_id, game_step_time, game_duration):
    admin_client = None
    producer = None
    try:
        admin_client = KafkaAdminClient(
            bootstrap_servers=BOOTSTRAP_SERVER, client_id=f'{game_id}_game_simulator')
        create_topic_if_not_exists(admin_client, topic)
        producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVER,
                                 value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        logging.info(f"Starting simulation for game: {game_id}")
        run_game(producer, topic, game_id, game_step_time, game_duration)
    except Exception as e:
        logging.error(
            f"Error occurred during setup for game {game_id}: {e}")
    finally:
        if producer:
            producer.close()
        if admin_client:
            admin_client.close()


if __name__ == "__main__":
    if len(sys.argv) < 6:
        logging.error(
            "Usage: python script.py <bootstrap_server> <topic> <game_id> <game_step_time> <game_duration>")
        sys.exit(1)

    BOOTSTRAP_SERVER = sys.argv[1]
    topic = sys.argv[2]
    game_id = sys.argv[3]
    try:
        game_step_time = float(sys.argv[4])
        game_duration = float(sys.argv[5])
    except ValueError:
        logging.error("game_step_time, game_duration must be a numeric value.")
        sys.exit(1)

    game_setup(topic, game_id, game_step_time, game_duration)
