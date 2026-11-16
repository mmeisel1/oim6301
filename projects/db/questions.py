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


@app.cell
def _():
    #checking my answer
    return


@app.cell
def _(ask, mo):
    _alone = ask("""
        SELECT round(CAST(sum(quantity * price) AS DOUBLE), 2) AS bought,
               (SELECT count(*) FROM portfolios) AS portfolios
        FROM trades
        WHERE side = 'buy'
    """)
    _q2 = ask("""
        SELECT m.member_id,
               count(DISTINCT p.portfolio_id) AS portfolios,
               round(CAST(coalesce(sum(t.quantity * t.price), 0) AS DOUBLE), 2) AS total_bought
        FROM members AS m
        LEFT JOIN portfolios AS p ON p.member_id = m.member_id
        LEFT JOIN trades AS t
            ON t.portfolio_id = p.portfolio_id
           AND t.side = 'buy'
        GROUP BY m.member_id
    """)
    _answer_bought     = round(float(_q2["total_bought"].sum()), 2)
    _answer_portfolios = int(_q2["portfolios"].sum())
    _alone_bought      = float(_alone["bought"][0])
    _alone_portfolios  = int(_alone["portfolios"][0])

    assert _answer_portfolios == _alone_portfolios and abs(_answer_bought - _alone_bought) < 0.1, \
        f"Question 2 does not add up: {_answer_portfolios} vs {_alone_portfolios} portfolios, {_answer_bought} vs {_alone_bought}"

    mo.md(f"**Check 2, Question 2:** the 15 member rows add up to {_answer_portfolios} portfolios and {_answer_bought:,.2f} bought; `portfolios` and `trades` alone give {_alone_portfolios} portfolios and {_alone_bought:,.2f}. They agree.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Question 3**: What each portfolio holds on your as_of date: for each asset, the units bought minus the units sold, keeping only those above zero. (three tables or more)
    """)
    return


@app.cell
def _(AS_OF, ask):
    ask(f"""
        SELECT p.portfolio_id,
               p.name AS portfolio,
               a.name AS asset,
               tk.ticker,
               CAST(sum(CASE WHEN t.side = 'buy' THEN t.quantity
                             ELSE -t.quantity END) AS DOUBLE) AS units_held
        FROM trades AS t
        JOIN portfolios AS p ON p.portfolio_id = t.portfolio_id
        JOIN assets     AS a ON a.asset_id     = t.asset_id
        LEFT JOIN asset_tickers AS tk
            ON tk.asset_id = a.asset_id
           AND tk.valid_from <= DATE '{AS_OF}'
           AND (tk.valid_to IS NULL OR tk.valid_to >= DATE '{AS_OF}')
        WHERE t.trade_date <= DATE '{AS_OF}'
        GROUP BY p.portfolio_id, p.name, a.name, tk.ticker
        HAVING sum(CASE WHEN t.side = 'buy' THEN t.quantity
                        ELSE -t.quantity END) > 0
        ORDER BY p.portfolio_id, asset
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    On 2025-12-31, the 19 portfolios hold 188 positions across 13 assets; for example, Ava’s Portfolio 1 holds 31 shares of JPMorgan Chase, 21 of Microsoft and 0.075 Bitcoin. I measured each holding in units (bought minus sold) rather than in dollars, show each asset under the ticker it used on that date (so Block appears as XYZ), and left out positions that were fully sold.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Question 4**: For every trade in the last 90 days, the closing price on the trade date, and how far the trade price was from it, as a percent of the closing price. (three tables or more)
    """)
    return


@app.cell
def _(AS_OF, ask):
    ask(f"""
        SELECT t.trade_id,
               t.trade_date,
               p.name AS portfolio,
               a.name AS asset,
               t.side,
               CAST(t.price AS DOUBLE)        AS trade_price,
               CAST(pr.close_price AS DOUBLE) AS closing_price,
               round(CAST(100.0 * (t.price - pr.close_price) / pr.close_price AS DOUBLE), 2) AS gap_pct
        FROM trades AS t
        JOIN portfolios AS p ON p.portfolio_id = t.portfolio_id
        JOIN assets     AS a ON a.asset_id     = t.asset_id
        LEFT JOIN prices AS pr
            ON pr.asset_id   = t.asset_id
           AND pr.price_date = t.trade_date
        WHERE t.trade_date >  DATE '{AS_OF}' - INTERVAL 90 DAY
          AND t.trade_date <= DATE '{AS_OF}'
        ORDER BY t.trade_date, t.trade_id
    """)
    return


@app.cell
def _(AS_OF, ask):
    ask(f"""
        SELECT count(*) AS trades,
               round(CAST(avg(abs(100.0 * (t.price - pr.close_price) / pr.close_price)) AS DOUBLE), 2) AS avg_abs_gap_pct,
               round(CAST(max(abs(100.0 * (t.price - pr.close_price) / pr.close_price)) AS DOUBLE), 2) AS max_abs_gap_pct
        FROM trades AS t
        JOIN prices AS pr ON pr.asset_id = t.asset_id AND pr.price_date = t.trade_date
        WHERE t.trade_date >  DATE '{AS_OF}' - INTERVAL 90 DAY
          AND t.trade_date <= DATE '{AS_OF}'
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In the 90 days ending 2025-12-31, 116 trades were made, and every one has a closing price for its trade date. On average a trade price was 0.73% away from that day’s close, and the largest gap was 1.48%. I measured the gap as (trade price − closing price) ÷ closing price, so a positive number means the trade was above the close; the average and the largest gap use the size of the gap, ignoring its direction.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Question 5**: The assets the club follows that no portfolio has ever traded.
    """)
    return


@app.cell
def _(AS_OF, ask):
    ask(f"""
        SELECT a.asset_id,
               a.name AS asset,
               tk.ticker,
               a.asset_type,
               a.sector
        FROM assets AS a
        LEFT JOIN trades AS t ON t.asset_id = a.asset_id
        LEFT JOIN asset_tickers AS tk
            ON tk.asset_id = a.asset_id
           AND tk.valid_from <= DATE '{AS_OF}'
           AND (tk.valid_to IS NULL OR tk.valid_to >= DATE '{AS_OF}')
        WHERE t.trade_id IS NULL
        ORDER BY a.asset_id
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Only one of the assets the club follows has never been traded by any portfolio: the Vanguard Total Bond ETF (BND). Every other asset has at least one trade.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Question 6**: The asset that changed its ticker: its value traded over the year, under both tickers together.
    """)
    return


@app.cell
def _(AS_OF, ask):
    ask(f"""
        SELECT a.name AS asset,
               tk.ticker,
               tk.valid_from,
               tk.valid_to,
               count(t.trade_id) AS trades,
               round(CAST(coalesce(sum(t.quantity * t.price), 0) AS DOUBLE), 2) AS value_traded
        FROM (SELECT asset_id FROM asset_tickers
              GROUP BY asset_id HAVING count(*) > 1) AS changed
        JOIN assets AS a         ON a.asset_id  = changed.asset_id
        JOIN asset_tickers AS tk ON tk.asset_id = a.asset_id
        LEFT JOIN trades AS t
            ON t.asset_id = a.asset_id
           AND t.trade_date >= tk.valid_from
           AND (tk.valid_to IS NULL OR t.trade_date <= tk.valid_to)
           AND t.trade_date >  DATE '{AS_OF}' - INTERVAL 1 YEAR
           AND t.trade_date <= DATE '{AS_OF}'
        GROUP BY a.name, tk.ticker, tk.valid_from, tk.valid_to
        ORDER BY tk.valid_from
    """)
    return


@app.cell
def _(AS_OF, ask):
    ask(f"""
        SELECT a.name AS asset,
               count(*) AS trades,
               round(CAST(sum(t.quantity * t.price) AS DOUBLE), 2) AS value_traded
        FROM trades AS t
        JOIN assets AS a ON a.asset_id = t.asset_id
        WHERE t.asset_id IN (SELECT asset_id FROM asset_tickers
                             GROUP BY asset_id HAVING count(*) > 1)
          AND t.trade_date >  DATE '{AS_OF}' - INTERVAL 1 YEAR
          AND t.trade_date <= DATE '{AS_OF}'
        GROUP BY a.name
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The asset that changed its ticker is Block: it traded as SQ until 2025-01-20 and as XYZ from 2025-01-21. Over the year ending 2025-12-31, the portfolios traded $22,765.91 of Block in 24 trades: $1,960.71 in 2 trades under SQ and $20,805.20 in 22 trades under XYZ. I counted the value traded as quantity × price for buys and sells together, without fees.
    """)
    return


@app.cell
def _():
    #checking my answers
    return


@app.cell
def _(AS_OF, ask):
    q6_by_ticker = ask(f"""
        SELECT a.name AS asset,
               tk.ticker,
               tk.valid_from,
               tk.valid_to,
               count(t.trade_id) AS trades,
               round(CAST(coalesce(sum(t.quantity * t.price), 0) AS DOUBLE), 2) AS value_traded
        FROM (SELECT asset_id FROM asset_tickers
              GROUP BY asset_id HAVING count(*) > 1) AS changed
        JOIN assets AS a         ON a.asset_id  = changed.asset_id
        JOIN asset_tickers AS tk ON tk.asset_id = a.asset_id
        LEFT JOIN trades AS t
            ON t.asset_id = a.asset_id
           AND t.trade_date >= tk.valid_from
           AND (tk.valid_to IS NULL OR t.trade_date <= tk.valid_to)
           AND t.trade_date >  DATE '{AS_OF}' - INTERVAL 1 YEAR
           AND t.trade_date <= DATE '{AS_OF}'
        GROUP BY a.name, tk.ticker, tk.valid_from, tk.valid_to
        ORDER BY tk.valid_from
    """)
    q6_by_ticker
    return (q6_by_ticker,)


@app.cell
def _(AS_OF, ask):
    q6_total = ask(f"""
        SELECT a.name AS asset,
               count(t.trade_id) AS trades,
               round(CAST(coalesce(sum(t.quantity * t.price), 0) AS DOUBLE), 2) AS value_traded
        FROM assets AS a
        JOIN trades AS t ON t.asset_id = a.asset_id
        WHERE a.asset_id IN (SELECT asset_id FROM asset_tickers
                             GROUP BY asset_id HAVING count(*) > 1)
          AND t.trade_date >  DATE '{AS_OF}' - INTERVAL 1 YEAR
          AND t.trade_date <= DATE '{AS_OF}'
        GROUP BY a.name
    """)
    q6_total
    return (q6_total,)


@app.cell
def _(mo, q6_by_ticker, q6_total):
    _parts_trades = int(q6_by_ticker["trades"].sum())
    _total_trades = int(q6_total["trades"][0])
    _parts_value  = round(float(q6_by_ticker["value_traded"].sum()), 2)
    _total_value  = float(q6_total["value_traded"][0])

    assert _parts_trades == _total_trades and abs(_parts_value - _total_value) < 0.01, \
        f"Question 6 does not add up: {_parts_trades} vs {_total_trades} trades, {_parts_value} vs {_total_value}"

    mo.md(f"**Check 1, Question 6:** SQ + XYZ = {_parts_trades} trades and {_parts_value:,.2f} traded; Block's total from `trades` alone = {_total_trades} trades and {_total_value:,.2f}. They agree.")
    return


@app.cell
def _():
    # AssertionError: Question 6 does not add up: 46 vs 24 trades, 43571.11 vs 22765.91 (this was changed)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Question 7**: Every trade checked against the rule that it happens on a day its asset has a closing price, and a list of any that break it. (checks a rule)
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT count(*) AS trades_checked,
               count(pr.price_date) AS with_closing_price,
               count(*) - count(pr.price_date) AS breaking_the_rule
        FROM trades AS t
        LEFT JOIN prices AS pr
            ON pr.asset_id   = t.asset_id
           AND pr.price_date = t.trade_date
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT t.trade_id,
               t.trade_date,
               dayname(t.trade_date) AS weekday,
               p.name AS portfolio,
               a.name AS asset,
               a.asset_type,
               t.side,
               t.quantity,
               CAST(t.price AS DOUBLE) AS price
        FROM trades AS t
        JOIN portfolios AS p ON p.portfolio_id = t.portfolio_id
        JOIN assets     AS a ON a.asset_id     = t.asset_id
        LEFT JOIN prices AS pr
            ON pr.asset_id   = t.asset_id
           AND pr.price_date = t.trade_date
        WHERE pr.price_date IS NULL
        ORDER BY t.trade_id
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    I checked all 392 trades against the closing prices: 390 happen on a day their asset has a closing price, and 2 break the rule. They are trade 389 (Ava’s Portfolio 1 buying 5 Apple on Saturday 2025-03-15) and trade 390 (Ava’s Portfolio 2 buying 3 Microsoft on Saturday 2025-08-09), the two rows I broke on purpose in Part A; stocks have no closing price on a Saturday.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Question 8**: Every sell checked against the rule that a portfolio never sells more than it holds, and a list of any that break it. (checks a rule)
    """)
    return


