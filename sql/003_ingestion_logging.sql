CREATE TABLE IF NOT EXISTS analytics.ingestion_log (
    ingestion_log_id BIGSERIAL PRIMARY KEY,
    pipeline_name VARCHAR(100) NOT NULL,
    symbol VARCHAR(20),
    interval_code VARCHAR(20) NOT NULL,
    request_start_date DATE,
    request_end_date DATE,
    row_count_fetched INTEGER NOT NULL DEFAULT 0,
    row_count_loaded INTEGER NOT NULL DEFAULT 0,
    status VARCHAR(30) NOT NULL,
    error_message TEXT,
    started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    finished_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_ingestion_log_lookup
    ON analytics.ingestion_log (pipeline_name, symbol, started_at DESC);