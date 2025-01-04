from kafka import KafkaProducer  # type: ignore
from kafka.admin import KafkaAdminClient, NewTopic  # type: ignore
import psycopg2  # type: ignore
import json
import sys
import time
import logging
import os

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

DATA_FOLDER_PATH = os.path.join(os.getcwd(), "game_data")

BROKER_SERVER = os.getenv("BROKER_SERVER")
POSTGRES_SERVER = os.getenv("POSTGRES_SERVER")

POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")


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


def store_cricket_game_data(game_id, game_info):
    try:
        conn = psycopg2.connect(
            host=POSTGRES_HOST, database=POSTGRES_DB, user=POSTGRES_USER, password=POSTGRES_PASSWORD)
        cursor = conn.cursor()

        insert_query = """
        INSERT INTO cricket_matches ( game_id, match_type, match_gender, match_date, 
        match_name, match_city, match_venue, team_a, team_b, players_a, players_b)
        VALUES (%(game_id)s, %(match_type)s, %(match_gender)s, %(match_date)s, %(match_name)s,
        %(match_city)s, %(match_venue)s, %(team_a)s, %(team_b)s, %(players_a)s::JSONB, %(players_b)s::JSONB)
        """
        insert_data = {
            "game_id": game_id,
            "match_type": game_info["match_type"],
            "match_gender": game_info["gender"],
            "match_date": game_info["dates"][0],
            "match_name": game_info["event"]["name"],
            "match_city": game_info["city"],
            "match_venue": game_info["venue"],
            "team_a": game_info["teams"][0],
            "team_b": game_info["teams"][1],
            "players_a": json.dumps(game_info["players"][game_info["teams"][0]]),
            "players_b": json.dumps(game_info["players"][game_info["teams"][1]])
        }
        cursor.execute(insert_query, insert_data)
        conn.commit()
        cursor.close()
        conn.close()
        logging.error(f"Successfully added to cricket_matches table: {insert_data}")
    except Exception as e:
        logging.error(f"Error during [{game_id}] db update: {e}")


def load_json_data(game_id):
    game_data = None
    try:
        file_path = os.path.join(DATA_FOLDER_PATH, f'{game_id}.json')
        with open(file_path, "r") as file:
            game_data = json.load(file)
        return game_data
    except Exception as e:
        logging.error(f"Error loading {game_id} game data: {e}")
        return []


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

        logging.info(f"[{game_id}] simulation completed.")
    except Exception as e:
        logging.error(f"Error during [{game_id}] simulation: {e}")


def run_cricket(producer, topic, game_id, game_step_time):
    try:
        game_data = load_json_data(game_id)
        store_cricket_game_data(game_id, game_data['info'])
        for inningIdx, inning in enumerate(game_data['innings']):
            for overIdx, over in enumerate(inning['overs']):
                for ballIdx, delivery in enumerate(over['deliveries']):
                    message = {
                        'game_id': game_id,
                        'inning': inningIdx+1,
                        'team': inning['team'],
                        'over': overIdx,
                        'ball': ballIdx+1,
                        'delivery': delivery,
                        'timestamp': time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
                    }
                    producer.send(topic, key=game_id, value=message)
                    logging.info(f"Published message: {message}")
                    time.sleep(game_step_time)

        logging.info(f"[{game_id}] simulation completed.")
    except Exception as e:
        logging.error(f"Error during [{game_id}] simulation: {e}")


def game_setup(topic, game_id, game_step_time, game_duration):
    admin_client = None
    producer = None
    try:
        admin_client = KafkaAdminClient(
            bootstrap_servers=BROKER_SERVER, client_id=f'{game_id}_game_simulator')
        create_topic_if_not_exists(admin_client, topic)
        producer = KafkaProducer(bootstrap_servers=BROKER_SERVER,
                                 key_serializer=str.encode,
                                 value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        logging.info(f"Starting [{game_id}] simulation.")

        if topic == 'cricket':
            run_cricket(producer, topic, game_id, game_step_time)
        else:
            run_game(producer, topic, game_id, game_step_time, game_duration)
    except Exception as e:
        logging.error(
            f"Error during [{game_id}] game setup: {e}")
    finally:
        if producer:
            producer.close()
        if admin_client:
            admin_client.close()


if __name__ == "__main__":
    if len(sys.argv) < 5:
        logging.error(
            "Usage: python script.py <topic> <game_id> <game_step_time> <game_duration>")
        sys.exit(1)

    topic = sys.argv[1]
    game_id = sys.argv[2]
    try:
        game_step_time = float(sys.argv[3])
        game_duration = float(sys.argv[4])
    except ValueError:
        logging.error("game_step_time, game_duration must be a numeric value.")
        sys.exit(1)

    game_setup(topic, game_id, game_step_time, game_duration)
