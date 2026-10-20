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


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # My Inputs
    """)
    return


@app.cell
def _():
    import requests

    fiscal_year = 2026

    BASE_URL = "https://oim.zhili.dev/ma"
    return fiscal_year, requests


@app.cell
def _(mo):
    county_dropdown = mo.ui.dropdown(
        options=[
            "Barnstable", "Berkshire", "Bristol", "Dukes", "Essex", "Franklin",
            "Hampden", "Hampshire", "Middlesex", "Nantucket", "Norfolk",
            "Plymouth", "Suffolk", "Worcester",
        ],
        value="Middlesex",
        label="County",
    )
    budget_input = mo.ui.number(start=100000, stop=5000000, step=10000, value=700000, label="Budget ($)")
    tax_limit_input = mo.ui.number(start=1000, stop=50000, step=500, value=8000, label="Tax bill limit ($)")

    mo.vstack([county_dropdown, budget_input, tax_limit_input])
    return budget_input, county_dropdown, tax_limit_input


@app.cell
def _(budget_input, county_dropdown, tax_limit_input):
    county = county_dropdown.value
    budget_dollars = budget_input.value
    tax_limit_dollars = tax_limit_input.value
    return budget_dollars, county, tax_limit_dollars


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Functions
    """)
    return


@app.cell
def _(requests):
    def get_towns(county):
        """Return every town in the county, across all pages."""
        # 1. Ask for page 1, which also tells us how many pages there are
        reply = requests.get(
            "https://oim.zhili.dev/ma/towns",
            params={"county": county, "page": 1, "per_page": 100},
            timeout=10,
        ).json()
        towns = reply["items"]
        pages = reply["pagination"]["pages"]
        total = reply["pagination"]["total"]

        # 2. Ask for any pages after page 1
        for page in range(2, pages + 1):
            next_reply = requests.get(
                "https://oim.zhili.dev/ma/towns",
                params={"county": county, "page": page, "per_page": 100},
                timeout=10,
            ).json()
            towns = towns + next_reply["items"]

        print("Got", len(towns), "of", total, "towns in", county)
        return towns


    def get_year(dor_code, year):
        """Return one town's numbers for one fiscal year, or None if that year is missing."""
        history = requests.get(
            f"https://oim.zhili.dev/ma/towns/{dor_code}/history",
            params={"from_year": year, "to_year": year},
            timeout=10,
        ).json()
        if history["years"]:
            return history["years"][0]
        return None


    def compute_taxbill(value, rate):
        """Return the tax bill: average value x tax rate / 1,000."""
        return value * rate / 1000


    def by_bill(row):
        """Tell sort to sort by the bill."""
        return row["bill"]


    def shortlist(county, budget, tax_limit, year):
        """Return the towns that fit the budget and the tax limit, cheapest bill first."""
        rows = []
        for town in get_towns(county):
            # 1. Get this town's numbers for the year
            record = get_year(town["dor_code"], year)
            if record is None:
                continue
            value = record["average_single_family_value_dollars"]
            rate = record["residential_rate_per_thousand"]
            bill = record["average_single_family_bill_dollars"]
            if value is None or rate is None or bill is None:
                continue

            # 2. Keep it only if it passes both limits
            if value <= budget and bill < tax_limit:
                rows.append({"town": town["name"], "dor_code": town["dor_code"],
                             "value": value, "rate": rate, "bill": bill,
                             "income": town["income_per_capita_dollars"]})

        # 3. Cheapest bill first
        rows.sort(key=by_bill)
        return rows

    return (shortlist,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # THE WORK
    """)
    return


@app.cell
def _(budget_dollars, county, fiscal_year, shortlist, tax_limit_dollars):
    results = shortlist(county, budget_dollars, tax_limit_dollars, fiscal_year)
    return (results,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # THE ANSWER
    """)
    return


@app.cell
def _(budget_dollars, county, fiscal_year, results, tax_limit_dollars):
    def _():
        # 1. The table, with the columns lined up
        print(f"{'Town':<20}{'Avg home value ($)':>20}{'Tax rate':>10}{'Avg bill ($)':>14}")
        print("-" * 64)
        for row in results:
            print(f"{row['town']:<20}{row['value']:>20,}{row['rate']:>10.2f}{row['bill']:>14,}")
        print()

        # 2. One sentence for the couple, built from the data
        if results:
            best = results[0]
            print(f"In {county} County for FY{fiscal_year}, {len(results)} towns have an average home "
                  f"at or under ${budget_dollars:,} and an average tax bill under ${tax_limit_dollars:,}; "
                  f"the cheapest is {best['town']}, where the average home is ${best['value']:,} "
                  f"and the average bill is ${best['bill']:,} (${best['rate']:.2f} per $1,000).")
        else:
            print(f"No town in {county} County has an average home at or under ${budget_dollars:,} "
                  f"with an average bill under ${tax_limit_dollars:,} in FY{fiscal_year}.")


    _()
    return


