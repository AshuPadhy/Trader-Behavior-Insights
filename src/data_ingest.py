#!/usr/bin/env python3
"""Simple data ingestion helper for the Trader-Behavior-Insights scaffold.

Usage:
  python src/data_ingest.py --local
  python src/data_ingest.py --download <hyperliquid_drive_url> <feargreed_drive_url>

The script does not commit data to the repo. It writes processed files to data/processed/ and
an outputs/schema_report.md file with basic stats.
"""

import argparse
import os
import pandas as pd
from pathlib import Path

OUT_DIR = Path("data/processed")
RAW_DIR = Path("data/raw")
OUT_DIR.mkdir(parents=True, exist_ok=True)

def download_from_gdrive(hyper_url, fear_url):
    try:
        import gdown
    except Exception:
        raise SystemExit("Please install gdown (pip install gdown) to use --download")
    h_out = RAW_DIR / "hyperliquid_history.csv"
    f_out = RAW_DIR / "fear_greed.csv"
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Downloading hyperliquid -> {h_out}")
    gdown.download(hyper_url, str(h_out), quiet=False)
    print(f"Downloading fear_greed -> {f_out}")
    gdown.download(fear_url, str(f_out), quiet=False)
    return h_out, f_out

def read_local():
    h = RAW_DIR / "hyperliquid_history.csv"
    f = RAW_DIR / "fear_greed.csv"
    if not h.exists() or not f.exists():
        raise FileNotFoundError("Expected files not found in data/raw/. See data/README.md")
    return h, f

def simple_schema_report(h_path, f_path):
    reports = []
    # hyperliquid
    dfh = pd.read_csv(h_path, nrows=1000)
    reports.append('# Hyperliquid sample schema and missingness (first 1k rows)\n')
    reports.append(dfh.dtypes.astype(str).to_markdown())
    reports.append('\n\n')
    reports.append(dfh.head(5).to_markdown())
    reports.append('\n\n')
    # fear greed
    dff = pd.read_csv(f_path, nrows=1000)
    reports.append('# Fear & Greed sample schema (first 1k rows)\n')
    reports.append(dff.dtypes.astype(str).to_markdown())
    reports.append('\n\n')
    reports.append(dff.head(5).to_markdown())

    out = Path('outputs')
    out.mkdir(parents=True, exist_ok=True)
    repfile = out / 'schema_report.md'
    repfile.write_text('\n'.join(reports))
    print('Wrote', repfile)

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--download', nargs=2, help='Provide two gdrive urls: hyperliquid feargreed')
    p.add_argument('--local', action='store_true')
    args = p.parse_args()

    if args.download:
        h_path, f_path = download_from_gdrive(args.download[0], args.download[1])
    elif args.local:
        h_path, f_path = read_local()
    else:
        p.print_help()
        return

    simple_schema_report(h_path, f_path)
    print('Done: schema report generated in outputs/schema_report.md')

if __name__ == '__main__':
    main()