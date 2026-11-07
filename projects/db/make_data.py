"""Make the fake data for the Babson Investment Club database.

Run it from the root folder of the repository:
    uv run python projects/db/make_data.py

It writes six CSV files into projects/db/data/, one per table.
The data covers the 12 months up to the as_of date, 2025-12-31.
It obeys every rule in the scenario except for four trades that are
broken on purpose, two for question 7 and two for question 8 (section 6).
"""

import csv
import random
from datetime import date, timedelta
from pathlib import Path

random.seed(6301)  # same seed, same data, every time the script runs

DATA_DIR = Path(__file__).parent / "data"
YEAR_START = date(2025, 1, 1)
YEAR_END = date(2025, 12, 31)


def write_csv(name, rows):
    """Write a list of dicts to data/<name>.csv."""
    path = DATA_DIR / f"{name}.csv"
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"{name}.csv: {len(rows)} rows")


def all_days():
    """Every day of the year, Jan 1 to Dec 31."""
    day = YEAR_START
    while day <= YEAR_END:
        yield day
        day += timedelta(days=1)


# ---------------------------------------------------------------------------
# 1. assets and asset_tickers
# ---------------------------------------------------------------------------
# (asset_id, name, asset_type, sector, starting price)
ASSET_LIST = [
    (1, "Apple", "stock", "Technology", 245.0),
    (2, "Microsoft", "stock", "Technology", 420.0),
    (3, "NVIDIA", "stock", "Technology", 135.0),
    (4, "Amazon", "stock", "Consumer Discretionary", 220.0),
    (5, "JPMorgan Chase", "stock", "Financials", 240.0),
    (6, "Exxon Mobil", "stock", "Energy", 108.0),
    (7, "Johnson & Johnson", "stock", "Health Care", 145.0),
    (8, "Block", "stock", "Financials", 85.0),  # changes ticker: SQ -> XYZ
    (9, "SPDR S&P 500 ETF", "ETF", "", 590.0),
    (10, "Invesco QQQ ETF", "ETF", "", 515.0),
    (11, "Vanguard Total Bond ETF", "ETF", "", 72.0),  # never traded (question 5)
    (12, "Bitcoin", "crypto", "", 94000.0),
    (13, "Ethereum", "crypto", "", 3350.0),
    (14, "Solana", "crypto", "", 190.0),
]

assets = [
    {"asset_id": a, "name": n, "asset_type": t, "sector": s}
    for a, n, t, s, _ in ASSET_LIST
]

# One row per ticker an asset used. Block is the asset that changes:
# it traded as SQ until Jan 20, 2025, and as XYZ from Jan 21, 2025.
TICKERS = {1: "AAPL", 2: "MSFT", 3: "NVDA", 4: "AMZN", 5: "JPM", 6: "XOM",
           7: "JNJ", 9: "SPY", 10: "QQQ", 11: "BND", 12: "BTC", 13: "ETH",
           14: "SOL"}
asset_tickers = [
    {"asset_id": a, "valid_from": "2000-01-01", "ticker": t, "valid_to": ""}
    for a, t in TICKERS.items()
]
asset_tickers.append({"asset_id": 8, "valid_from": "2015-11-19",
                      "ticker": "SQ", "valid_to": "2025-01-20"})
asset_tickers.append({"asset_id": 8, "valid_from": "2025-01-21",
                      "ticker": "XYZ", "valid_to": ""})
asset_tickers.sort(key=lambda r: (r["asset_id"], r["valid_from"]))

# ---------------------------------------------------------------------------
# 2. prices: one closing price per asset per trading day
#    stocks and ETFs: every weekday; crypto: every day
# ---------------------------------------------------------------------------
prices = []
close = {}  # close[(asset_id, day)] = closing price; also our set of price days
for asset_id, _, asset_type, _, start_price in ASSET_LIST:
    price = start_price
    daily_move = 0.035 if asset_type == "crypto" else 0.015
    for day in all_days():
        if asset_type != "crypto" and day.weekday() >= 5:  # 5 = Sat, 6 = Sun
            continue
        price = price * (1 + random.gauss(0.0004, daily_move))
        price = round(price, 2)
        close[(asset_id, day)] = price
        prices.append({"asset_id": asset_id, "price_date": day.isoformat(),
                       "close_price": price})

# ---------------------------------------------------------------------------
# 3. members: 15, and some of them will get no portfolio (question 2)
# ---------------------------------------------------------------------------
NAMES = [("Ava", "Chen"), ("Liam", "Patel"), ("Sofia", "Garcia"),
         ("Noah", "Kim"), ("Mia", "Rossi"), ("Ethan", "Okafor"),
         ("Isabella", "Silva"), ("Lucas", "Novak"), ("Amelia", "Haddad"),
         ("Mateo", "Lopez"), ("Harper", "Nguyen"), ("Leo", "Schmidt"),
         ("Zoe", "Ibrahim"), ("Jack", "Murphy"), ("Chloe", "Tanaka")]

members = []
for member_id, (first, last) in enumerate(NAMES, start=1):
    class_year = random.choice([2026, 2027, 2028, 2029])
    joined = date(class_year - 4, 9, 1) + timedelta(days=random.randint(0, 400))
    members.append({
        "member_id": member_id,
        "first_name": first,
        "last_name": last,
        "email": f"{first.lower()}.{last.lower()}@babson.edu",
        "class_year": class_year,
        "join_date": joined.isoformat(),
    })

