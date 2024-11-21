import sys
import pandas as pd
import os

def load_model(filename='model.txt'):
    if not os.path.exists(filename):
        print(f"File '{filename}' does not exist. Exiting...")
        sys.exit(1)
    with open(filename, 'r') as file:
            content = file.read().strip()
            
            parts = content.split(',')
            if len(parts) != 2:
                exit("Invalid model file")
            if parts[0] == '' or parts[1] == '':
                exit("Invalid model file")

            theta0, theta1 = map(float, parts)
    return theta0, theta1

def load_data(filename):
    data = pd.read_csv(filename)
    return data['km'].values, data['price'].values

def estimate_price(mileage, theta0, theta1):
    if mileage < 0:
        print("The mileage should be a positive number")
        sys.exit(1)
    return theta0 + theta1 * mileage

def check_if_float(s):
    dot_count = 0

    for char in s:
        if char.isdigit():
            continue
        elif char == '.':
            dot_count += 1
        else:
            return False

    if dot_count <= 1:
        return True
    else:
        return False

def main():
    theta0, theta1 = load_model()
    if len(sys.argv) == 1:
        mileage = input("Enter the mileage of the car: ")
        if check_if_float(mileage):
            mileage = float(mileage)
        elif not mileage.isdigit():
            print("The mileage should be a number. If float use a point and not a comma\n")
            sys.exit(1)
        else:
            mileage = float(mileage)
        predicted_price = estimate_price(mileage, theta0, theta1)
        if predicted_price < 0:
            predicted_price = 0
        print(f'\nThe estimated price for a car with {mileage} mileage is: {predicted_price}\n')
        mileages, prices = load_data('data.csv')
        for i in range(len(prices)):
            if mileage == mileages[i]:
                print(f'The actual price for a car with {mileages[i]} mileage is: {prices[i]}')
                print(f'The result of this operation is: {round(prices[i] - predicted_price, 1)} dollars away from the actual price.')
                break
    else:
        print("Usage: python3 estimate_price.py")

if __name__ == "__main__":
    main()
