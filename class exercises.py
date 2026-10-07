import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    charge = 10
    print(charge)
    return


@app.cell
def _(charges):
    print(charges)
    return


@app.cell
def _():
    # data[0]['name'] - if i wanted to get 'name' from a list {}, class example was the open ai babson code
    return


if __name__ == "__main__":
    app.run()
