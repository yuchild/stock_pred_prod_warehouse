SYMBOLS ?= SPY,QQQ,NVDA,AAPL,MSFT
PERIOD ?= 2y
INTERVAL ?= 1d
BACKFILL_DAYS ?= 10

.PHONY: test-db ingest-daily ingest-daily-incremental check-prices seed-symbols list-tables show-ingestion-log

test-db:
	python scripts/test_db_connection.py

seed-symbols:
	python scripts/seed_symbols.py

list-tables:
	python scripts/list_tables.py

ingest-daily:
	python scripts/ingest_daily_prices.py --symbols $(SYMBOLS) --period $(PERIOD) --interval $(INTERVAL)

ingest-daily-incremental:
	python scripts/ingest_daily_prices_incremental.py --symbols $(SYMBOLS) --interval $(INTERVAL) --backfill-days $(BACKFILL_DAYS)

check-prices:
	python scripts/check_price_history.py

show-ingestion-log:
	python scripts/show_ingestion_log.py