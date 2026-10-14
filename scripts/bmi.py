# compute bmi bmi = weight_kg / (height_m ** 2)
def compute_bmi(weight_kg, height_m):
    bmi = weight_kg / (height_m ** 2)
    return bmi
def classify_bmi(bmi):
    if bmi >= 30:
        category = "Obese"
    elif bmi >= 25:
        category = "Overweight"
    elif bmi >= 18.5:
        category = "Normal"
    else:
        category = "Underweight"
    return category

def main():
    weight_kg = float(input("Enter your weight in kg: "))
    height_m = float(input("Enter your height in meters: "))
    bmi_value = compute_bmi(weight_kg, height_m)
    result = classify_bmi(bmi_value)
    print(f"Your BMI is: {bmi_value:.2f}. You are classified as: {result    }.")

# docstring 

if __name__ == "__main__":
    main()
    