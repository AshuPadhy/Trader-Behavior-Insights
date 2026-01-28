"""Feature engineering helpers (skeleton)"""
from typing import List
import pandas as pd

def basic_trade_features(df: pd.DataFrame) -> pd.DataFrame:
    """Compute basic trade-level features.
    Assumes df has columns: execution price, size, side, time, closedPnL, leverage"""
    out = df.copy()
    # normalize column names
    if 'execution price' in out.columns:
        out = out.rename(columns={'execution price': 'price'})
    if 'closedPnL' in out.columns:
        out = out.rename(columns={'closedPnL': 'closed_pnl'})
    # notional
    if 'size' in out.columns and 'price' in out.columns:
        out['notional'] = out['size'].abs() * out['price']
    # pnl pct
    if 'closed_pnl' in out.columns and 'notional' in out.columns:
        out['pnl_pct'] = out['closed_pnl'] / out['notional'].replace(0, pd.NA)
    # is_long
    if 'side' in out.columns:
        out['is_long'] = out['side'].astype(str).str.lower().isin(['buy', 'long', 'b'])
    return out
