from kafka import KafkaProducer # type: ignore
import json
import sys
import time
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
    ]
)


def main():
    game_id = sys.argv[1]
    topic = "cricket"
    logging.info(f"Starting simulation for game: {game_id}")

    try:
        producer = KafkaProducer(bootstrap_servers='broker:9092',
                                 value_serializer=lambda v: json.dumps(v).encode('utf-8'))

        start_time = time.time()
        duration = 5 * 60

        idx = 0
        while time.time() - start_time < duration:
            idx += 1
            message = {
                "game_id": game_id,
                "count": idx,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
            }
            producer.send(topic, message)
            logging.info(f"Published message: {message}")
            time.sleep(20)
    except Exception as e:
        logging.error(
            f"Error occurred during simulation for game {game_id}: {e}")
    finally:
        if 'producer' in locals():
            producer.close()
        logging.info(f"Simulation for {game_id} completed.")


if __name__ == "__main__":
    main()
