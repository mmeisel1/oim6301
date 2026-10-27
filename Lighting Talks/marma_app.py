import marimo

__generated_with = "0.17.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    from typing import Literal, Optional
    from fastmcp import FastMCP, Client
    return Client, FastMCP, Literal, Optional, mo


@app.cell
def _(mo):
    mo.md(
        r"""
        # MARMA Project, as a ChatGPT app

        **Lightning talk demo.** A "brand app" in ChatGPT (like *Explore Prada*) is just a
        small **Python server** that tells the model: *here are functions you're allowed to call*.
        It uses the open **Model Context Protocol (MCP)**.

        This notebook builds one for **MARMA Project**: brand moves and trends
        *before they go mainstream*.

        1. **The data**: what MARMA knows
        2. **The server**: two Python functions become tools
        3. **What ChatGPT sees**: the schema generated from type hints and docstrings
        4. **Try it**: call the tools the way ChatGPT would
        5. **What breaks**: the same tool with a lazy docstring
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""## 1 · The data""")
    return


@app.cell
def _():
    # Real brand moves (from MARMA notes / public sources). Add your own!
    BRAND_MOVES = [
        {
            "id": "bm-001",
            "brand": "Golden Goose",
            "category": "fashion",
            "city": "Boston",
            "move": "Took over The Coop (Harvard's bookstore) for year three of its "
                    "FiveFourFive collab, an Ivy League / varsity collection.",
            "why_it_matters": "Sells the Ivy aesthetic from inside the Ivy League. "
                              "The venue is the credibility.",
        },
        {
            "id": "bm-002",
            "brand": "Prada",
            "category": "fashion",
            "city": "Global",
            "move": "Launched 'Explore Prada' inside ChatGPT: browse products, "
                    "runway stories and stores in conversation.",
            "why_it_matters": "Luxury meeting customers inside an AI assistant "
                              "instead of only on its own site.",
        },
        {
            "id": "bm-003",
            "brand": "Miu Miu",
            "category": "fashion",
            "city": "Global",
            "move": "Custom Studio with Accenture Song: customers personalise bags "
                    "and shoes with charms and pins, rendered by AI image generation.",
            "why_it_matters": "AI as a personalisation layer for luxury, "
                              "not just a cost-cutting tool.",
        },
    ]

    # SAMPLE trend signals: placeholders to replace with your own MARMA research.
    # mainstream_score: 0 = only coolhunters know, 100 = your mum has heard of it.
    TRENDS = [
        {"trend": "Varsity / Ivy prep revival", "category": "fashion", "mainstream_score": 62},
        {"trend": "Shopping inside AI assistants", "category": "tech", "mainstream_score": 28},
        {"trend": "Fragrance layering kits", "category": "beauty", "mainstream_score": 55},
        {"trend": "Artist-run members' clubs", "category": "art", "mainstream_score": 18},
        {"trend": "Fractional luxury resale", "category": "finance", "mainstream_score": 34},
        {"trend": "Bookstore-as-brand-venue", "category": "fashion", "mainstream_score": 22},
    ]
    return BRAND_MOVES, TRENDS


@app.cell
def _(BRAND_MOVES, TRENDS, mo):
    mo.vstack([
        mo.md("**Brand moves**"), mo.ui.table(BRAND_MOVES, selection=None),
        mo.md("**Trend radar** *(sample data)*"), mo.ui.table(TRENDS, selection=None),
    ])
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 2 · The server

        Two ordinary Python functions. The `@mcp.tool` decorator is the whole trick.
        **Type hints** become the input rules, and the **docstring** becomes the
        instructions the model reads to decide *when* to call the tool.
        """
    )
    return


@app.cell
def _(BRAND_MOVES, FastMCP, Literal, Optional, TRENDS):
    Category = Literal["fashion", "beauty", "art", "finance", "tech"]

    mcp = FastMCP("MARMA Project")

    @mcp.tool
    def search_brand_moves(
        category: Optional[Category] = None,
        city: Optional[str] = None,
        keyword: Optional[str] = None,
    ) -> list[dict]:
        """Find notable brand moves (collabs, takeovers, launches) curated by
        MARMA Project, a coolhunting platform. Use when the user asks what
        brands are doing, what's a smart brand move, or what's happening in a city."""
        results = BRAND_MOVES
        if category:
            results = [m for m in results if m["category"] == category]
        if city:
            results = [m for m in results if city.lower() in m["city"].lower()]
        if keyword:
            k = keyword.lower()
            results = [m for m in results if k in (m["brand"] + m["move"]).lower()]
        return results

    @mcp.tool
    def trend_radar(
        category: Optional[Category] = None,
        max_mainstream_score: int = 40,
    ) -> list[dict]:
        """Return emerging trends BEFORE they go mainstream. mainstream_score runs
        from 0 (only coolhunters know) to 100 (everyone knows). Lower
        max_mainstream_score = earlier, more niche trends. Sorted earliest first."""
        results = [t for t in TRENDS if t["mainstream_score"] <= max_mainstream_score]
        if category:
            results = [t for t in results if t["category"] == category]
        return sorted(results, key=lambda t: t["mainstream_score"])

    return (mcp,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 3 · What ChatGPT actually sees

        ChatGPT never sees the Python code. It gets this JSON: a name, a description,
        and an input schema, all **generated automatically** from the function above.
        """
    )
    return


