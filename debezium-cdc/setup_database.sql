-- Database setup script for Debezium CDC Demo
-- Run this script in PostgreSQL to create the required tables

-- Create games table
CREATE TABLE IF NOT EXISTS games (
    game_id SERIAL PRIMARY KEY,
    sport VARCHAR(50) NOT NULL,
    league VARCHAR(50) NOT NULL,
    home_team VARCHAR(100) NOT NULL,
    away_team VARCHAR(100) NOT NULL,
    commence_time TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create odds_history table
CREATE TABLE IF NOT EXISTS odds_history (
    id SERIAL PRIMARY KEY,
    game_id INTEGER NOT NULL REFERENCES games(game_id),
    bookmaker VARCHAR(50) NOT NULL,
    market VARCHAR(50) NOT NULL,
    outcome VARCHAR(50) NOT NULL,
    price DECIMAL(5,2) NOT NULL,
    fetched_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_odds_history_game_id ON odds_history(game_id);
CREATE INDEX IF NOT EXISTS idx_odds_history_fetched_at ON odds_history(fetched_at);
CREATE INDEX IF NOT EXISTS idx_odds_history_bookmaker ON odds_history(bookmaker);
CREATE INDEX IF NOT EXISTS idx_games_sport ON games(sport);
CREATE INDEX IF NOT EXISTS idx_games_commence_time ON games(commence_time);

-- Enable logical replication (required for Debezium)
-- Note: This typically requires superuser privileges
-- ALTER SYSTEM SET wal_level = logical;
-- ALTER SYSTEM SET max_replication_slots = 10;
-- ALTER SYSTEM SET max_wal_senders = 10;

-- Grant necessary permissions for the Debezium user
GRANT SELECT ON ALL TABLES IN SCHEMA public TO admin;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO admin;

-- Show table structure
\d games;
\d odds_history;

COMMENT ON TABLE games IS 'Sports games with teams and scheduled times';
COMMENT ON TABLE odds_history IS 'Historical odds data from various bookmakers';
COMMENT ON COLUMN odds_history.market IS 'Type of bet: moneyline, spread, total';
COMMENT ON COLUMN odds_history.outcome IS 'Specific outcome: home, away, over, under';
COMMENT ON COLUMN odds_history.price IS 'Decimal odds price'; 