@app.cell
def _():
    # in the above, I have my shortlist of 12 towns with an average home <= $700,000 and an average property tax bill < $8,000. In this table, the avg tax bill per town is sorted by lowest to highest, with Malden having the lowest avg bill at $4,952.
    return


@app.cell
def _(results):
    def by_rate(row):
        """Tell sort to sort by the tax rate."""
        return row["rate"]


    results_by_rate = sorted(results, key=by_rate)
    results_by_rate
    return


@app.cell
def _(mo, results):
    towns_table = []
    for row in results:
        towns_table.append({
            "Town": row["town"],
            "Average home value ($)": row["value"],
            "Residential tax rate": row["rate"],
            "Average bill ($)": row["bill"],
        })

    mo.ui.table(towns_table)
    return


@app.cell
def _():
    #above I have the same results also sorted from lowest to highest average tax bill but in an UI that is more nice to visualize and understand
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # GOING FURTHER
    """)
    return


@app.cell
def _(mo, results):
    def _():
        def by_rate(row):
            """Tell sort to sort by the residential tax rate."""
            return row["rate"]


        def _():
            # 1. Make a new list sorted by tax rate, lowest first (results stays sorted by bill)
            by_rate_results = sorted(results, key=by_rate)

            # 2. Build the table the same way as before
            rate_table = []
            for rank, row in enumerate(by_rate_results, start=1):
                rate_table.append({
                    "Rank by rate": rank,
                    "Town": row["town"],
                    "Residential tax rate": row["rate"],
                    "Average home value ($)": row["value"],
                    "Average bill ($)": row["bill"],
                })

            # 3. Does the order change?
            bill_order = [row["town"] for row in results]
            rate_order = [row["town"] for row in by_rate_results]
            print("Same order as by bill?", bill_order == rate_order)

            return mo.ui.table(rate_table)
        return _()


    _()
    return


@app.cell
def _():
    # When ranking by tax rate and town the results now change and now Dracut is placed at the top, being the town with the lowest rate for homes within the budget and under the average bill. These results are different than the initial ones we had since the average bill in this case is still higher (5,737 vs Malden at 4,952). Ultimately, the results are different because the bill depends on both the rate and the home value, but ranking by rate ignores home value, so towns with cheaper homes move up the bill list even if their rate is higher.
    return


@app.cell
def _(fiscal_year, mo, requests, results):
    def get_bill_history(dor_code, from_year, to_year):
        """Return a town's yearly records between two fiscal years."""
        history = requests.get(
            f"https://oim.zhili.dev/ma/towns/{dor_code}/history",
            params={"from_year": from_year, "to_year": to_year},
            timeout=10,
        ).json()
        return history["years"]


    def _():
        start_year = fiscal_year - 10
        top_three = results[:3]

        # 1. One row per year, one column per town
        bill_table = []
        for year in range(start_year, fiscal_year + 1):
            bill_table.append({"Fiscal year": year})

        for row in top_three:
            years = get_bill_history(row["dor_code"], start_year, fiscal_year)
            for record in years:
                for table_row in bill_table:
                    if table_row["Fiscal year"] == record["fiscal_year"]:
                        table_row[row["town"] + " bill ($)"] = record["average_single_family_bill_dollars"]

            # 2. How much the bill changed, using only the years that actually have a bill
            years_with_data = [
                record for record in years
                if record["average_single_family_bill_dollars"] is not None
            ]
            if years_with_data:
                first_record = years_with_data[0]
                last_record = years_with_data[-1]
                first_bill = first_record["average_single_family_bill_dollars"]
                last_bill = last_record["average_single_family_bill_dollars"]
                change = last_bill - first_bill
                percent = change / first_bill * 100
                print(f"{row['town']}: ${first_bill:,} in FY{first_record['fiscal_year']} to "
                      f"${last_bill:,} in FY{last_record['fiscal_year']}, "
                      f"up ${change:,} ({percent:.0f}%)")
            else:
                print(f"{row['town']}: no bill history available in this range.")

        return mo.ui.table(bill_table)


    _()
    return


@app.cell
def _(mo, results):
    def _():
        income_table = []
        for row in results:
            # Bill as a share of income per person, in percent
            share = row["bill"] / row["income"] * 100
            income_table.append({
                "Town": row["town"],
                "Average bill ($)": row["bill"],
                "Income per person ($)": row["income"],
                "Bill as % of income": round(share, 1),
            })

        # One sentence for the cheapest town
        if results:
            best = results[0]
            best_share = best["bill"] / best["income"] * 100
            print(f"In {best['town']}, the average bill of ${best['bill']:,} is "
                  f"{best_share:.1f}% of the income per person (${best['income']:,}).")

        return mo.ui.table(income_table)


    _()
    return


if __name__ == "__main__":
    app.run()
