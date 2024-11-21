import sys
import pandas as pd

def load_model(filename='model.txt'):
    with open(filename, 'r') as file:
        theta0, theta1 = map(float, file.read().split(','))
    return theta0, theta1

def load_data(filename):
    data = pd.read_csv(filename)
    return data['km'].values, data['price'].values

def estimate_price(mileage, theta0, theta1):
    return theta0 + theta1 * mileage

def main():
    theta0, theta1 = load_model()
    if len(sys.argv) == 1:
        mileage = float(input("Enter the mileage of the car: "))
        predicted_price = estimate_price(mileage, theta0, theta1)
        print()
        print(f'The estimated price for a car with {mileage} mileage is: {predicted_price}')
        print()
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
