-- ── Schema verification for Claude AI Trainer ───────────────────────────────
-- Run this in Railway's Postgres console (or any psql session connected to prod)
-- A healthy schema returns no rows from each "MISSING" check.

-- ── 1. Tables that must exist ─────────────────────────────────────────────────
SELECT 'MISSING TABLE: ' || t AS issue
FROM unnest(ARRAY['users','user_badges','submissions']) AS t
WHERE t NOT IN (
    SELECT table_name FROM information_schema.tables
    WHERE table_schema = 'public'
);

-- ── 2. users columns ──────────────────────────────────────────────────────────
-- Required: username, email, password_hash, display_name, xp, level,
--           created_at, last_active
SELECT 'MISSING COLUMN: users.' || c AS issue
FROM unnest(ARRAY[
    'username','email','password_hash','display_name',
    'xp','level','created_at','last_active'
]) AS c
WHERE c NOT IN (
    SELECT column_name FROM information_schema.columns
    WHERE table_schema = 'public' AND table_name = 'users'
);

-- ── 3. user_badges columns ────────────────────────────────────────────────────
-- Required: username, badge_id, earned_at
SELECT 'MISSING COLUMN: user_badges.' || c AS issue
FROM unnest(ARRAY['username','badge_id','earned_at']) AS c
WHERE c NOT IN (
    SELECT column_name FROM information_schema.columns
    WHERE table_schema = 'public' AND table_name = 'user_badges'
);

-- ── 4. submissions columns ────────────────────────────────────────────────────
-- Required: id, username, challenge_id, prompt, response,
--           score, xp_earned, feedback, created_at
SELECT 'MISSING COLUMN: submissions.' || c AS issue
FROM unnest(ARRAY[
    'id','username','challenge_id','prompt','response',
    'score','xp_earned','feedback','created_at'
]) AS c
WHERE c NOT IN (
    SELECT column_name FROM information_schema.columns
    WHERE table_schema = 'public' AND table_name = 'submissions'
);

-- ── 5. Unique constraints on users ───────────────────────────────────────────
-- username and email both need UNIQUE constraints for the 409 duplicate check
SELECT 'MISSING UNIQUE on users(' || required.col || ')' AS issue
FROM (VALUES ('username'), ('email')) AS required(col)
WHERE required.col NOT IN (
    SELECT a.attname
    FROM pg_index i
    JOIN pg_attribute a ON a.attrelid = i.indrelid AND a.attnum = ANY(i.indkey)
    JOIN pg_class c ON c.oid = i.indrelid
    WHERE c.relname = 'users' AND i.indisunique AND i.indnkeyatts = 1
);

-- ── 6. Full column detail for each table (informational) ──────────────────────
SELECT table_name, column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_schema = 'public'
  AND table_name IN ('users', 'user_badges', 'submissions')
ORDER BY table_name, ordinal_position;
