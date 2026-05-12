-- ============================================================
-- USIU Akinator — Supabase Setup
-- Run all of this in: Supabase Dashboard → SQL Editor → New Query
-- ============================================================


-- 1. Learning data table
--    Stores the Bayesian counts per (attr, response) pair.
--    This is what the model actually learns from.
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS learning_data (
    key      TEXT PRIMARY KEY,        -- e.g. "coding|Definitely Yes"
    success  INTEGER NOT NULL DEFAULT 0,
    trials   INTEGER NOT NULL DEFAULT 0,
    updated_at TIMESTAMPTZ DEFAULT NOW()
);


-- 2. Game log table
--    Every completed game is stored here for analytics.
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS game_log (
    id          BIGSERIAL PRIMARY KEY,
    type        TEXT,                 -- "SUCCESS" or "FAIL"
    guess       TEXT,                 -- what the model guessed
    correct     TEXT,                 -- what the correct programme was
    confidence  INTEGER,              -- confidence % at time of guess
    n_questions INTEGER,              -- how many questions were asked
    path        TEXT,                 -- JSON array of [attr, response] pairs
    created_at  TIMESTAMPTZ DEFAULT NOW()
);


-- 3. Atomic increment function
--    Prevents race conditions when two games finish simultaneously.
--    Instead of read-modify-write, this runs entirely inside Postgres.
-- ------------------------------------------------------------
CREATE OR REPLACE FUNCTION increment_learning(
    p_key           TEXT,
    p_delta_success INTEGER,
    p_delta_trials  INTEGER
)
RETURNS VOID AS $$
BEGIN
    INSERT INTO learning_data (key, success, trials)
        VALUES (p_key, p_delta_success, p_delta_trials)
    ON CONFLICT (key) DO UPDATE
        SET success    = learning_data.success + EXCLUDED.success,
            trials     = learning_data.trials  + EXCLUDED.trials,
            updated_at = NOW();
END;
$$ LANGUAGE plpgsql;


-- 4. Row Level Security (RLS)
--    Allow the anon key to read AND write both tables.
--    (The app uses the anon key — it never exposes the service_role key)
-- ------------------------------------------------------------
ALTER TABLE learning_data ENABLE ROW LEVEL SECURITY;
ALTER TABLE game_log      ENABLE ROW LEVEL SECURITY;

-- Learning data: anyone can read and upsert
CREATE POLICY "allow_read_learning"  ON learning_data FOR SELECT USING (true);
CREATE POLICY "allow_write_learning" ON learning_data FOR INSERT WITH CHECK (true);
CREATE POLICY "allow_update_learning" ON learning_data FOR UPDATE USING (true);

-- Game log: anyone can insert and read
CREATE POLICY "allow_read_game_log"   ON game_log FOR SELECT USING (true);
CREATE POLICY "allow_insert_game_log" ON game_log FOR INSERT WITH CHECK (true);


-- ============================================================
-- Done! You can verify the tables were created with:
--   SELECT * FROM learning_data LIMIT 5;
--   SELECT * FROM game_log      LIMIT 5;
-- ============================================================
