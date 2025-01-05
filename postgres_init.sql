CREATE TABLE IF NOT EXISTS live_match (
    id SERIAL PRIMARY KEY,
    topic VARCHAR(32) NOT NULL,
    game_id VARCHAR(32) UNIQUE NOT NULL,
    starts_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS cricket_match (
    id SERIAL PRIMARY KEY,
    game_id VARCHAR(32) NOT NULL,
    FOREIGN KEY (game_id)  REFERENCES live_match (game_id),
    match_type VARCHAR(16) NOT NULL,
    match_gender varchar(16) NOT NULL,
    match_date VARCHAR(16) NOT NULL,
    match_name  varchar(255) NOT NULL,
    match_city varchar(64) NOT NULL,
    match_venue varchar(255) NOT NULL,
    team_a varchar(32) NOT NULL,
    team_b varchar(32) NOT NULL,
    players_a JSONB NOT NULL,
    players_b JSONB NOT NULL,
    starts_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
