import logging
import subprocess
import time
import sys
import os
import json

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

DATA_FOLDER_PATH = os.path.join(os.getcwd(), "game_data")

def load_games():
    games = []
    for filename in os.listdir(DATA_FOLDER_PATH):
        if filename.endswith(".json"):
            game_id = filename.replace(".json", "")
            games.append((game_id.split("_")[0], game_id))
    return games

def start_game_subprocesses():
    # topic = 'cricket'
    # games = ["game-1", "game-2", "game-3"]
    # games = ["game-1"]
    games = load_games()
    new_game_offset_time = 2
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
    logging.info("Starting game simulations...")
    start_game_subprocesses()
