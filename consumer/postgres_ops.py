import psycopg2  # type: ignore
import logging
import json
import os

POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")


def execute_query(query, data=None, fetch_results=False, oper=None):
    conn = None
    try:
        conn = psycopg2.connect(
            host=POSTGRES_HOST, database=POSTGRES_DB, user=POSTGRES_USER, password=POSTGRES_PASSWORD)

        with conn.cursor() as cursor:
            cursor.execute(query, data)
            if fetch_results:
                return cursor.fetchall()
            conn.commit()
        logging.info(f"[{oper}] operation completed.")
    except Exception as e:
        logging.error(f"Error during [{oper}] operation: {e}")
    finally:
        if conn:
            conn.close()


def fetch_all_live_match():
    query = "SELECT * FROM live_match"
    results = execute_query(query, fetch_results=True,
                            oper="fetch_all_live_match")
    if results:
        return results
    else:
        logging.info("No live matches found.")
        return []


def register_cricket_ball_event(data):
    insert_query = """
    INSERT INTO cricket_ball_event ( game_id, inning, team, over, ball, delivery )
    VALUES (%(game_id)s, %(inning)s, %(team)s, %(over)s, %(ball)s, %(delivery)s::JSONB)
    """

    query_data =  dict(data)
    query_data['delivery'] = json.dumps(query_data['delivery'])

    execute_query(insert_query, query_data,
                  oper=f"insert ({query_data['game_id']}) ball event")


def update_cricket_match_state(match_state):
    query = """
    INSERT INTO cricket_match_state (
        game_id, inning, team, total_runs, balls_bowled, extras,
        batters_stats, bowlers_stats, wickets, on_strike,
        non_striker, partnership_runs, overs_bowled, current_run_rate 
    ) VALUES (
        %(game_id)s, %(inning)s, %(team)s, %(total_runs)s, %(balls_bowled)s, %(extras)s,
        %(batters_stats)s::JSONB, %(bowlers_stats)s::JSONB, %(wickets)s, %(on_strike)s,
        %(non_striker)s, %(partnership_runs)s, %(overs_bowled)s, %(current_run_rate)s 
    )
    ON CONFLICT (game_id) DO UPDATE SET
        inning = EXCLUDED.inning,
        team = EXCLUDED.team,
        total_runs = EXCLUDED.total_runs,
        balls_bowled = EXCLUDED.balls_bowled,
        extras = EXCLUDED.extras,
        batters_stats = EXCLUDED.batters_stats,
        bowlers_stats = EXCLUDED.bowlers_stats,
        wickets = EXCLUDED.wickets,
        on_strike = EXCLUDED.on_strike,
        non_striker = EXCLUDED.non_striker,
        partnership_runs = EXCLUDED.partnership_runs,
        overs_bowled = EXCLUDED.overs_bowled,
        current_run_rate = EXCLUDED.current_run_rate
    """

    data = dict(match_state)
    data['batters_stats'] = json.dumps(data['batters_stats'])
    data['bowlers_stats'] = json.dumps(data['bowlers_stats'])

    execute_query(query, data,
                  oper=f"update ({data['game_id']}) match state")
