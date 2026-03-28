# stock_pred_prod_warehouse

Local-first stock prediction production warehouse.

## Goals
- Infrastructure-as-code in GitHub
- Local Linux machine runs:
  - PostgreSQL
  - cron jobs
  - Airflow
  - Streamlit
  - Jupyter notebooks
- Modular code for ingestion, feature engineering, training, prediction, and forecasting
- Scalable to additional Linux hardware

## High-level architecture
- `src/` reusable Python modules
- `sql/` warehouse DDL and views
- `airflow/` orchestration DAGs
- `streamlit_app/` dashboard app
- `notebooks/` analysis and presentation notebooks
- `scripts/` operational entry points
- `infra/` cron/systemd deployment files

## Initial setup
Project bootstrap in progress.
