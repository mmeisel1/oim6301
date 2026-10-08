# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
# ]
# ///
"""Mini Project 1.
"""

import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium", sql_output="polars")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Mini Project 1

    Your choice of option, what each one asks for, the due date and how it is graded are on the Mini Project 1 page of the course site, linked from the calendar. This notebook is the shape to build it in. Keep the headings, and replace each line in italics with your own.

    Save it in your course repository as `projects/mp1/<your-tool>.py`, named for what it does, such as `loan-schedule.py`, and open it with `uv run marimo edit`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. The Question

    *Who would use this, and what decision does it help them make? Two or three sentences, in words somebody outside this course would understand.*
    """)
    return


@app.cell
def _():
    #This tool is for anyone taking out a large, long-term loan, such as a homebuyer choosing between different terms for a mortgage (common terms like 15,30 years). It shows the monthly payment, the total interest, and the remaining balance for each option side by side, and lets them plug in their own lender’s quote. That helps them decide whether a lower monthly payment is worth paying more interest over the life of the loan.
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. My Plan Before AI

    *Before you ask your agent anything, write how you would solve it: the steps, in order, in plain words, in five lines or more. Then answer these two questions:*

    - *What does your loop carry from one step to the next, the way a running total carries its sum?*
    - *Which check will you use in section 6, and which two numbers should agree?*

    *Commit this notebook with the message `mp1: plan before AI`.*
    """)
    return


@app.cell
def _():
    #My loop carries the remaining balance to the next month since each month it uses the current balance to find out what the month’s interest is, subtracts the principal paid, and passes the new balance on to the next month.
    return


@app.cell
def _():
    #I would check that all the principal paid is equal to the original amount borrowed
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Inputs

    Every number the project starts from goes in the cell below, and nowhere else, so that changing one input changes every result after it.

    Copy in the default inputs for your option from the Mini Project 1 page. If you chose D, your own option, type your data in here, or ask your agent to generate it with `faker`. The required part reads no file.
    """)
    return


@app.cell
def _():
    loan_amount = 400000
    annual_rates = {30: 0.0703, 15: 0.0642}
    return annual_rates, loan_amount


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. The Work

    Add as many cells as you need. Try each step yourself before you ask your agent, and commit as you go.
    """)
    return


@app.cell
def _(annual_rates, loan_amount):
    loan_options = []
    for years, annual_rate in annual_rates.items():
        monthly_rate = annual_rate / 12
        months = years * 12
        payment = loan_amount * monthly_rate / (1 - (1 + monthly_rate) ** -months)

        balance = loan_amount
        principal_paid = 0.0
        interest_paid = 0.0

        for month in range(months):
            interest = balance * monthly_rate
            principal = payment - interest
            balance = balance - principal
            principal_paid = principal_paid + principal
            interest_paid = interest_paid + interest

        loan_options.append({
            "years": years,
            "payment": payment,
            "principal_paid": principal_paid,
            "interest_paid": interest_paid,
            "ending_balance": balance,
        })

    for option in loan_options:
        print(f"{option['years']}-year: ${option['payment']:,.2f} per month")
        print(f"   principal paid ${option['principal_paid']:,.2f}   interest paid ${option['interest_paid']:,.2f}   ending balance ${abs(option['ending_balance']):,.2f}")
    return (loan_options,)


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. The Answer

    *A table of your results in the cell below, printed with `print` and f-strings, then one sentence here that answers the question in section 1, with the number in it.*
    """)
    return


@app.cell
def _(loan_amount, loan_options):
    def _():
        print(f"{'Term':<12}{'Monthly payment':>18}{'Total interest':>18}{'Total paid':>18}")
        print("-" * 66)

        for option in loan_options:
            total_paid = loan_amount + option["interest_paid"]
            print(f"{str(option['years']) + '-year':<12}{option['payment']:>18,.2f}{option['interest_paid']:>18,.2f}{total_paid:>18,.2f}")

        print("-" * 66)
        payment_15 = [option["payment"] for option in loan_options if option["years"] == 15][0]
        payment_30 = [option["payment"] for option in loan_options if option["years"] == 30][0]
        interest_15 = [option["interest_paid"] for option in loan_options if option["years"] == 15][0]
        interest_30 = [option["interest_paid"] for option in loan_options if option["years"] == 30][0]

        payment_diff = payment_15 - payment_30
        interest_diff = interest_30 - interest_15
        return print(f"{'Difference':<12}{payment_diff:>18,.2f}{interest_diff:>18,.2f}{interest_diff:>18,.2f}")


    _()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. How I Know These Numbers Are Right

    *At least one check that reaches a result a second, independent way. Name what you compared and what came out.*
    """)
    return


