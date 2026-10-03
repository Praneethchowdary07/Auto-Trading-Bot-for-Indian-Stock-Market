"""Fetch market data and write static JSON/CSV files for the GitHub Pages dashboard.

Run by .github/workflows/pages.yml every hour during NSE market hours.
"""
import json
import os
import sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "webapp"))
import strategy as st  # noqa: E402

OUT = os.path.join(ROOT, "site", "data")


def main() -> int:
    os.makedirs(OUT, exist_ok=True)
    now = datetime.now(timezone.utc).isoformat()
    ok = 0
    for symbol in st.SYMBOLS:
        for interval in st.PERIODS:
            key = f"{symbol.replace('^', '').replace('.', '_')}_{interval}"
            try:
                df = st.generate_signals(st.fetch_data(symbol, interval))
                payload = st.build_payload(df, symbol, interval)
                payload["generated_at"] = now
                with open(os.path.join(OUT, f"{key}.json"), "w") as f:
                    json.dump(payload, f, separators=(",", ":"))
                st.signal_log(df).to_csv(os.path.join(OUT, f"{key}.csv"))
                ok += 1
                print(f"ok   {key}: {len(df)} candles, signal {payload['latest']['signal']}")
            except Exception as exc:  # keep going; one bad symbol shouldn't break the site
                print(f"FAIL {key}: {exc}")
    print(f"{ok} datasets written")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
