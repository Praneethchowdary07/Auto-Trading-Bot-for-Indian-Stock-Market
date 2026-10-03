"""SMA crossover strategy, signal detection and backtest for Indian stocks/indices."""
from __future__ import annotations

import numpy as np
import pandas as pd

SYMBOLS = {
    "^NSEI": "Nifty 50",
    "^NSEBANK": "Nifty Bank",
    "RELIANCE.NS": "Reliance Industries",
    "TCS.NS": "Tata Consultancy Services",
    "INFY.NS": "Infosys",
    "HDFCBANK.NS": "HDFC Bank",
}

# interval -> history period to download
PERIODS = {"1h": "3mo", "1d": "2y"}


def fetch_data(symbol: str, interval: str = "1h") -> pd.DataFrame:
    """Download OHLCV candles from Yahoo Finance."""
    import yfinance as yf  # imported lazily so the module is testable offline

    df = yf.Ticker(symbol).history(period=PERIODS[interval], interval=interval, auto_adjust=False)
    if df is None or df.empty:
        raise ValueError(f"No market data returned for {symbol}")
    df = df[["Open", "High", "Low", "Close", "Volume"]].dropna(subset=["Close"])
    if df.index.tz is not None:
        df.index = df.index.tz_convert("Asia/Kolkata").tz_localize(None)
    return df


def generate_signals(df: pd.DataFrame, short: int = 20, long: int = 50) -> pd.DataFrame:
    """Add SMA columns, position (1 = long, 0 = flat) and crossover events."""
    out = df.copy()
    out["SMA_short"] = out["Close"].rolling(short).mean()
    out["SMA_long"] = out["Close"].rolling(long).mean()
    valid = out["SMA_long"].notna()
    out["Position"] = np.where(valid & (out["SMA_short"] > out["SMA_long"]), 1, 0)
    change = out["Position"].diff()
    out["Event"] = ""
    out.loc[valid & (change == 1), "Event"] = "BUY"
    out.loc[valid & (change == -1), "Event"] = "SELL"
    return out


def backtest(df: pd.DataFrame) -> dict:
    """Long-only backtest: hold while SMA_short > SMA_long, trade on the next candle."""
    d = df[df["SMA_long"].notna()].copy()
    d["Return"] = d["Close"].pct_change().fillna(0)
    d["Strategy"] = d["Position"].shift(1).fillna(0) * d["Return"]
    d["Equity_strategy"] = (1 + d["Strategy"]).cumprod()
    d["Equity_hold"] = (1 + d["Return"]).cumprod()

    # round trips (BUY -> SELL)
    trades, entry = [], None
    for ts, row in d.iterrows():
        if row["Event"] == "BUY":
            entry = (ts, row["Close"])
        elif row["Event"] == "SELL" and entry is not None:
            trades.append((row["Close"] / entry[1]) - 1)
            entry = None
    wins = sum(1 for t in trades if t > 0)

    peak = d["Equity_strategy"].cummax()
    max_dd = ((d["Equity_strategy"] / peak) - 1).min()

    return {
        "strategy_return": float(d["Equity_strategy"].iloc[-1] - 1) if len(d) else 0.0,
        "buy_hold_return": float(d["Equity_hold"].iloc[-1] - 1) if len(d) else 0.0,
        "trades": len(trades),
        "win_rate": (wins / len(trades)) if trades else None,
        "max_drawdown": float(max_dd) if len(d) else 0.0,
        "equity": d[["Equity_strategy", "Equity_hold"]],
    }


def latest_signal(df: pd.DataFrame) -> dict:
    d = df[df["SMA_long"].notna()]
    last = d.iloc[-1]
    events = d[d["Event"] != ""]
    last_cross = events.iloc[-1] if len(events) else None
    return {
        "signal": "BUY" if last["Position"] == 1 else "SELL",
        "price": float(last["Close"]),
        "sma_short": float(last["SMA_short"]),
        "sma_long": float(last["SMA_long"]),
        "as_of": d.index[-1].strftime("%d %b %Y, %H:%M"),
        "last_cross": None
        if last_cross is None
        else {
            "type": last_cross["Event"],
            "price": float(last_cross["Close"]),
            "time": events.index[-1].strftime("%d %b %Y, %H:%M"),
        },
    }
