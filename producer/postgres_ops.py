import psycopg2  # type: ignore
import logging
import json
import os
from datetime import datetime, timedelta

POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")


def execute_query(query, data, oper):
    conn = None
    try:
        conn = psycopg2.connect(
            host=POSTGRES_HOST, database=POSTGRES_DB, user=POSTGRES_USER, password=POSTGRES_PASSWORD)

        with conn.cursor() as cursor:
            cursor.execute(query, data)
            conn.commit()
        logging.info(f"[{oper}] operation completed.")
    except Exception as e:
        logging.error(f"Error during [{oper}] operation: {e}")
    finally:
        if conn:
            conn.close()


def register_live_match(topic, game_id, offset_seconds):
    insert_query = """
    INSERT INTO live_match ( topic, game_id, starts_at)
    VALUES (%(topic)s, %(game_id)s, %(starts_at)s)
    """
    insert_data = {
        "topic": topic,
        "game_id": game_id,
        "starts_at": datetime.now() + timedelta(seconds=offset_seconds),
    }
    execute_query(insert_query, insert_data, f"create ({topic}, {game_id}) live match" )


def register_cricket_match(game_id, game_info, offset_seconds):
    insert_query = """
    INSERT INTO cricket_match ( game_id, match_type, match_gender, match_date, 
    match_name, match_city, match_venue, team_a, team_b, players_a, players_b, starts_at)
    VALUES (%(game_id)s, %(match_type)s, %(match_gender)s, %(match_date)s, %(match_name)s,
    %(match_city)s, %(match_venue)s, %(team_a)s, %(team_b)s, %(players_a)s::JSONB, %(players_b)s::JSONB, %(starts_at)s)
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
        "players_b": json.dumps(game_info["players"][game_info["teams"][1]]),
        "starts_at": datetime.now() + timedelta(seconds=offset_seconds),
    }
    execute_query(insert_query, insert_data, f"create (cricket, {game_id}) cricket match")
