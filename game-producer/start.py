import subprocess
import logging
import time

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
    ]
)

def main():
    matches = ["match-1", "match-2", "match-3"]
    # matches = ["match-1"]
    processes = []

    logging.info("Starting match simulations...")

    try:
        for match in matches:
            process = subprocess.Popen(
                ["python", "game_sim.py", match])
            processes.append((match, process))
            time.sleep(5)

        for match, process in processes:
            process.wait()

    except Exception as e:
        logging.error(f"An error occurred while running simulations: {e}")

    logging.info("All simulations have completed.")


if __name__ == "__main__":
    main()
