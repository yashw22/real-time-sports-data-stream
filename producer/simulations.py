import time
import logging
import json
import os

DATA_FOLDER_PATH = os.path.join(os.getcwd(), "game_data")


def run_game_sim(producer, topic, game_id, game_step_time):
    game_duration = 5*60
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


def load_cricket_data(game_id):
    game_data = None
    try:
        file_path = os.path.join(DATA_FOLDER_PATH, f'{game_id}.json')
        with open(file_path, "r") as file:
            game_data = json.load(file)
        return game_data
    except Exception as e:
        logging.error(f"Error loading {game_id} game data: {e}")
        return []


def run_cricket_sim(producer, topic, game_id, game_step_time):
    try:
        game_data = load_cricket_data(game_id)
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
