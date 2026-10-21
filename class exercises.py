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


@app.cell
def _():
    #clas oct 21
    return


@app.cell
def _():
    def compute_bmi(height, weight):
        height = float(input("Height in meters: "))
        weight = float(input("Weight in kilograms: "))
        return weight / height ** 2

    compute_bmi(1.75, 70)
    return


@app.cell
def _():
    #with this compute info it doesn't work because it then asks you to manually input the height and weight to comptute the bmi
    return


@app.cell
def _():
    people = [
        {"name": "Carla", "bmi": 27.1},
        {"name": "Hiro", "bmi": 22.4},
    ]
    for person in people:
        print(person)
    return


@app.cell
def _():
    def _():
        people = [
            {"name": "Carla", "bmi": 27.1},
            {"name": "Hiro", "bmi": 22.4},
        ]
        for person in people:
            return print(person["name"])


    _()
    return


@app.cell
def _():
    import requests

    reply = requests.get(
        "https://oim.zhili.dev/ma/towns",
        params={"county": "Worcester"},
    ).json()
    reply["pagination"]["total"]   # 60
    len(reply["items"])
    return


if __name__ == "__main__":
    app.run()
