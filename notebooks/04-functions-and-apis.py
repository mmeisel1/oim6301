# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "requests",
# ]
# ///
"""Functions and APIs.
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
    # Functions and APIs

    This session moves between two notebooks. It opens with section 4 of notebook 3, `03-collections-and-apis.py`, then comes here for section 1, on functions. After the break it goes back for section 5 of notebook 3, the first requests to a server, and returns here for the rest: reading an API built for this course, and sending data to it.

    | | |
    |---|---|
    | ✏️ | Your turn. Add cells with the **+** button |
    | 🚀 | This week's work |

    For a written answer, add a cell under the question, open the cell's **⋯** menu and choose **Convert to Markdown**.

    Every ✏️ is part of this week's work. Those marked **Advanced** are optional; try them once the rest is done.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Work with your agent the same way as in notebook 3.** Try it yourself first, or write the steps in words. Then ask your agent, ask it to explain any line you could not have written, and ask which concepts its answer used.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 1. Functions

    Notebooks 2 and 3 each computed what the portfolio costs, and each time the loop was written out again. A **function** gives that work a name, so it is written once and used on any portfolio.

    You have called functions since the first day: `len(...)`, `round(...)`, `print(...)`. Each takes something in and gives something back, the way `SUM(A1:A6)` does in a spreadsheet.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Start with the smallest one:

    - `def` starts a function.
    - `add_tax` is its name, a verb and a noun for what it does.
    - `amount` in brackets is its **parameter**, what it takes in.
    - `return` is what it gives back.

    Defining it runs nothing; it runs each time it is called. Massachusetts sales tax is 6.25%, so the function multiplies by 1.0625.
    """)
    return


@app.function
def add_tax(amount):
    return round(amount * 1.0625, 2)


@app.cell
def _():
    add_tax(100)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    If the tax rate changes, you edit the one line inside `add_tax`, and every call uses the new rate.
    """)
    return


@app.cell
def _():
    holdings = [
        ("AAPL", 100, 173.93),
        ("MSFT", 50, 319.53),
        ("GOOG", 80, 131.36),
        ("AMZN", 200, 129.33),
        ("NVDA", 20, 410.17),
        ("TSLA", 150, 255.70),
    ]
    holdings
    return (holdings,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Names inside a function belong to that function.** `symbol`, `shares` and `cost_so_far` exist only while it runs, so they need no underscore, and two functions can each use `price` without colliding.
    """)
    return


@app.function
def compute_cost(portfolio):
    cost_so_far = 0
    for symbol, shares, price in portfolio:
        cost_so_far = cost_so_far + shares * price
    return round(cost_so_far, 2)


@app.function
def compute_cost2(portfolio):
    cost_so_far = 0
    for stock in portfolio:
        print(stock)
        stock_cost = stock[1] * stock[2]
        cost_so_far += stock_cost
        
        return round(cost_so_far, 2)


@app.cell
def _(holdings):
    compute_cost2(holdings)
    return


@app.cell
def _(holdings):
    compute_cost(holdings)
    return


@app.cell
def _(holdings):
    for stock in holdings:
        print(stock, type(stock), len(stock))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    A second client holds two funds and one stock. The same function answers for them, with no new loop.
    """)
    return


@app.cell
def _():
    retirement_holdings = [
        ("VTI", 120, 228.40),
        ("BND", 300, 72.15),
        ("AAPL", 40, 173.93),
    ]
    retirement_holdings
    return (retirement_holdings,)


@app.cell
def _(retirement_holdings):
    compute_cost(retirement_holdings)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Why programs are built from functions:**

    - **A change happens in one place.** Add a trading fee inside `compute_cost` and every portfolio's cost follows.
    - **The name says what the work is for.** `compute_cost(retirement_holdings)` reads as a sentence; a loop has to be read line by line.
    - **Everything it needs comes in through the brackets.** So you can test it on a portfolio whose answer you already know, such as notebook 3's $116,302.70.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ✏️ A · Functions of your own

    1. Add a cell that defines `count_shares(portfolio)`. It returns the total number of shares in a portfolio. Call it on both portfolios. *Check yourself: `600` and `460`.*
    2. Add a cell that defines `find_largest(portfolio)`. It returns the ticker and the cost of the holding that cost the most, as a tuple. Call it on both portfolios. *Check yourself: `('TSLA', 38355.0)` and `('VTI', 27408.0)`.*

    **Going further.** Add a second parameter, `n`, and return the `n` largest holdings, largest first.
    """)
    return


