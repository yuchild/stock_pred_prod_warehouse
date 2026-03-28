CREATE TABLE IF NOT EXISTS mart.dim_symbol (
    symbol_id BIGSERIAL PRIMARY KEY,
    symbol VARCHAR(20) NOT NULL UNIQUE,
    asset_type VARCHAR(20),
    exchange VARCHAR(50),
    currency VARCHAR(10) DEFAULT 'USD',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS raw.stock_price_daily (
    price_id BIGSERIAL PRIMARY KEY,
    symbol VARCHAR(20) NOT NULL,
    trade_date DATE NOT NULL,
    open_price NUMERIC(18,6),
    high_price NUMERIC(18,6),
    low_price NUMERIC(18,6),
    close_price NUMERIC(18,6),
    adj_close_price NUMERIC(18,6),
    volume BIGINT,
    data_source VARCHAR(50) DEFAULT 'yfinance',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (symbol, trade_date)
);

CREATE INDEX IF NOT EXISTS idx_stock_price_daily_symbol_date
    ON raw.stock_price_daily (symbol, trade_date DESC);

CREATE TABLE IF NOT EXISTS ml.model_run (
    model_run_id BIGSERIAL PRIMARY KEY,
    model_name VARCHAR(100) NOT NULL,
    model_version VARCHAR(50),
    interval_code VARCHAR(20) NOT NULL,
    target_name VARCHAR(100),
    train_start_date DATE,
    train_end_date DATE,
    prediction_as_of_date DATE,
    training_row_count BIGINT,
    test_row_count BIGINT,
    feature_count BIGINT,
    metric_primary_name VARCHAR(100),
    metric_primary_value NUMERIC(18,6),
    model_artifact_path TEXT,
    run_status VARCHAR(30) NOT NULL DEFAULT 'SUCCESS',
    notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_model_run_lookup
    ON ml.model_run (model_name, interval_code, created_at DESC);

CREATE TABLE IF NOT EXISTS ml.prediction_output (
    prediction_id BIGSERIAL PRIMARY KEY,
    model_run_id BIGINT NOT NULL REFERENCES ml.model_run(model_run_id),
    symbol VARCHAR(20) NOT NULL,
    interval_code VARCHAR(20) NOT NULL,
    as_of_timestamp TIMESTAMPTZ NOT NULL,
    prediction_date DATE,
    predicted_class VARCHAR(50),
    predicted_label VARCHAR(50),
    probability_up NUMERIC(12,8),
    probability_down NUMERIC(12,8),
    probability_no_change NUMERIC(12,8),
    forecast_return NUMERIC(18,8),
    forecast_close NUMERIC(18,6),
    current_close NUMERIC(18,6),
    stop_loss NUMERIC(18,6),
    take_profit NUMERIC(18,6),
    shares_suggested INTEGER,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_prediction_output_symbol_time
    ON ml.prediction_output (symbol, as_of_timestamp DESC);