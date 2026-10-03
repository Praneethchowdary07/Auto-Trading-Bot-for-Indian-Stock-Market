---
title: Nifty Trading Bot
emoji: 📈
colorFrom: blue
colorTo: gray
sdk: docker
app_port: 7860
pinned: false
short_description: SMA 20/50 crossover signals and backtest for Indian markets
---

# Auto Trading Bot for Indian Stock Market (Nifty 50)

Live web demo of an SMA(20)/SMA(50) crossover strategy for Nifty 50, Nifty Bank and large-cap NSE stocks.

- Fetches hourly or daily candles from Yahoo Finance (yfinance)
- Detects Buy/Sell crossovers and shows the current signal
- Long-only backtest: strategy vs buy & hold, trades, win rate, max drawdown
- Interactive price and equity charts, downloadable CSV signal log

**Stack:** Python, Pandas, NumPy, yfinance, Flask, Gunicorn, vanilla JS/SVG charts

Run locally:

```bash
pip install -r requirements.txt
python app.py   # http://localhost:7860
```

For education and research only. Not financial advice.
