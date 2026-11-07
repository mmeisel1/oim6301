import marimo

__generated_with = "0.9.0"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    import duckdb
    from pathlib import Path

    DB_DIR = Path(__file__).parent
    DATA_DIR = DB_DIR / "data"
    DB_PATH = DB_DIR / "database.duckdb"
    return DATA_DIR, DB_PATH, duckdb, mo


@app.cell
def _(DB_PATH, duckdb):
    # Start from an empty database every time, so build.py always
    # makes the same database from the same CSV files.
    if DB_PATH.exists():
        DB_PATH.unlink()
    con = duckdb.connect(str(DB_PATH))
    return (con,)


@app.cell
def _(con):
    # The six tables. Parent tables come first, because a foreign key
    # can only point at a table that already exists.
    con.execute("""
    CREATE TABLE members (
        member_id   INTEGER PRIMARY KEY,
        first_name  VARCHAR NOT NULL,
        last_name   VARCHAR NOT NULL,
        email       VARCHAR NOT NULL UNIQUE,
        class_year  INTEGER NOT NULL,
        join_date   DATE    NOT NULL
    );

    CREATE TABLE portfolios (
        portfolio_id INTEGER PRIMARY KEY,
        member_id    INTEGER NOT NULL REFERENCES members (member_id),
        name         VARCHAR NOT NULL,
        created_date DATE    NOT NULL,
        strategy     VARCHAR              -- optional, so NULL is allowed
    );

    CREATE TABLE assets (
        asset_id   INTEGER PRIMARY KEY,
        name       VARCHAR NOT NULL,
        asset_type VARCHAR NOT NULL CHECK (asset_type IN ('stock', 'ETF', 'crypto')),
        sector     VARCHAR                -- empty for crypto
    );

    CREATE TABLE asset_tickers (
        asset_id   INTEGER NOT NULL REFERENCES assets (asset_id),
        valid_from DATE    NOT NULL,
        ticker     VARCHAR NOT NULL,
        valid_to   DATE,                  -- NULL means the ticker is still in use
        PRIMARY KEY (asset_id, valid_from),
        CHECK (valid_to IS NULL OR valid_to >= valid_from)
    );

    CREATE TABLE prices (
        asset_id    INTEGER       NOT NULL REFERENCES assets (asset_id),
        price_date  DATE          NOT NULL,
        close_price DECIMAL(18,2) NOT NULL CHECK (close_price > 0),
        PRIMARY KEY (asset_id, price_date)   -- one close per asset per day
    );

    CREATE TABLE trades (
        trade_id     INTEGER PRIMARY KEY,
        portfolio_id INTEGER       NOT NULL REFERENCES portfolios (portfolio_id),
        asset_id     INTEGER       NOT NULL REFERENCES assets (asset_id),
        trade_date   DATE          NOT NULL,
        side         VARCHAR       NOT NULL CHECK (side IN ('buy', 'sell')),
        quantity     DECIMAL(18,4) NOT NULL CHECK (quantity > 0),
        price        DECIMAL(18,2) NOT NULL CHECK (price > 0),
        fee          DECIMAL(10,2) NOT NULL DEFAULT 0 CHECK (fee >= 0),
        UNIQUE (portfolio_id, asset_id, trade_date),          -- once a day
        FOREIGN KEY (asset_id, trade_date)                    -- a day with a price
            REFERENCES prices (asset_id, price_date)
    );
    """)
    return


@app.cell
def _(DATA_DIR, con):
    # Load each CSV into its table, parents before children.
    # nullstr='' turns empty cells (no sector, no strategy, no valid_to) into NULL.
    TABLES = ["members", "portfolios", "assets", "asset_tickers", "prices", "trades"]
    for table in TABLES:
        path = DATA_DIR / f"{table}.csv"
        con.execute(
            f"INSERT INTO {table} SELECT * FROM read_csv(?, header = true, nullstr = '')",
            [str(path)],
        )
    return (TABLES,)


@app.cell
def _(TABLES, con, mo):
    # Check: how many rows landed in each table?
    counts = [
        {"table": t, "rows": con.execute(f"SELECT COUNT(*) FROM {t}").fetchall()[0][0]}
        for t in TABLES
    ]
    mo.ui.table(counts)
    return


if __name__ == "__main__":
    app.run()
