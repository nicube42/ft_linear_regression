import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def load_data(filename):
    data = pd.read_csv(filename)
    return data['km'].values, data['price'].values

def estimate_price(mileage, theta0, theta1):
    return theta0 + theta1 * mileage

def train_linear_regression(mileages, prices, learning_rate, num_iterations):
    m = len(mileages)
    theta0 = 0
    theta1 = 0

    mean_mileage = np.mean(mileages)
    std_mileage = np.std(mileages)
    mileages_standardized = (mileages - mean_mileage) / std_mileage
    
    print("Training...")
    
    for iteration in range(num_iterations):
        errors = estimate_price(mileages_standardized, theta0, theta1) - prices
        sum_errors_theta0 = np.sum(errors)
        sum_errors_theta1 = np.sum(errors * mileages_standardized)
        
        tmp_theta0 = learning_rate * (1 / m) * sum_errors_theta0
        tmp_theta1 = learning_rate * (1 / m) * sum_errors_theta1
        
        theta0 -= tmp_theta0
        theta1 -= tmp_theta1
    
    theta1 = theta1 / std_mileage
    theta0 = theta0 - (theta1 * mean_mileage)
    
    return theta0, theta1

def save_model(theta0, theta1, filename='model.txt'):
    with open(filename, 'w') as file:
        file.write(f'{theta0},{theta1}')

def plot_data(mileages, prices, theta0, theta1):
    plt.scatter(mileages, prices, color='blue')
    plt.plot(mileages, theta0 + theta1 * mileages, color='red')
    plt.xlabel('Mileage')
    plt.ylabel('Price')
    plt.title('Price vs Mileage (non-standardized values)')
    plt.show()

def plot_residuals_histogram(mileages, prices, theta0, theta1):
    predicted_prices = estimate_price(mileages, theta0, theta1)

    residuals = prices - predicted_prices

    plt.figure(figsize=(10, 6))
    plt.hist(residuals, bins=30, edgecolor='k', alpha=0.7)
    plt.xlabel('Residuals')
    plt.ylabel('Frequency')
    plt.title('Histogram of Residuals')
    plt.grid(True)
    plt.show()

# r2 score
def calculate_precision(prices, predicted_prices):
    return 1 - np.sum((prices - predicted_prices) ** 2) / np.sum((prices - np.mean(prices)) ** 2)

def compute_mae(prices, predicted_prices):
    return np.mean(np.abs(prices - predicted_prices))

def main():
    filename = 'data.csv'
    learning_rate = 1e-5
    num_iterations = 2000000
    
    mileages, prices = load_data(filename)
    theta0, theta1 = train_linear_regression(mileages, prices, learning_rate, num_iterations)
    print("Training completed.")
    save_model(theta0, theta1)
    print(f'Model trained: theta0 = {theta0}, theta1 = {theta1}')
    print(f'Precision (R2): {round(calculate_precision(prices, estimate_price(mileages, theta0, theta1)) * 100, 2)}%')
    print(f'Mean Absolute Error (MAE): {compute_mae(prices, estimate_price(mileages, theta0, theta1))}')
    plot_data(mileages, prices, theta0, theta1)
    plot_residuals_histogram(mileages, prices, theta0, theta1)
if __name__ == "__main__":
    main()