@app.cell
def _(loan_amount, loan_options):
    for _option in loan_options:
        _months = _option["years"] * 12
        _total_paid_check = _option["payment"] * _months
        _interest_check = _total_paid_check - loan_amount

        _principal_ok = round(_option["principal_paid"], 2) == loan_amount
        _interest_ok = round(_option["interest_paid"], 2) == round(_interest_check, 2)

        print(f"{_option['years']}-year check:")
        print(f"  principal paid matches loan amount?     {_principal_ok}   (${_option['principal_paid']:,.2f} vs ${loan_amount:,.2f})")
        print(f"  interest paid matches independent calc? {_interest_ok}   (${_option['interest_paid']:,.2f} vs ${_interest_check:,.2f})")
    return


@app.cell
def _():
    960938.64-560938.64
    return


@app.cell
def _():
    624035.15-224035.15
    return


@app.cell
def _():
    #I looked at the Total Paid per mortgage term (15 years, 30 years) and then I subtracted the total interest paid. In both cases I got the total amount to match the original loan amount which was 400k. I also asked my AI to build a way to check it  and it did and showed true because it matched
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. Working With the Agent

    *Pick one piece of AI output you did not accept as-is. What did it give you, what did you change, and how did you know? Point to the commit or the cell.*

    *If the agent got it right the first time: what did you do to verify that?*
    """)
    return


@app.cell
def _():
    #the agent didn't get it perfectly right the first time but it I used the ai to fixed it and it was seconds of fixing and just clicking on keeping change and it gave me the answers we needed. I also wanted to use the AI agent to help me check my numbers in a more complex way and it did verify that the answers were in fact TRUE and matching the original loan amount. I also did it manually to ensure all answers were aligned
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Going Further

    *Take at least one step past the main task, in any direction, and use your agent as much as you like. It does not have to work. State what you tried, what you found, and where it is in this notebook.*
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### What if you pay an extra $200 a month?

    Plan A is the original schedule. Plan B pays the same loan, but adds $200 to every monthly payment. The extra money goes straight to principal, so the loan is paid off early and less interest builds up along the way.
    """)
    return


@app.cell
def _(annual_rates, loan_amount, loan_options):
    extra_payment = 200

    extra_payment_options = []
    for _option in loan_options:
        _years = _option["years"]
        _annual_rate = annual_rates[_years]
        _monthly_rate = _annual_rate / 12
        _new_payment = _option["payment"] + extra_payment

        _balance = loan_amount
        _interest_paid = 0.0
        _months_taken = 0

        while _balance > 0:
            _interest = _balance * _monthly_rate
            _principal = _new_payment - _interest
            _balance = _balance - _principal
            _interest_paid = _interest_paid + _interest
            _months_taken = _months_taken + 1

        extra_payment_options.append({
            "years": _years,
            "payment": _new_payment,
            "interest_paid": _interest_paid,
            "months_taken": _months_taken,
        })

    extra_payment_options
    return (extra_payment_options,)


