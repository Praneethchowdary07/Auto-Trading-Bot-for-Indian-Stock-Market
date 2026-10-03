"""Flask web app for the Nifty 50 SMA crossover trading bot."""
from __future__ import annotations

import io
import time

from flask import Flask, Response, jsonify, render_template, request

import strategy as st

app = Flask(__name__)
CACHE_SECONDS = 600
_cache: dict[tuple[str, str], tuple[float, object]] = {}


def load(symbol: str, interval: str):
    key = (symbol, interval)
    hit = _cache.get(key)
    if hit and time.time() - hit[0] < CACHE_SECONDS:
        return hit[1]
    df = st.generate_signals(st.fetch_data(symbol, interval))
    _cache[key] = (time.time(), df)
    return df


def params():
    symbol = request.args.get("symbol", "^NSEI")
    interval = request.args.get("interval", "1h")
    if symbol not in st.SYMBOLS or interval not in st.PERIODS:
        raise ValueError("Unsupported symbol or interval")
    return symbol, interval


@app.get("/")
def index():
    return render_template("index.html", symbols=st.SYMBOLS)


@app.get("/api/signals")
def api_signals():
    try:
        symbol, interval = params()
        df = load(symbol, interval)
    except Exception as exc:  # network errors, bad symbol, empty data
        return jsonify(error=str(exc)), 502

    return jsonify(st.build_payload(df, symbol, interval))


@app.get("/api/signals.csv")
def api_csv():
    try:
        symbol, interval = params()
        df = load(symbol, interval)
    except Exception as exc:
        return Response(str(exc), status=502)
    buf = io.StringIO()
    st.signal_log(df).to_csv(buf)
    fname = f"signals_{symbol.replace('^', '')}_{interval}.csv"
    return Response(buf.getvalue(), mimetype="text/csv",
                    headers={"Content-Disposition": f"attachment; filename={fname}"})


@app.get("/health")
def health():
    return "ok"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860, debug=False)
