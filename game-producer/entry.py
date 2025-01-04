import os
import logging
import subprocess
import time
import json
import random

from postgres_api import register_cricket_match

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
                register_cricket_match(
                    game_id, json.load(file)['info'], curr_offset_secs)
            curr_offset_secs += offset_secs
    return games


def start_game_subprocesses():
    # topic = 'cricket'
    # games = ["game-1", "game-2", "game-3"]
    games = load_games(60)
    new_game_offset_time = 60
    game_step_time = new_game_offset_time*(1+len(games))
    game_duration = 5*60
    print(games)

    processes = []
    try:
        for topic, game_id in games:
            process = subprocess.Popen(
                ["python", "game_sim.py", topic, game_id, str(game_step_time), str(game_duration)])
            processes.append((game_id, process))
            time.sleep(new_game_offset_time)

        for _, process in processes:
            process.wait()

        logging.info("All game simulations have completed.")
    except Exception as e:
        logging.error(f"Error while running game simulations: {e}")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.StreamHandler()]
    )
    logging.info("Starting game simulations...")
    start_game_subprocesses()