@app.cell
def _(extra_payment_options, loan_amount, loan_options):
    def _():
        print(f"{'Term':<10}{'Plan':<8}{'Monthly payment':>18}{'Total interest':>18}{'Total paid':>18}{'Months to pay off':>20}")
        print("-" * 92)

        for _a, _b in zip(loan_options, extra_payment_options):
            _term = _a["years"]
            _months_a = _term * 12
            _total_paid_a = loan_amount + _a["interest_paid"]
            _total_paid_b = loan_amount + _b["interest_paid"]

            print(f"{str(_term) + '-year':<10}{'A':<8}{_a['payment']:>18,.2f}{_a['interest_paid']:>18,.2f}{_total_paid_a:>18,.2f}{_months_a:>20}")
            print(f"{'':<10}{'B':<8}{_b['payment']:>18,.2f}{_b['interest_paid']:>18,.2f}{_total_paid_b:>18,.2f}{_b['months_taken']:>20}")

            _payment_diff = _b["payment"] - _a["payment"]
            _interest_diff = _a["interest_paid"] - _b["interest_paid"]
            _total_paid_diff = _total_paid_a - _total_paid_b
            _months_diff = _months_a - _b["months_taken"]

            print(f"{'':<10}{'Diff':<8}{_payment_diff:>18,.2f}{_interest_diff:>18,.2f}{_total_paid_diff:>18,.2f}{_months_diff:>20}")
            print("-" * 92)


    _()
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Refinancing the 30-year loan after 5 years

    After 5 years (60 months) of paying the original 30-year loan, the rate drops to 6% and refinancing costs $6,000. This finds the balance remaining at that point, the new monthly payment, and the month at which the savings from refinancing overtake the $6,000 cost.
    """)
    return


@app.cell
def _(annual_rates, loan_amount):
    def _():
        original_rate = annual_rates[30]
        original_monthly_rate = original_rate / 12
        original_months = 30 * 12
        original_payment = loan_amount * original_monthly_rate / (1 - (1 + original_monthly_rate) ** -original_months)

        months_before_refi = 60
        balance = loan_amount
        for _month in range(months_before_refi):
            interest = balance * original_monthly_rate
            principal = original_payment - interest
            balance = balance - principal

        balance_at_refi = balance

        new_rate = 0.06
        new_monthly_rate = new_rate / 12
        months_remaining = original_months - months_before_refi
        new_payment = balance_at_refi * new_monthly_rate / (1 - (1 + new_monthly_rate) ** -months_remaining)

        monthly_savings = original_payment - new_payment
        refi_cost = 6000

        savings_so_far = 0.0
        month_savings_overtake_cost = None
        for _month in range(1, months_remaining + 1):
            savings_so_far = savings_so_far + monthly_savings
            if savings_so_far >= refi_cost and month_savings_overtake_cost is None:
                month_savings_overtake_cost = _month

        print(f"Balance remaining after 5 years: ${balance_at_refi:,.2f}")
        print(f"Original payment: ${original_payment:,.2f}   New payment at 6%: ${new_payment:,.2f}")
        print(f"Monthly savings: ${monthly_savings:,.2f}")
        return print(f"Savings overtake the ${refi_cost:,.2f} refinancing cost in month {month_savings_overtake_cost} after refinancing.")


    _()
    return


@app.cell
def _():
    #sliders
    return


@app.cell
def _(mo):
    rate_30_slider = mo.ui.slider(start=3.0, stop=10.0, step=0.01, value=7.03,
                                  label="30-year rate (%)", show_value=True)
    rate_15_slider = mo.ui.slider(start=3.0, stop=10.0, step=0.01, value=6.42,
                                  label="15-year rate (%)", show_value=True)
    extra_slider = mo.ui.slider(start=0, stop=1000, step=50, value=0,
                                label="Extra payment each month ($)", show_value=True)

    mo.vstack([rate_30_slider, rate_15_slider, extra_slider])
    return extra_slider, rate_15_slider, rate_30_slider


@app.cell
def _(loan_amount):
    def run_loan(annual_rate, years, extra):
        r = annual_rate / 12
        n = years * 12
        payment = round(loan_amount * r / (1 - (1 + r) ** -n), 2)

        balance = loan_amount
        total_interest = 0
        months = 0

        while balance > 0:
            months = months + 1
            interest = round(balance * r, 2)
            principal = payment + extra - interest
            if principal > balance or months == n:   # last payment clears the balance
                principal = balance
            balance = round(balance - principal, 2)
            total_interest = round(total_interest + interest, 2)

        return payment, months, total_interest

    return (run_loan,)


@app.cell
def _(extra_slider, rate_15_slider, rate_30_slider, run_loan):
    def _():
        slider_rates = {30: rate_30_slider.value / 100, 15: rate_15_slider.value / 100}
        extra = extra_slider.value

        print(f"{'Term':<10}{'Payment':>12}{'Months':>9}{'Interest':>15}{'Months saved':>14}{'Interest saved':>16}")
        print("-" * 76)

        for years, rate in slider_rates.items():
            payment, months, interest = run_loan(rate, years, extra)
            base_payment, base_months, base_interest = run_loan(rate, years, 0)
            print(f"{str(years) + '-year':<10}{payment + extra:>12,.2f}{months:>9}{interest:>15,.2f}"
                  f"{base_months - months:>14}{base_interest - interest:>16,.2f}")


    _()
    return


@app.cell
def _(loan_amount):
    def build_balance_rows(annual_rate, years, extra):
        r = annual_rate / 12
        n = years * 12
        payment = round(loan_amount * r / (1 - (1 + r) ** -n), 2)

        balance = loan_amount
        month = 0
        rows = []

        while balance > 0:
            month = month + 1
            interest = round(balance * r, 2)
            principal = payment + extra - interest
            if principal > balance or month == n:
                principal = balance
            balance = round(balance - principal, 2)
            rows.append({"Month": month, "Balance": balance})

        return rows

    return (build_balance_rows,)


@app.cell
def _(build_balance_rows, extra_slider, rate_15_slider, rate_30_slider):
    import polars as pl
    import altair as alt

    _rate_30 = rate_30_slider.value / 100
    _rate_15 = rate_15_slider.value / 100
    _extra = extra_slider.value

    _rows_30 = build_balance_rows(_rate_30, 30, _extra)
    for _row in _rows_30:
        _row["Loan"] = "30-year"

    _rows_15 = build_balance_rows(_rate_15, 15, _extra)
    for _row in _rows_15:
        _row["Loan"] = "15-year"

    balance_df = pl.DataFrame(_rows_30 + _rows_15)

    alt.Chart(balance_df).mark_line().encode(
        x=alt.X("Month", title="Month"),
        y=alt.Y("Balance", title="Remaining balance ($)"),
        color=alt.Color("Loan", title="Loan"),
        tooltip=["Loan", "Month", "Balance"],
    ).properties(
        title="Loan balance over time",
        width=600,
        height=350,
    )
    return


if __name__ == "__main__":
    app.run()