@app.function
def count_shares(portfolio):
    """Return the total number of shares across all positions."""
    return sum(shares for _, shares, _ in portfolio)


@app.cell
def _(holdings):
    print(count_shares(holdings))    # 600
    return


@app.cell
def _(retirement_holdings):
    print(count_shares(retirement_holdings))
    return


@app.function
def find_largest(portfolios):
    largest = None
    for ticker,shares,prices in portfolios:
        if largest is None or shares > largest:
            largest = shares
    return largest


@app.cell
def _(holdings, retirement_holdings):
    def _():
        def find_largest(portfolio):
            """Return (ticker, cost) for the holding with the highest total cost."""
            ticker, shares, price = max(portfolio, key=lambda pos: pos[1] * pos[2])
            return (ticker, shares * price)

        print(find_largest(holdings))
        return print(find_largest(retirement_holdings))


    _()
    return


@app.cell
def _(holdings, retirement_holdings):
    def _():
        def find_largest(portfolio, n=1):
            """Return a list of (ticker, cost) for the n most expensive holdings, largest first."""
            costs = [(ticker, shares * price) for ticker, shares, price in portfolio]
            costs.sort(key=lambda item: item[1], reverse=True)
            return costs[:n]

        print(find_largest(holdings, 3))
        return print(find_largest(retirement_holdings, 3))


    _()
    return


@app.cell
def _(holdings):
    print(find_largest(holdings))
    return


@app.cell
def _(retirement_holdings):
    print(find_largest(retirement_holdings))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ✏️ B · Without `return`

    Copy `count_shares` into a new cell under a new name, and put `print(...)` where the `return` was. Call it and keep the result in a name. In a markdown cell under it, answer: what does that name hold, and what could the next cell do with it?
    """)
    return


@app.function
def count_shares_print(portfolio):
    print(sum(shares for _, shares, _ in portfolio))


@app.function
def print_shares(portfolio):
    """Return the total number of shares across all positions."""
    print(sum(shares for _, shares, _ in portfolio))


@app.cell
def _(holdings):
    a=print_shares(holdings)
    return (a,)


@app.cell
def _(a):
    print(a)
    return


@app.cell
def _():
    # my name (a) holds None. The function prints 600 on the screen, but because it has no return, it doesn’t give the number back, so nothing useful is stored in a. I can't do much with my name. For example, a + 10 would give an error, because you can’t do maths with None.Print shows a value to a person; return gives the value back so code can use it.
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 2. Calling an API

    Calling an **API** is like calling a function someone else wrote, running on their computer. You call it with a web address, their server runs its code, and the result comes back to you.

    | | Calling a function you wrote | Calling an API |
    |---|---|---|
    | **You call it with** | `get_towns("Norfolk")` | `oim.zhili.dev/ma/towns?county=Norfolk` |
    | **What goes in** | parameters in brackets | parameters after `?` |
    | **What comes back** | the `return` value | a reply, usually JSON |
    | **When it goes wrong** | an error in your notebook | a status code and a message |
    | **Where it runs** | your laptop | somebody else's server |

    You cannot see the code behind an API, so its documentation is how you learn its parameters and what it returns.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The course runs its own API at `oim.zhili.dev`. Its Massachusetts endpoints come from the state's [Division of Local Services](https://www.mass.gov/info-details/division-of-local-services-municipal-databank): every city and town, its population and income, and its property tax rates and bills. The documentation is at [oim.zhili.dev/docs](https://oim.zhili.dev/docs), and the API also lists its own endpoints. **Before any code**, open [oim.zhili.dev/mass](https://oim.zhili.dev/mass) and [oim.zhili.dev/ma/towns?county=Norfolk](https://oim.zhili.dev/ma/towns?county=Norfolk) in your browser and read what comes back.
    """)
    return


@app.cell
def _():
    import requests

    return (requests,)


@app.cell
def _(requests):
    ma_endpoints = requests.get("https://oim.zhili.dev/ma", timeout=10).json()
    ma_endpoints
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `/ma/towns` takes a `county`. Pass parameters as a dictionary with `params=`, and `requests` builds the address. `.url` shows the address it built.
    """)
    return


@app.cell
def _(requests):
    norfolk_reply = requests.get(
        "https://oim.zhili.dev/ma/towns",
        params={"county": "Norfolk"},
        timeout=10,
    )
    norfolk_reply.status_code, norfolk_reply.url
    return (norfolk_reply,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Why a dictionary.** A value with a space in it has to be encoded before it can go in an address, and `params=` does that for you. Ask for `{"name": "West Newbury"}` and `.url` ends in `name=West+Newbury`.

    The reply is a dictionary with two keys. `pagination` states how much there is.
    """)
    return


