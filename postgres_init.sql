CREATE TABLE IF NOT EXISTS cricket_matches (
    id SERIAL PRIMARY KEY,
    game_id VARCHAR(32) NOT NULL,
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
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);