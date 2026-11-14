import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import duckdb

    return duckdb, mo


@app.cell
def _(duckdb, mo):
    database = mo.notebook_dir() / "database.duckdb"
    AS_OF = "2025-12-31"  # the data covers the 12 months up to this date

    def ask(sql):
        with duckdb.connect(database, read_only=True) as _con:
            return _con.sql(sql).pl()

    return AS_OF, ask


@app.cell
def _(ask):
    ask("SELECT side, count(*) AS trades FROM trades GROUP BY side")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Babson Investment Club: Business Questions

    Every date counts back from AS_OF, 2025-12-31. "The last 30 days" means the 30 days ending on that date, December 2 to December 31, 2025.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Question 1**: For each portfolio over the last 30 days: the number of trades, the money spent on buys with fees added, and the money received from sells with fees taken off.
    """)
    return


@app.cell
def _(AS_OF, ask):
    ask(f"""
        SELECT p.portfolio_id,
               p.name AS portfolio,
               count(t.trade_id) AS trades,
               round(CAST(coalesce(sum(CASE WHEN t.side = 'buy'
                                            THEN t.quantity * t.price + t.fee END), 0) AS DOUBLE), 2) AS spent_on_buys,
               round(CAST(coalesce(sum(CASE WHEN t.side = 'sell'
                                            THEN t.quantity * t.price - t.fee END), 0) AS DOUBLE), 2) AS received_from_sells
        FROM portfolios AS p
        LEFT JOIN trades AS t
            ON t.portfolio_id = p.portfolio_id
           AND t.trade_date >  DATE '{AS_OF}' - INTERVAL 30 DAY
           AND t.trade_date <= DATE '{AS_OF}'
        GROUP BY p.portfolio_id, p.name
        ORDER BY p.portfolio_id
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In the 30 days ending 2025-12-31, the 19 portfolios made 46 trades, spending $87,251.51 on buys (fees added) and receiving $11,594.59 from sells (fees taken off). Liam’s Portfolio 1 was the most active, with 5 trades, and Leo’s Portfolio 1 spent the most, $16,800.18. I read “each portfolio” as all 19, so the two with no trades in that window, Ava’s Portfolio 2 and Harper’s Portfolio 1, are listed with 0.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Question 2**: One row for each member, members with no portfolio included: their number of portfolios and the total value they bought across them. (three tables or more)
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT m.member_id,
               m.first_name || ' ' || m.last_name AS member,
               count(DISTINCT p.portfolio_id) AS portfolios,
               round(CAST(coalesce(sum(t.quantity * t.price), 0) AS DOUBLE), 2) AS total_bought
        FROM members AS m
        LEFT JOIN portfolios AS p ON p.member_id = m.member_id
        LEFT JOIN trades AS t
            ON t.portfolio_id = p.portfolio_id
           AND t.side = 'buy'
        GROUP BY m.member_id, m.first_name, m.last_name
        ORDER BY total_bought DESC
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    All 15 members are listed, and together they bought $758,705.24 across 19 portfolios. Sofia Garcia owns the most portfolios, 3, and bought the most, $133,914.76; Jack Murphy and Chloe Tanaka have no portfolio, so they show 0. I counted the value bought as quantity × price, without fees, because the club keeps the fee apart from a trade’s value.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Question 3**: What each portfolio holds on your as_of date: for each asset, the units bought minus the units sold, keeping only those above zero. (three tables or more)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Question 4**: For every trade in the last 90 days, the closing price on the trade date, and how far the trade price was from it, as a percent of the closing price. (three tables or more)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Question 5**: The assets the club follows that no portfolio has ever traded.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Question 6**: The asset that changed its ticker: its value traded over the year, under both tickers together.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Question 7**: Every trade checked against the rule that it happens on a day its asset has a closing price, and a list of any that break it. (checks a rule)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Question 8**: Every sell checked against the rule that a portfolio never sells more than it holds, and a list of any that break it. (checks a rule)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Question 9**:
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Question 10**:
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. How I Know These Numbers Are Right
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. Working With the Agent
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Reading It Back

    **Prediction (Question 2):** I expect 335 rows from the joins members LEFT JOIN portfolios LEFT JOIN trades (buys only), before any grouping: one row for each of the 333 buys, plus one row each for members 14 and 15, who have no portfolio but are kept by the LEFT JOIN. I expect every portfolio to have at least one buy, so no portfolio adds an empty row.

    After running it: Result: The joins alone give 335 rows, so my prediction matched. The 333 buys each became one row, members 14 and 15 (Jack Murphy and Chloe Tanaka) each kept one row because of the LEFT JOIN, and every one of the 19 portfolios had at least one buy, so no portfolio added an empty row.

    One row of the final result is one member, with their number of portfolios and the total value of all the buys across them.
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT count(*) AS rows_before_grouping
        FROM members AS m
        LEFT JOIN portfolios AS p ON p.member_id = m.member_id
        LEFT JOIN trades AS t
            ON t.portfolio_id = p.portfolio_id
           AND t.side = 'buy'
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. Going Further
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. Time Spent
    """)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