@app.cell
def _(ask):
    ask("""
        WITH sells AS (
            SELECT s.trade_id,
                   s.quantity AS sold,
                   coalesce(sum(CASE WHEN e.side = 'buy' THEN e.quantity
                                     ELSE -e.quantity END), 0) AS held_before
            FROM trades AS s
            LEFT JOIN trades AS e
                ON e.portfolio_id = s.portfolio_id
               AND e.asset_id     = s.asset_id
               AND e.trade_date   < s.trade_date
            WHERE s.side = 'sell'
            GROUP BY s.trade_id, s.quantity
        )
        SELECT count(*) AS sells_checked,
               sum(CASE WHEN sold > held_before THEN 1 ELSE 0 END) AS breaking_the_rule
        FROM sells
    """)
    return


@app.cell
def _(ask):
    ask("""
        WITH sells AS (
            SELECT s.trade_id,
                   s.trade_date,
                   s.portfolio_id,
                   s.asset_id,
                   s.quantity AS sold,
                   coalesce(sum(CASE WHEN e.side = 'buy' THEN e.quantity
                                     ELSE -e.quantity END), 0) AS held_before
            FROM trades AS s
            LEFT JOIN trades AS e
                ON e.portfolio_id = s.portfolio_id
               AND e.asset_id     = s.asset_id
               AND e.trade_date   < s.trade_date
            WHERE s.side = 'sell'
            GROUP BY s.trade_id, s.trade_date, s.portfolio_id, s.asset_id, s.quantity
        )
        SELECT x.trade_id,
               x.trade_date,
               p.name AS portfolio,
               a.name AS asset,
               CAST(x.held_before AS DOUBLE) AS held_before,
               CAST(x.sold AS DOUBLE)        AS sold,
               CAST(x.sold - x.held_before AS DOUBLE) AS oversold_by
        FROM sells AS x
        JOIN portfolios AS p ON p.portfolio_id = x.portfolio_id
        JOIN assets     AS a ON a.asset_id     = x.asset_id
        WHERE x.sold > x.held_before
        ORDER BY x.trade_id
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    I checked all 59 sells against what the portfolio held just before each one: 57 follow the rule and 2 break it. Trade 391 (Liam’s Portfolio 1 selling 19 Exxon Mobil on 2025-12-30 while holding 9) and trade 392 (Sofia’s Portfolio 2 selling 10 Johnson & Johnson on 2025-12-29 while holding none) each oversold by 10 units; these are the two rows I broke on purpose in Part A. I counted the holding from all earlier trades of that asset in that portfolio
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Question 9**:Which portfolio made the most profit by 2025-12-31, counting what it still holds at that day's closing prices?
    """)
    return


