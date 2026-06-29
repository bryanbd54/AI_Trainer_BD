-- AI Trainer BD — PostgreSQL Schema
-- Run this once against your Railway database to initialize all tables.

CREATE TABLE IF NOT EXISTS users (
    username    TEXT PRIMARY KEY,
    xp          INTEGER NOT NULL DEFAULT 0,
    level       INTEGER NOT NULL DEFAULT 1,
    created_at  TIMESTAMP NOT NULL DEFAULT NOW(),
    last_active TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS submissions (
    id           SERIAL PRIMARY KEY,
    username     TEXT NOT NULL REFERENCES users(username),
    challenge_id TEXT NOT NULL,
    prompt       TEXT NOT NULL,
    response     TEXT NOT NULL,
    score        INTEGER NOT NULL,
    xp_earned    INTEGER NOT NULL,
    feedback     TEXT,
    created_at   TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS user_badges (
    id         SERIAL PRIMARY KEY,
    username   TEXT NOT NULL REFERENCES users(username),
    badge_id   TEXT NOT NULL,
    earned_at  TIMESTAMP NOT NULL DEFAULT NOW(),
    UNIQUE (username, badge_id)
);

-- Indexes to speed up the leaderboard and history queries
CREATE INDEX IF NOT EXISTS idx_submissions_username        ON submissions(username);
CREATE INDEX IF NOT EXISTS idx_submissions_challenge_id   ON submissions(challenge_id);
CREATE INDEX IF NOT EXISTS idx_user_badges_username       ON user_badges(username);
