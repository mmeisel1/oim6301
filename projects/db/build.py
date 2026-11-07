import marimo

__generated_with = "0.9.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import duckdb
    import polars as pl

    database = mo.notebook_dir() / "database.duckdb"
    data_dir = mo.notebook_dir() / "data"
    AS_OF = "2025-12-31"  # the data covers the 12 months up to this date

    def ask(sql):
        with duckdb.connect(database, read_only=True) as _con:
            return _con.sql(sql).pl()
    return AS_OF, ask, data_dir, database, duckdb, mo, pl


@app.cell
def _(mo):
    mo.md(r"""
    # Babson Investment Club: building the database

    This notebook builds `database.duckdb` from the CSV files that
    `make_data.py` writes in `data/`. Run `make_data.py` first.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 1. The Tables

    One `CREATE TABLE` per table. Parent tables come first, because a
    foreign key can only point at a table that already exists.
    """)
    return


@app.cell
def _():
    SCHEMA = """
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
        member_id    INTEGER NOT NULL REFERENCES members (member_id),  -- exactly one member
        name         VARCHAR NOT NULL,
        created_date DATE    NOT NULL,
        strategy     VARCHAR                                           -- optional
    );

    CREATE TABLE assets (
        asset_id   INTEGER PRIMARY KEY,
        name       VARCHAR NOT NULL,
        asset_type VARCHAR NOT NULL CHECK (asset_type IN ('stock', 'ETF', 'crypto')),
        sector     VARCHAR                                             -- crypto has none
    );

    CREATE TABLE asset_tickers (
        asset_id   INTEGER NOT NULL REFERENCES assets (asset_id),
        valid_from DATE    NOT NULL,
        ticker     VARCHAR NOT NULL,
        valid_to   DATE,                                               -- NULL = still in use
        PRIMARY KEY (asset_id, valid_from),
        CHECK (valid_to IS NULL OR valid_to >= valid_from)
    );

    CREATE TABLE prices (
        asset_id    INTEGER       NOT NULL REFERENCES assets (asset_id),
        price_date  DATE          NOT NULL,
        close_price DECIMAL(18,2) NOT NULL CHECK (close_price > 0),
        PRIMARY KEY (asset_id, price_date)                 -- one close per asset per day
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
        UNIQUE (portfolio_id, asset_id, trade_date)        -- at most once a day
    );
    """
    return (SCHEMA,)


@app.cell
def _(mo):
    mo.md(r"""
    ## 2. The Data

    `make_data.py` writes the data for the 12 months up to `AS_OF`
    (2025-12-31). It obeys every rule except four trades that are broken
    on purpose, so that the two rule-check questions have something to find:

    | trade_id | broken on purpose for | what is wrong |
    |---|---|---|
    | 389 | question 7 | Apple bought on Saturday 2025-03-15, a day with no closing price |
    | 390 | question 7 | Microsoft bought on Saturday 2025-08-09, a day with no closing price |
    | 391 | question 8 | portfolio 3 sells 10 more units of Exxon than it holds |
    | 392 | question 8 | portfolio 5 sells 10 more units of Johnson & Johnson than it holds |

    Unattached rows: members 14 and 15 own no portfolio, and the Vanguard
    Total Bond ETF (asset 11) is never traded.

    The cell below deletes the old database, builds it again from the CSVs,
    and saves the view from section 7.
    """)
    return


@app.cell
def _(AS_OF, SCHEMA, data_dir, database, duckdb):
    TABLES = ["members", "portfolios", "assets", "asset_tickers", "prices", "trades"]

    database.unlink(missing_ok=True)  # delete the old database first

    with duckdb.connect(database) as _con:
        _con.execute(SCHEMA)
        for _table in TABLES:
            # nullstr='' turns empty cells (no sector, no strategy, no valid_to) into NULL
            _con.execute(
                f"INSERT INTO {_table} SELECT * FROM read_csv(?, header = true, nullstr = '')",
                [str(data_dir / f"{_table}.csv")],
            )

        # The view for section 7: what each portfolio holds on AS_OF.
        _con.execute(f"""
            CREATE VIEW current_holdings AS
            SELECT
                t.portfolio_id,
                t.asset_id,
                SUM(CASE WHEN t.side = 'buy' THEN t.quantity ELSE -t.quantity END) AS units
            FROM trades t
            WHERE t.trade_date <= DATE '{AS_OF}'
            GROUP BY t.portfolio_id, t.asset_id
            HAVING SUM(CASE WHEN t.side = 'buy' THEN t.quantity ELSE -t.quantity END) > 0
        """)
    return (TABLES,)