@app.cell
def _(norfolk_reply):
    norfolk_page = norfolk_reply.json()
    norfolk_page["pagination"]
    return (norfolk_page,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `items` is a table: a list of records, one per town, the same shape as the orders in notebook 2.
    """)
    return


@app.cell
def _(norfolk_page):
    norfolk_page["items"][0]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Wrap the request in a function and the endpoint becomes a Python function. `get_towns` takes a county and returns its towns, and the cell that calls it never sees the address.
    """)
    return


@app.cell
def _(requests):
    def get_towns(county):
        towns_reply = requests.get(
            "https://oim.zhili.dev/ma/towns",
            params={"county": county},
            timeout=10,
        )
        return towns_reply.json()["items"]

    return (get_towns,)


@app.cell
def _(get_towns):
    get_towns("Suffolk")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ✏️ Weather by Town

    In notebook 3 you searched Open-Meteo for a town (F) and asked for the weather at a pair of coordinates. Put the two requests in one function.

    Add a cell that defines `get_temperature(town)`. It searches for `town` with `count=1`, takes the latitude and longitude of the first result, asks for the current temperature in °F, and returns that number. Then call it: `get_temperature("Wellesley")`.

    *Check yourself: within a degree or two of notebook 3's reading at Babson, since Wellesley is next door.*

    **Going further.** Try `get_temperature("Babson Park")`. Add a second parameter, `state`, so the function uses the first place in that state.
    """)
    return


@app.cell
def _():
    def _():
        import requests

        def get_temperature(town):
            # 1. Search for the town and take the first result
            search = requests.get(
                "https://geocoding-api.open-meteo.com/v1/search",
                params={"name": town, "count": 1},
            ).json()
            place = search["results"][0]

            # 2. Ask for the current temperature at that place's coordinates
            weather = requests.get(
                "https://api.open-meteo.com/v1/forecast",
                params={
                    "latitude": place["latitude"],
                    "longitude": place["longitude"],
                    "current": "temperature_2m",
                    "temperature_unit": "fahrenheit",
                },
            ).json()

            return weather["current"]["temperature_2m"]


    _()
    return


@app.cell
def _(requests):
    def get_temperature(town):
        # 1. Search for the town and take the first result
        search = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": town, "count": 1},
        ).json()
        place = search["results"][0]

        # 2. Ask for the current temperature at that place's coordinates
        weather = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": place["latitude"],
                "longitude": place["longitude"],
                "current": "temperature_2m",
                "temperature_unit": "fahrenheit",
            },
        ).json()

        return weather["current"]["temperature_2m"]


    get_temperature("Wellesley")
    return


@app.cell
def _(requests):
    def _():
        def get_temperature(town, state):
            # 1. Search for the town, then take the first result in the given state
            search = requests.get(
                "https://geocoding-api.open-meteo.com/v1/search",
                params={"name": town, "count": 10},
            ).json()
            for result in search["results"]:
                if result.get("admin1") == state:
                    place = result
                    break

            # 2. Ask for the current temperature at that place's coordinates
            weather = requests.get(
                "https://api.open-meteo.com/v1/forecast",
                params={
                    "latitude": place["latitude"],
                    "longitude": place["longitude"],
                    "current": "temperature_2m",
                    "temperature_unit": "fahrenheit",
                },
            ).json()

            return weather["current"]["temperature_2m"]
        return print(get_temperature("Babson Park", "Massachusetts"))


    _()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ✏️ C · Read the documentation

    Open [oim.zhili.dev/docs](https://oim.zhili.dev/docs) and find `/ma/towns`. Use its parameters to ask for the five Norfolk towns with the highest income per person, highest first. Let the server do the sorting.

    *Check yourself: Dover, Wellesley, Cohasset, Needham, Westwood.*
    """)
    return