# ---------------------------------------------------------------------------
# 4. portfolios: members 14 and 15 get none; a few members get two or three
# ---------------------------------------------------------------------------
PORTFOLIO_COUNTS = {1: 2, 2: 1, 3: 3, 4: 1, 5: 2, 6: 1, 7: 1, 8: 2,
                    9: 1, 10: 1, 11: 1, 12: 2, 13: 1}  # 14, 15: none
STRATEGIES = ["Growth", "Value", "Dividend", "Crypto", "Index", ""]  # "" = none

portfolios = []
portfolio_id = 0
for member in members:
    for n in range(PORTFOLIO_COUNTS.get(member["member_id"], 0)):
        portfolio_id += 1
        joined = date.fromisoformat(member["join_date"])
        created = max(joined, date(2024, 6, 1)) + timedelta(days=random.randint(0, 200))
        created = min(created, date(2025, 3, 1))  # every portfolio exists by March
        portfolios.append({
            "portfolio_id": portfolio_id,
            "member_id": member["member_id"],
            "name": f"{member['first_name']}'s Portfolio {n + 1}",
            "created_date": created.isoformat(),
            "strategy": random.choice(STRATEGIES),
        })

# ---------------------------------------------------------------------------
# 5. trades, made in date order so holdings are always up to date
# ---------------------------------------------------------------------------
TRADED_ASSETS = [a for a, *_ in ASSET_LIST if a != 11]  # BND is never traded
holdings = {}       # holdings[(portfolio_id, asset_id)] = units held now
traded_today = set()  # (portfolio_id, asset_id, day): at most one trade a day
trades = []

for day in all_days():
    for _ in range(random.randint(0, 3)):  # up to 3 tries a day, ~350 trades
        portfolio = random.choice(portfolios)
        p_id = portfolio["portfolio_id"]
        if day < date.fromisoformat(portfolio["created_date"]):
            continue
        asset_id = random.choice(TRADED_ASSETS)
        if (asset_id, day) not in close:  # rule: only on days with a price
            continue
        if (p_id, asset_id, day) in traded_today:  # rule: once a day
            continue

        held = holdings.get((p_id, asset_id), 0)
        is_crypto = asset_id in (12, 13, 14)
        side = "sell" if held > 0 and random.random() < 0.35 else "buy"

        if side == "buy":
            if is_crypto:
                quantity = round(random.uniform(200, 3000) / close[(asset_id, day)], 4)  # $200-$3,000 worth
            else:
                quantity = random.randint(1, 20)
        else:  # rule: never sell more than held
            if is_crypto:
                quantity = round(held * random.uniform(0.3, 1.0), 4)
            else:
                quantity = random.randint(1, int(held))
        if quantity <= 0:
            continue

        # trade price is near the close, within about 1.5%
        price = round(close[(asset_id, day)] * (1 + random.uniform(-0.015, 0.015)), 2)
        fee = random.choice([0, 0, 0, 1.00, 2.50, 4.95])

        trades.append({
            "trade_id": len(trades) + 1,
            "portfolio_id": p_id,
            "asset_id": asset_id,
            "trade_date": day.isoformat(),
            "side": side,
            "quantity": quantity,
            "price": price,
            "fee": fee,
        })
        traded_today.add((p_id, asset_id, day))
        change = quantity if side == "buy" else -quantity
        holdings[(p_id, asset_id)] = round(held + change, 4)

# ---------------------------------------------------------------------------
# 6. four deliberately broken trades, two for each rule-check question.
#    The assignment asks for exactly two broken rows per "checks a rule"
#    question, so that questions 7 and 8 have something to find.
# ---------------------------------------------------------------------------
def add_trade(portfolio_id, asset_id, day, side, quantity, price, fee=0):
    trades.append({
        "trade_id": len(trades) + 1,
        "portfolio_id": portfolio_id,
        "asset_id": asset_id,
        "trade_date": day.isoformat(),
        "side": side,
        "quantity": quantity,
        "price": price,
        "fee": fee,
    })
    return len(trades)


# Question 7: two stock trades on a Saturday, when stocks have no closing price.
broken_q7 = [
    add_trade(1, 1, date(2025, 3, 15), "buy", 5, 230.00),    # Apple, Sat Mar 15
    add_trade(2, 2, date(2025, 8, 9), "buy", 3, 450.00),     # Microsoft, Sat Aug 9
]

# Question 8: two sells of more units than the portfolio holds.
# Each goes on a day with a closing price, so it breaks only the sell rule.
broken_q8 = []
for p_id, asset_id in [(3, 6), (5, 7)]:  # Exxon and J&J
    day = date(2025, 12, 30) if len(broken_q8) == 0 else date(2025, 12, 29)
    held = holdings.get((p_id, asset_id), 0)
    broken_q8.append(add_trade(p_id, asset_id, day, "sell", int(held) + 10,
                               close[(asset_id, day)]))

print("Broken on purpose, question 7 (no closing price):", broken_q7)
print("Broken on purpose, question 8 (sells more than held):", broken_q8)

# ---------------------------------------------------------------------------
# 7. write the CSV files
# ---------------------------------------------------------------------------
DATA_DIR.mkdir(exist_ok=True)
write_csv("members", members)
write_csv("portfolios", portfolios)
write_csv("assets", assets)
write_csv("asset_tickers", asset_tickers)
write_csv("prices", prices)
write_csv("trades", trades)
