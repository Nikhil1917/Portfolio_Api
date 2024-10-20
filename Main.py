from flask import Flask, request, jsonify
import numpy as np
import pandas as pd
import os

app = Flask(__name__)

# Function to read stock data from a Parquet file
def read_stock_data(file_path):
    try:
        data = pd.read_parquet(file_path)
        return data
    except Exception as e:
        print(f"Error reading Parquet file: {e}")
        return None

# Function to optimize the portfolio
def optimize_portfolio(stock_data, initial_budget, risk_free_rate):
    # Group by 'context_id' to get unique assets
    grouped_data = stock_data.groupby('context_id').agg({
        'close': 'mean'  # Calculate the average closing price for each asset
    }).reset_index()

    # Simulate returns for each asset based on average closing prices
    returns = {}
    for index, row in grouped_data.iterrows():
        # For simplicity, let's simulate some random returns
        returns[row['context_id']] = np.random.rand()

    assets = list(returns.keys())
    num_assets = len(assets)

    if num_assets == 0:
        return None, None, None, None  # No assets available

    # Generate random weights for each asset
    weights = np.random.rand(num_assets)
    weights /= np.sum(weights)  # Normalize weights

    # Calculate expected return and risk
    expected_return = np.dot(weights, list(returns.values())) * initial_budget
    expected_risk = np.std(list(returns.values()))

    # Calculate the amount to invest in each asset based on their weights
    investment = (weights * initial_budget).tolist()

    # Create a DataFrame for the results
    result_df = pd.DataFrame({
        'Asset': assets,
        'Weight': weights,
        'Investment': investment,
        'Expected Return': [returns[asset] for asset in assets]
    })

    # Define output Excel file path
    excel_file_path = os.path.join('static', 'portfolio_optimization.xlsx')

    # Save the results to an Excel file
    result_df.to_excel(excel_file_path, index=False)

    return expected_return, expected_risk, investment, excel_file_path

@app.route('/optimize', methods=['POST'])
def optimize():
    # Get input data from the request
    data = request.get_json()
    parquet_file_path = data.get('parquet_file_path')
    initial_budget = data.get('initial_budget', 1000)
    risk_free_rate = data.get('risk_free_rate', 0.01)

    print(f"Received data: {data}")

    # Read stock data from the Parquet file
    stock_data = read_stock_data(parquet_file_path)
    if stock_data is None:
        return jsonify({'error': 'Failed to read Parquet file.'}), 400

    # Call the optimization function
    expected_return, expected_risk, investments, excel_file_path = optimize_portfolio(stock_data, initial_budget, risk_free_rate)

    # Return results as JSON
    return jsonify({
        'expected_return': expected_return,
        'expected_risk': expected_risk,
        'investments': investments,
        'excel_url': excel_file_path  # URL to download the Excel file
    })

if __name__ == '__main__':
    # Ensure the static folder exists for storing files
    os.makedirs('static', exist_ok=True)

    # Run the Flask app
    app.run(debug=True)