@app.cell
def _():
    {
      "items": [
        {
          "dor_code": "317",
          "name": "Wellesley",
          "county": "string",
          "type": "string",
          "area_square_miles": 0,
          "founded_year": 0,
          "population": 0,
          "income_per_capita_dollars": 0,
          "equalized_value_dollars": 0,
          "equalized_value_per_capita_dollars": 0,
          "data_fiscal_year": 0,
          "average_single_family_value_dollars": 0,
          "average_single_family_bill_dollars": 0,
          "finances_fiscal_year": 0
        }
      ],
      "pagination": {
        "page": 0,
        "per_page": 0,
        "total": 0,
        "pages": 0,
        "has_next": True,
        "has_prev": True
      }
    }
    return


@app.cell
def _(requests):
    response = requests.get(
        "https://oim.zhili.dev/ma/towns",
        params={"county": "Norfolk", "sort": "income", "order": "desc", "per_page": 5},
    ).json()

    for town in response["items"]:
        print(town["name"], town["income_per_capita_dollars"])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ✏️ D · From a Name to a History

    1. Find Wellesley's `dor_code` with the `name` parameter of `/ma/towns`.
    2. Use it to ask `/ma/towns/{dor_code}/history` for fiscal year 2026.
    3. Check the bill a second way: the average value times the tax rate, divided by 1,000.

    *Check yourself: `317`. Then $2,020,758 × 10.17 / 1,000 = $20,551.11, and the reply's bill is $20,551.*

    **Going further.** Write `town_history(name)`, which takes a town's name, makes both requests, and returns the history.
    """)
    return


@app.cell
def _(requests):
    def _():
        # Find Wellesley's dor_code with the name parameter
        towns = requests.get(
            "https://oim.zhili.dev/ma/towns",
            params={"name": "Wellesley"},
        ).json()
        town = towns["items"][0]
        dor_code = town["dor_code"]
        print(town["name"], dor_code)

        # 1. Ask the history endpoint for fiscal year 2026 only
        history = requests.get(
            f"https://oim.zhili.dev/ma/towns/{dor_code}/history",
            params={"from_year": 2026, "to_year": 2026},
        ).json()
        fy2026 = history["years"][0]
        print(fy2026)

        # 2. Check the bill: average value x tax rate / 1,000
        value = fy2026["average_single_family_value_dollars"]
        rate = fy2026["residential_rate_per_thousand"]
        bill = fy2026["average_single_family_bill_dollars"]

        computed = value * rate / 1000
        print("Reported bill:", bill)
        return print("Computed bill:", round(computed))


    _()
    return


@app.cell
def _(requests):
    def town_history(name):
        """Return the yearly finance history for the town with this name."""
        # 1. Find the town's dor_code
        towns = requests.get(
            "https://oim.zhili.dev/ma/towns",
            params={"name": name},
        ).json()
        for town in towns["items"]:
            if town["name"].lower() == name.lower():
                dor_code = town["dor_code"]
                break

        # 2. Ask for that town's history
        history = requests.get(
            f"https://oim.zhili.dev/ma/towns/{dor_code}/history",
        ).json()
        return history["years"]


    wellesley = town_history("Wellesley")
    print(len(wellesley), "years")
    print(wellesley[-1])
    return (town_history,)


@app.cell
def _(town_history):
    for year in town_history("Dover"):
        print(year["fiscal_year"], year["average_single_family_bill_dollars"])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 3. More Than One Page

    Leave `county` out and `/ma/towns` has every town in the state to give you. Read how many it sends.
    """)
    return


@app.cell
def _(requests):
    state_first_page = requests.get("https://oim.zhili.dev/ma/towns", timeout=10).json()
    len(state_first_page["items"]), state_first_page["pagination"]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Why a server sends pages.** It answers many people at once, so it limits what one request can cost it. The course shop has more than 15,000 orders behind `/shop/orders`, with a few more every day, and one reply holding all of them would be slow to send and slow to read. You can ask for bigger pages up to a limit, and past it the server refuses.
    """)
    return


@app.cell
def _(requests):
    too_big_reply = requests.get(
        "https://oim.zhili.dev/ma/towns",
        params={"per_page": 500},
        timeout=10,
    )
    too_big_reply.status_code, too_big_reply.json()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **422** means the request had the right shape and a value the server will not accept. Its reply names the limit.

    So reading everything takes one request per page. `get_page` asks for one page. `per_page=100` in its brackets is a **default**: `get_page(2)` uses 100, and `get_page(2, 20)` uses 20. The server's parameters have defaults too, which is why leaving out `page` gave page 1.
    """)
    return


@app.cell
def _(requests):
    def get_page(page, per_page=100):
        page_reply = requests.get(
            "https://oim.zhili.dev/ma/towns",
            params={"page": page, "per_page": per_page},
            timeout=10,
        )
        return page_reply.json()

    return (get_page,)


