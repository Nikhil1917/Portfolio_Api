# Stock Portfolio Optimization API

This project provides a Flask API for optimizing stock portfolios based on data stored in a Parquet file. The API allows you to upload a Parquet file containing stock data and receive an optimized portfolio in return.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Testing the API](#testing-the-api)
5. [Example Request](#example-request)
6. [Contributing](#contributing)
7. [License](#license)

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.7 or higher
- pip (Python package manager)
- A Parquet file with the necessary stock data (see [Usage](#usage) for details)

## Installation

1. **Clone the repository** (if applicable):
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2. **Create a virtual environment** (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages**:
    ```bash
    pip install Flask pandas openpyxl
    ```

## Usage

1. **Prepare your Parquet file**: Ensure your Parquet file contains the following columns:
    - `context_id`: Identifier for each asset.
    - `close`: Closing prices for the assets.

2. **Run the Flask application**:
    ```bash
    python Main.py
    ```

   By default, the API will run on `http://127.0.0.1:5000`.

## Testing the API

You can test the API using tools like Postman or CURL. Here's how to do it with CURL:

### Example Request

1. **Make a POST request to the `/optimize` endpoint**. Replace `<path_to_your_parquet_file>` with the actual path to your Parquet file:

   ```bash
   curl -X POST http://127.0.0.1:5000/optimize \
   -H "Content-Type: application/json" \
   -d '{
       "parquet_file_path": "<path_to_your_parquet_file>",
       "initial_budget": 1000,
       "risk_free_rate": 0.01
   }'
