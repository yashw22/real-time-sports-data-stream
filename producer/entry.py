import os
import logging
import time
import json
import random
import concurrent.futures

from producer import setup_producer
from postgres_ops import register_live_match, register_cricket_match

DATA_FOLDER_PATH = os.path.join(os.getcwd(), "game_data")


def load_games(offset_secs):
    games = []
    curr_offset_secs = 0
    file_list = os.listdir(DATA_FOLDER_PATH)
    random.seed(42)
    random.shuffle(file_list)
    for filename in file_list:
        if filename.endswith(".json"):
            game_id = filename.replace(".json", "")
            topic = game_id.split("_")[0]
            games.append((topic, game_id))
            file_path = os.path.join(DATA_FOLDER_PATH, f'{game_id}.json')
            with open(file_path, "r") as file:
                register_live_match(topic, game_id, curr_offset_secs)
                register_cricket_match(
                    game_id, json.load(file)['info'], curr_offset_secs)
            curr_offset_secs += offset_secs
    return games


def create_producers():
    new_game_offset_time = 2
    games = load_games(offset_secs=2)
    game_step_time = new_game_offset_time*(1+len(games))

    processes = []
    try:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for topic, game_id in games:
                futures.append(executor.submit(setup_producer, topic, game_id, game_step_time))
                time.sleep(new_game_offset_time)
            for future in futures:
                future.result()

        logging.info("All game simulations have completed.")
    except Exception as e:
        logging.error(f"Error while running game simulations: {e}")

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.FileHandler("producer.log"),
                  logging.StreamHandler()]
    )
    logging.info("Starting game simulations...")
    create_producers()