@app.cell
def _(get_page):
    get_page(1)["pagination"]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ✏️ E · Every town

    Write `get_all_towns()`. It reads page 1, takes `pages` from its `pagination`, reads the pages after it with `range(2, pages + 1)`, and returns one list of every town.

    *Check yourself: 351 towns, the same number as `pagination["total"]`. The first is Abington and the last is Yarmouth.*

    The count you collected against the total the server reports is a check you can run on any API that sends pages.

    **Going further.** Which town has the highest average single-family tax bill in the state, and which the lowest?
    """)
    return


@app.cell
def _(requests):
    def get_all_towns():
        """Return a list of every town, reading all pages of /ma/towns."""
        url = "https://oim.zhili.dev/ma/towns"

        # Page 1: keep its towns and find out how many pages there are
        first_page = requests.get(url, timeout=10).json()
        towns = first_page["items"]
        pages = first_page["pagination"]["pages"]

        # Pages 2 through the last one
        for page in range(2, pages + 1):
            response = requests.get(url, params={"page": page}, timeout=10).json()
            towns.extend(response["items"])

        return towns


    all_towns = get_all_towns()
    len(all_towns)
    return (all_towns,)


@app.cell
def _(all_towns):
    with_bill = [t for t in all_towns if t["average_single_family_bill_dollars"] is not None]

    highest = max(with_bill, key=lambda t: t["average_single_family_bill_dollars"])
    lowest = min(with_bill, key=lambda t: t["average_single_family_bill_dollars"])

    print("Highest:", highest["name"], highest["average_single_family_bill_dollars"])
    print("Lowest:", lowest["name"], lowest["average_single_family_bill_dollars"])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 4. Sending Data

    Every request so far has been a **GET**, which asks for data and changes nothing. A **POST** sends data for the server to keep. Submitting a form on a website is a POST.

    The course API has a board, [oim.zhili.dev/live](https://oim.zhili.dev/live), with one line per student. A POST to `/message` writes yours.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **The server has to know who sent it.** A request can carry **headers**, lines that travel beside the address. Here the header `x-token` holds your GitHub username, and the board shows your first name. Your username is public, so it can sit in a cell. A real API's key goes in a header the same way, but a key is a secret and never goes in a cell: [Mini Project 2](/assignments/mini-project-2/) says where to keep one.

    **The message goes in the body.** `json=` puts it there, which is where a POST carries its data. `params=` puts values in the address, which is for asking.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ✏️ F · Write on the board

    1. Look up a town you know with the `name` parameter of `/ma/towns`. Keep its name as `town_name` and its average single-family bill as `town_bill`.
    2. Add a cell with the code below, put your GitHub username in place of the brackets, and run it.

       ```python
       board_reply = requests.post(
           "https://oim.zhili.dev/message",
           headers={"x-token": "<your-github-username>"},
           json={"message": f"{town_name}: ${town_bill:,}"},
           timeout=10,
       )
       board_reply.status_code, board_reply.json()
       ```

       *Check yourself: **201**, which means the server created something, and your town on the board.*

    3. Delete the `headers=` line and run it again. In a markdown cell under it, answer: what did the server answer, and why does it need to know who sent a message?

    **Going further.** Post something more useful than one town's bill: choose a question somebody would ask, answer it from live data, and post the answer, in 140 characters or fewer.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Advanced · G · Take it down.** `requests.delete` on the same address, with the same header, removes your line. Run it twice and compare the two replies.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 🚀 This Week's Work

    1. **Notebook 3, sections 4 to 6**, if you have not finished them
    2. **Everything above in this notebook** that is not marked **Advanced**, in your repository under `notebooks/`
    3. **[Mini Project 1](/assignments/mini-project-1/)**, due Sunday 10/11
    4. **[Mini Project 2](/assignments/mini-project-2/)**, due Sunday 10/25
    5. **Commit as you go**, with messages that state what changed, and push before you stop
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **What you can do now:**

    - [ ] I can write a function with `def`, with parameters, a default and a `return`
    - [ ] I can state why a piece of work belongs in a function
    - [ ] I can find an endpoint's parameters in an API's documentation and pass them with `params=`
    - [ ] I can read every page of an API that sends pages, and check the count against the total
    - [ ] I can send data to an API with a POST and a header
    """)
    return


if __name__ == "__main__":
    app.run()
