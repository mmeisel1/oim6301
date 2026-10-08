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


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. Working With the Agent

    *Pick one piece of AI output you did not accept as-is. What did it give you, what did you change, and how did you know? Point to the commit or the cell.*

    *If the agent got it right the first time: what did you do to verify that?*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Going Further

    *Take at least one step past the main task, in any direction, and use your agent as much as you like. It does not have to work. State what you tried, what you found, and where it is in this notebook.*
    """)
    return


if __name__ == "__main__":
    app.run()
