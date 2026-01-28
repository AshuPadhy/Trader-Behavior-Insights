Place the two input files into data/raw/ with the filenames:
- hyperliquid_history.csv
- fear_greed.csv

If the Drive links are public, run:
    python src/data_ingest.py --download "<HYPERLIQUID_DRIVE_URL>" "<FEARGREED_DRIVE_URL>"

Otherwise, place files manually and run:
    python src/data_ingest.py --local

Expected behavior:
- The script will read data/raw/hyperliquid_history.csv and data/raw/fear_greed.csv,
  produce a small schema & data-quality report at outputs/schema_report.md, and
  save processed Parquet files to data/processed/.