@app.cell
def _(mo):
    mo.md(r"""
    ## 3. A Look at the Data

    NVIDIA's closing price, every trading day of the year, read straight
    from `data/prices.csv` with polars.
    """)
    return


@app.cell
def _(data_dir, pl):
    nvidia = (
        pl.read_csv(data_dir / "prices.csv", try_parse_dates=True)
        .filter(pl.col("asset_id") == 3)  # asset 3 is NVIDIA
    )
    nvidia.plot.line(x="price_date", y="close_price")
    return


@app.cell
def _(mo):
    mo.md(r"""
    **Would a real business look like that?** Mostly yes: a big tech stock really does move a few percent up and down from day to day like this, but real NVIDIA prices jump on news such as earnings, AI and leadership announcements, and geopolitical events, while these moves are just random numbers.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 4. Row Counts
    """)
    return


@app.cell
def _(TABLES, ask, pl):
    pl.concat(
        [ask(f"SELECT '{t}' AS table_name, COUNT(*) AS row_count FROM {t}") for t in TABLES]
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 5. A Row It Refuses

    A trade that is neither a buy nor a sell. The `CHECK` on `side`
    should refuse it, and the database should stay unchanged.
    """)
    return


@app.cell
def _(TABLES, database, duckdb, mo):
    assert TABLES  # run this after the build
    try:
        with duckdb.connect(database) as _con:
            _con.execute("""
                INSERT INTO trades VALUES
                    (9999, 1, 1, DATE '2025-06-02', 'hold', 5, 200.00, 0)
            """)
        refused = "The insert was accepted. That should not happen!"
    except duckdb.Error as error:
        refused = f"Refused: {error}"
    mo.md(f"```\n{refused}\n```")
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 6. Answers You Already Knew

    Three questions I can answer from how I made the data, before asking
    the database:

    | question | expected |
    |---|---|
    | members who own no portfolio | 2 (members 14 and 15) |
    | assets that were never traded | 1 (Vanguard Total Bond ETF) |
    | trades on a day their asset has no closing price | 2 (trades 389 and 390) |
    """)
    return


@app.cell
def _(TABLES, ask, pl):
    assert TABLES  # run this after the build
    known = pl.DataFrame({
        "question": [
            "members who own no portfolio",
            "assets that were never traded",
            "trades on a day with no closing price",
        ],
        "expected": [2, 1, 2],
        "actual": [
            ask("""SELECT COUNT(*) FROM members m
                   WHERE NOT EXISTS (SELECT 1 FROM portfolios p
                                     WHERE p.member_id = m.member_id)""").item(),
            ask("""SELECT COUNT(*) FROM assets a
                   WHERE NOT EXISTS (SELECT 1 FROM trades t
                                     WHERE t.asset_id = a.asset_id)""").item(),
            ask("""SELECT COUNT(*) FROM trades t
                   WHERE NOT EXISTS (SELECT 1 FROM prices p
                                     WHERE p.asset_id = t.asset_id
                                       AND p.price_date = t.trade_date)""").item(),
        ],
    })
    known.with_columns((pl.col("expected") == pl.col("actual")).alias("match"))
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 7. A View

    The weekly question: **what does each portfolio hold right now?**
    The view `current_holdings`, saved in the build cell in section 2,
    gives for each portfolio and asset the units bought minus the units
    sold up to `AS_OF`, keeping only those above zero. Part B question 3
    uses it.
    """)
    return


@app.cell
def _(TABLES, ask):
    assert TABLES  # run this after the build
    ask("SELECT * FROM current_holdings ORDER BY portfolio_id, asset_id")
    return


if __name__ == "__main__":
    app.run()
