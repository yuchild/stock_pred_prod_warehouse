#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="/home/oem/Documents/github/stock_pred_prod_warehouse"
LOG_DIR="$PROJECT_DIR/logs"
TIMESTAMP="$(date '+%Y-%m-%d_%H-%M-%S')"

mkdir -p "$LOG_DIR"

cd "$PROJECT_DIR"
source .venv/bin/activate

make ingest-daily-incremental >> "$LOG_DIR/cron_ingest_$TIMESTAMP.log" 2>&1