@app.cell
async def _(Client, mcp, mo):
    async with Client(mcp) as _client:
        _tools = await _client.list_tools()

    mo.accordion({
        f"🔧 {t.name}": mo.vstack([
            mo.md(f"*{t.description}*"),
            mo.json(t.input_schema),
        ])
        for t in _tools
    }, multiple=True)
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 4 · Try it: be the model

        When a user asks ChatGPT *"what's niche in tech right now?"*, the model picks a
        tool and fills in the arguments. Here **you** fill them in. The call goes through
        a real MCP client, exactly the protocol ChatGPT uses.
        """
    )
    return


@app.cell
def _(mo):
    tool_pick = mo.ui.dropdown(
        options=["trend_radar", "search_brand_moves"], value="trend_radar", label="Tool"
    )
    category_pick = mo.ui.dropdown(
        options=["any", "fashion", "beauty", "art", "finance", "tech"],
        value="any", label="category",
    )
    score_pick = mo.ui.slider(0, 100, value=40, step=5, label="max_mainstream_score",
                              show_value=True)
    city_pick = mo.ui.text(placeholder="e.g. Boston", label="city")
    return category_pick, city_pick, score_pick, tool_pick


@app.cell
def _(category_pick, city_pick, mo, score_pick, tool_pick):
    _extra = score_pick if tool_pick.value == "trend_radar" else city_pick
    mo.hstack([tool_pick, category_pick, _extra], justify="start", gap=1)
    return


@app.cell
async def _(Client, category_pick, city_pick, mcp, mo, score_pick, tool_pick):
    args = {}
    if category_pick.value != "any":
        args["category"] = category_pick.value
    if tool_pick.value == "trend_radar":
        args["max_mainstream_score"] = score_pick.value
    elif city_pick.value.strip():
        args["city"] = city_pick.value.strip()

    async with Client(mcp) as _client:
        _result = await _client.call_tool(tool_pick.value, args)
    rows = _result.structured_content["result"]

    mo.vstack([
        mo.md(f"**Model's tool call:** `{tool_pick.value}({args})`"),
        mo.ui.table(rows, selection=None) if rows else mo.md("_No results: nothing matches._"),
    ])
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 5 · What breaks: same code, lazy description

        This tool does **exactly the same thing** as `trend_radar`. But look at what the
        model gets: no idea what `n` means, what the numbers are, or when to use it.
        In an app, **the docstring is the product copy for the AI.**
        """
    )
    return


@app.cell
async def _(Client, FastMCP, TRENDS, mo):
    lazy = FastMCP("Lazy version")

    @lazy.tool
    def get_data(n: int = 40) -> list:
        return [t for t in TRENDS if t["mainstream_score"] <= n]

    async with Client(lazy) as _client:
        _t = (await _client.list_tools())[0]

    mo.hstack([
        mo.vstack([mo.md("**❌ get_data**"), mo.md(f"*{_t.description or '(no description)'}*"),
                   mo.json(_t.input_schema)]),
    ])
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ---
        ### 🗣️ Question for the room

        > **If you were Prada, would you rather own the customer on your own site,
        > or meet them inside ChatGPT, where OpenAI controls the interface?**

        <details><summary>Going live in real ChatGPT (optional)</summary>

        Move the server cell into `server.py`, end it with
        `mcp.run(transport="http", port=8000)`, expose it with a tunnel (e.g. ngrok),
        and add the URL as a custom app in ChatGPT's developer mode.
        </details>
        """
    )
    return


if __name__ == "__main__":
    app.run()
