import json

from postgres_ops import register_cricket_ball_event, update_cricket_match_state

games_state = {}


def process_cricket_ball_event(data):
    game_id = data['game_id']
    if game_id not in games_state:
        games_state[game_id] = {
            'game_id': game_id,
            'inning': data['inning'],
            'team': data['team'],
            'total_runs': 0,
            'balls_bowled': 0,
            'extras': 0,
            'batters_stats': {},  # {batter_name: {'runs': 0, 'balls': 0}}
            'bowlers_stats': {},  # {bowler_name: {'overs': 0, 'runs': 0, 'wickets': 0}}
            'wickets': 0,
            'on_strike': None,
            'non_striker': None,
            'partnership_runs': 0,
            'overs_bowled': 0,
            'current_run_rate': 0,
        }

    match_state = games_state[game_id]

    # Process ball
    runs = data['delivery']['runs']['total']
    batter_runs = data['delivery']['runs']['total']
    extras = data['delivery']['runs']['extras']
    batter = data['delivery']['batter']
    bowler = data['delivery']['bowler']

    match_state['total_runs'] += runs
    match_state['extras'] += extras
    match_state['balls_bowled'] += 1
    match_state['batters_stats'].setdefault(batter, {'runs': 0, 'balls': 0})
    match_state['bowlers_stats'].setdefault(
        bowler, {'overs': 0, 'runs': 0, 'wickets': 0})

    match_state['batters_stats'][batter]['runs'] += batter_runs
    match_state['batters_stats'][batter]['balls'] += 1
    match_state['bowlers_stats'][bowler]['runs'] += runs
    bowler_balls = match_state['bowlers_stats'][bowler]['overs'] + 1
    match_state['bowlers_stats'][bowler]['overs'] += bowler_balls // 6 + \
        (bowler_balls % 6) / 10

    if 'wickets' in data['delivery']:
        match_state['wickets'] += 1
        match_state['bowlers_stats'][bowler]['wickets'] += 1

    match_state['on_strike'], match_state['non_striker'] = data['delivery']['batter'], data['delivery']['non_striker']
    if batter_runs in [1, 3]:
        match_state['on_strike'], match_state['non_striker'] = match_state['non_striker'], match_state['on_strike']
    if data['ball'] == 6:
        match_state['on_strike'], match_state['non_striker'] = match_state['non_striker'], match_state['on_strike']

    match_state['partnership_runs'] += runs

    overs_bowled = match_state['balls_bowled'] // 6 + \
        (match_state['balls_bowled'] % 6) / 10
    crr = match_state['total_runs'] / overs_bowled if overs_bowled > 0 else 0

    match_state['overs_bowled'] = overs_bowled
    match_state['current_run_rate'] = round(crr, 2)

    games_state[game_id] = match_state


def consume_cricket_data(message):
    register_cricket_ball_event(message)
    process_cricket_ball_event(message)
    update_cricket_match_state(games_state[message['game_id']])
