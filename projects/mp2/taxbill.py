"""Mini Project 2.
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
    # Mini Project 2
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. The Question

    *Who would use this, and what decision does it help them make? Two or three sentences, in words somebody outside this course would understand.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This tool helps people shopping for a home in Massachusetts who haven’t settled on a town yet. For example, a family can find the towns in a county where a typical single-family home fits their budget and the yearly property tax bill stays under their limit, listed from cheapest bill to highest, and rerun it for a different county, budget, or limit. With different data, the same idea could compare other taxes, like which country has the lowest income tax.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #My Plan Before AI.

    Before you ask your agent anything, open the API's address in your browser and read what comes back. Then write how you would solve it: the steps, in order, in plain words, in five lines or more. Then answer these:

    Which functions will your tool need? For each, what goes in and what comes out?
    Which addresses will they request?
    How will you know you have every record?
    Which check will you use in section 6, and which two numbers should agree?
    """)
    return


@app.cell
def _():
    #For my structure for my mini project, there’s a lot of steps I can take from what we did in notebook 3 and 4. I would start by writing functions so I can reuse them for any county or budget.First I would use GET on /ma/towns to get the towns in the county and their basic info and use the pagination info in each reply to make sure I get every page. Then I would use GET on each town's history to get its numbers for fiscal year 2026 so every town is compared on the same year. From that I would pull out the average home value, the tax rate, and the average bill.I could use a for loop to go through the towns and keep only the ones under the budget and use return for other data points if needed to get other info from my list. Then I would sort the list so the cheapest bill is first and check how I could put it on a table . I could also use for and print to get the results, in both cases I would also use print to show the results in a readable format



    return


if __name__ == "__main__":
    app.run()
