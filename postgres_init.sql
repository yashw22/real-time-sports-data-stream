CREATE TABLE IF NOT EXISTS live_match (
    id SERIAL PRIMARY KEY,
    topic VARCHAR(32) NOT NULL,
    game_id VARCHAR(32) UNIQUE NOT NULL,
    starts_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS cricket_match (
    id SERIAL PRIMARY KEY,
    game_id VARCHAR(32) UNIQUE NOT NULL,
    FOREIGN KEY (game_id)  REFERENCES live_match (game_id),
    match_type VARCHAR(16) NOT NULL,
    match_gender varchar(16) NOT NULL,
    match_date VARCHAR(16) NOT NULL,
    match_name  VARCHAR(255) NOT NULL,
    match_city VARCHAR(64) NOT NULL,
    match_venue VARCHAR(255) NOT NULL,
    team_a VARCHAR(32) NOT NULL,
    team_b VARCHAR(32) NOT NULL,
    players_a JSONB NOT NULL,
    players_b JSONB NOT NULL,
    starts_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS cricket_ball_event (
    id SERIAL PRIMARY KEY,
    game_id VARCHAR(32) NOT NULL,
    FOREIGN KEY (game_id)  REFERENCES cricket_match (game_id) ON DELETE CASCADE,
    inning INT NOT NULL,
    team VARCHAR(32) NOT NULL,
    "over" INT NOT NULL,
    ball INT NOT NULL,
    delivery JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS cricket_match_state (
    id SERIAL PRIMARY KEY,
    game_id VARCHAR(32) UNIQUE NOT NULL,
    FOREIGN KEY (game_id) REFERENCES cricket_match (game_id) ON DELETE CASCADE,
    inning INT NOT NULL,
    team VARCHAR(32) NOT NULL,
    total_runs INT NOT NULL,
    balls_bowled INT NOT NULL,
    extras INT NOT NULL,
    batters_stats JSONB,
    bowlers_stats JSONB,
    wickets INT NOT NULL,
    on_strike VARCHAR(64),
    non_striker VARCHAR(64),
    partnership_runs INT NOT NULL,
    overs_bowled FLOAT NOT NULL,
    current_run_rate FLOAT NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER set_updated_at
BEFORE UPDATE ON cricket_match_state
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();
