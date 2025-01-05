import concurrent.futures
import logging

from postgres_ops import fetch_all_live_match
from consumer import setup_consumer

def start_consumers():
    games = fetch_all_live_match()
    games = [(match[1], match[2]) for match in games]

    try:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for topic, game_id in games:
                futures.append(executor.submit(setup_consumer, topic, game_id))
            for future in futures:
                future.result()

    except Exception as e:
        logging.error(f"Error while starting consumers: {e}")

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.FileHandler("consumer.log"),
                  logging.StreamHandler()]
    )
    logging.info("Starting consumers...")
    start_consumers()
