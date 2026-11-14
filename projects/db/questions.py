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

    return (ask,)


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


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Question 2**: One row for each member, members with no portfolio included: their number of portfolios and the total value they bought across them. (three tables or more)
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
