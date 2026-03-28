SYMBOLS ?= SPY,QQQ,NVDA,AAPL,MSFT
PERIOD ?= 2y
INTERVAL ?= 1d

.PHONY: test-db ingest-daily check-prices seed-symbols list-tables

test-db:
	python scripts/test_db_connection.py

seed-symbols:
	python scripts/seed_symbols.py

list-tables:
	python scripts/list_tables.py

ingest-daily:
	python scripts/ingest_daily_prices.py --symbols $(SYMBOLS) --period $(PERIOD) --interval $(INTERVAL)

check-prices:
	python scripts/check_price_history.py