@app.cell
def _(AS_OF, ask):
    ask(f"""
        WITH cash AS (
            SELECT portfolio_id,
                   sum(CASE WHEN side = 'buy'  THEN quantity * price + fee ELSE 0 END) AS spent,
                   sum(CASE WHEN side = 'sell' THEN quantity * price - fee ELSE 0 END) AS received
            FROM trades
            WHERE trade_date <= DATE '{AS_OF}'
            GROUP BY portfolio_id
        ),
        holdings AS (
            SELECT portfolio_id, asset_id,
                   sum(CASE WHEN side = 'buy' THEN quantity ELSE -quantity END) AS units
            FROM trades
            WHERE trade_date <= DATE '{AS_OF}'
            GROUP BY portfolio_id, asset_id
        ),
        worth AS (
            SELECT h.portfolio_id,
                   sum(h.units * pr.close_price) AS market_value
            FROM holdings AS h
            JOIN prices AS pr
                ON pr.asset_id = h.asset_id
               AND pr.price_date = DATE '{AS_OF}'
            WHERE h.units > 0
            GROUP BY h.portfolio_id
        )
        SELECT p.portfolio_id,
               p.name AS portfolio,
               m.first_name || ' ' || m.last_name AS owner,
               round(CAST(c.spent AS DOUBLE), 2)                       AS spent_on_buys,
               round(CAST(c.received AS DOUBLE), 2)                    AS received_from_sells,
               round(CAST(coalesce(w.market_value, 0) AS DOUBLE), 2)   AS worth_on_as_of,
               round(CAST(coalesce(w.market_value, 0) + c.received - c.spent AS DOUBLE), 2) AS profit,
               round(CAST(100.0 * (coalesce(w.market_value, 0) + c.received - c.spent) / c.spent AS DOUBLE), 1) AS return_pct
        FROM portfolios AS p
        JOIN members AS m ON m.member_id = p.member_id
        JOIN cash    AS c ON c.portfolio_id = p.portfolio_id
        LEFT JOIN worth AS w ON w.portfolio_id = p.portfolio_id
        ORDER BY profit DESC
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Lucas's Portfolio 1 made the most profit by 2025-12-31, \$5,083.46 (a 12.0% return on \$42,285.71 spent). I counted profit as the value of what each portfolio still holds at the 2025-12-31 closing prices, plus money received from sells, minus money spent on buys, with fees included. Liam's Portfolio 1 was the second most profitable (\$4,735.71), but it looks better than it is, because it includes trade 391, which sold 10 Exxon Mobil units it did not hold.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Question 10**: Which assets are the most popular with members: how many different members have bought each one, and how much money went into it?
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT a.name AS asset,
               a.asset_type,
               count(DISTINCT p.member_id)    AS members,
               count(DISTINCT t.portfolio_id) AS portfolios,
               count(*)                       AS buys,
               round(CAST(sum(t.quantity * t.price) AS DOUBLE), 2) AS money_invested
        FROM trades AS t
        JOIN portfolios AS p ON p.portfolio_id = t.portfolio_id
        JOIN assets     AS a ON a.asset_id     = t.asset_id
        WHERE t.side = 'buy'
        GROUP BY a.name, a.asset_type
        ORDER BY members DESC, money_invested DESC
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Three assets were bought by every one of the 13 members who have a portfolio: Solana, Ethereum and Johnson & Johnson. Crypto in general was very popular: Solana and Ethereum are first and second in the table, Ethereum is in the most portfolios (18) and has the most buys (34), and Solana has 32 buys, as many as JPMorgan Chase. But popular is not the same as the most money: students put \$102,073.10 into Solana and Ethereum together (\$53,122.10 and \$48,951.00), less than the \$121,910.02 that went into JPMorgan Chase alone, followed by the Invesco QQQ ETF with \$108,401.71. So crypto was bought often but in smaller amounts. I counted popularity as the number of different members who bought an asset, and money invested as quantity × price of the buys, without fees.
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
    I reached two answers a second way, in code, and each check stops with an error if the two numbers disagree.

    **Check 1, Question 6**: the two ticker rows (SQ and XYZ) add up to the same number of trades and the same value as Block's total computed from `trades` alone. The check reads the Question 6 cells' own results, so it fails if either query changes. To test it, I removed the valid_to condition from Question 6: trades then matched both tickers, and the check stopped with "AssertionError: Question 6 does not add up: 46 vs 24 trades, 43571.11 vs 22765.91". After I put the condition back, the check agreed again.

    **Check 2, Question 2**: the 15 member rows add up to 19 portfolios and 758,705.24 bought; counting the `portfolios` table and summing the buys in `trades` alone gives 19 portfolios and 758,705.25. The one-cent difference comes from rounding each member's total to cents before adding them, which is why the check allows a difference below 0.10.

    **Additional Check (Business Questions)**: I also asked marimo's AI agent to review all ten queries against their written answers; it found no errors, but I rely on these checks, because they run in the notebook.
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
    For Question 9, my agent drafted the answer sentence with dollar amounts written as $5,083.46, $42,285.71 and $4,735.71. **What I changed:** I put a backslash before every dollar sign (\$5,083.46), so marimo shows them as plain text. I did the same in my other answers with dollar amounts.

    **How I knew:** When I pasted the sentence into a markdown cell, most of it came out as squashed italic text with the spaces removed. marimo reads text between two $ signs as a math formula, so everything between the first and the last amount was turned into math. After the change, the cell displayed normally. See the answer cell under Question 9.
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


@app.cell
def _(ask, mo):
    _portfolios = ask("SELECT portfolio_id, name FROM portfolios ORDER BY portfolio_id")
    portfolio_picker = mo.ui.dropdown(
        options={row["name"]: row["portfolio_id"] for row in _portfolios.iter_rows(named=True)},
        value="Lucas's Portfolio 1",
        label="Portfolio",
    )
    portfolio_picker_portfolios = ask("SELECT portfolio_id, name FROM portfolios ORDER BY portfolio_id")
    portfolio_picker = mo.ui.dropdown(
        options={row["name"]: row["portfolio_id"] for row in _portfolios.iter_rows(named=True)},
        value="Lucas's Portfolio 1",
        label="Portfolio",
    )
    portfolio_picker
    return (portfolio_picker,)


@app.cell
def _(AS_OF, ask, portfolio_picker):
    picked_holdings = ask(f"""
        SELECT a.name AS asset,
               CAST(sum(CASE WHEN t.side = 'buy' THEN t.quantity ELSE -t.quantity END) AS DOUBLE) AS units,
               round(CAST(sum(CASE WHEN t.side = 'buy' THEN t.quantity ELSE -t.quantity END)
                          * pr.close_price AS DOUBLE), 2) AS value_on_as_of
        FROM trades AS t
        JOIN assets AS a ON a.asset_id = t.asset_id
        JOIN prices AS pr
            ON pr.asset_id = t.asset_id
           AND pr.price_date = DATE '{AS_OF}'
        WHERE t.portfolio_id = {portfolio_picker.value}
          AND t.trade_date <= DATE '{AS_OF}'
        GROUP BY a.name, pr.close_price
        HAVING sum(CASE WHEN t.side = 'buy' THEN t.quantity ELSE -t.quantity END) > 0
        ORDER BY value_on_as_of DESC
    """)
    picked_holdings
    return (picked_holdings,)


@app.cell
def _(AS_OF, picked_holdings, portfolio_picker):
    import altair as alt

    alt.Chart(picked_holdings).mark_bar().encode(
        x=alt.X("value_on_as_of:Q", title="Value on 2025-12-31 (USD)"),
        y=alt.Y("asset:N", sort="-x", title="Asset"),
    ).properties(
        title=f"What {portfolio_picker.selected_key} holds on {AS_OF}",
        width=520,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    I added a dropdown of the 19 portfolios that changes what a query returns, and a bar chart of the result with both axes titled. Pick a portfolio and the notebook shows, without editing any code, what it holds on 2025-12-31 and what each holding is worth at that day's closing price, largest first. It combines the logic of Question 3 (units bought minus units sold) and Question 9 (units × the closing price on the as_of date).

    What I found: Lucas's Portfolio 1, the most profitable, holds 9 assets worth \$47,219.12 in total, and a third of that is JPMorgan Chase (\$16,223.04). That total matches its value in Question 9, so the tool and Question 9 agree. Ava's Portfolio 1 also has JPMorgan Chase as its biggest holding (\$11,695.68), but spreads its \$32,989.35 over 10 assets, including all three crypto assets; its units are the same as the ones Question 3 lists for it.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. Time Spent
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    I've spent about 10-12 hours in the Database Project if we include both Part A and B
    """)
    return


if __name__ == "__main__":
    app.run()
