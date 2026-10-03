# 📈 Auto-Trading Bot for Indian Stock Market (Nifty 50)

Welcome to one of the most **practical, signal-driven, and recruiter-magnet** projects you'll come across!  
This Auto-Trading Bot generates intelligent **Buy/Sell signals** for Nifty 50 using proven **SMA crossover strategies**.  

> “If you're a recruiter looking for a smart, disciplined engineer who automates decisions better than most people make them — stop scrolling. This is it.”  

---

## 🌐 Live Web App

**Live demo:** _add your Hugging Face Space link here_

The `webapp/` folder is a Flask web app with a clean dashboard: pick Nifty 50, Nifty Bank or a large-cap NSE stock,
switch hourly/daily, and see the current signal, SMA 20/50 chart with crossover points, a long-only backtest
(strategy vs buy & hold, trades, win rate, max drawdown) and a downloadable CSV signal log.

```bash
cd webapp && pip install -r requirements.txt && python app.py   # http://localhost:7860
```

> 🔐 Telegram alerts now read `TELEGRAM_TOKEN` and `CHAT_ID` from environment variables — never commit them.

## 🔧 How It Works

This bot automates signal generation using the following logic:

1. 📊 Fetches **hourly Nifty 50 data** (via `yfinance`)
2. 📉 Calculates **SMA(20)** and **SMA(50)**
3. 🧠 Detects **crossover points**
4. 📬 Triggers Buy/Sell signals with visual output
5. 📤 Exports:
   - CSV logs
   - Trading chart
   - Telegram-style signal image

---

## 📁 Outputs

### ✅ Latest Signal (Telegram Style)
![Telegram Signal](outputs/styled_telegram_signal_output.png)

### 📈 Signal Chart (Crossover Points)
![Crossover Chart](outputs/nifty_sma_signals_simulated.png)

### 📄 CSV Output
[Download Signal Log (CSV)](outputs/nifty_sma_signals_simulated.csv)

---

## 💡 Why This Project Matters

- 💼 Real-world finance application
- ⚙️ Python scripting, data automation, visualization
- 📊 Strategy can scale to real brokerage APIs (e.g. Zerodha Kite)
- 🧠 Demonstrates pattern recognition, automation & risk insight

---

## 🛠 Tech Stack

- Python 🐍
- `yfinance` – For data fetching
- `pandas` – Data wrangling
- `matplotlib` – Visualization
- `Pillow` – Image generation

---

## 🚀 Run It Yourself

```bash
git clone https://github.com/yourusername/Auto-Trading-Bot-for-Indian-Stock-Market.git
cd Auto-Trading-Bot-for-Indian-Stock-Market
pip install -r requirements.txt
python nifty_sma_bot.py
