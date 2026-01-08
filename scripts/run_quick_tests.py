import pandas as pd
import os

def run_checks():
    data_path = 'data/sales_small.csv'
    if not os.path.exists(data_path):
        print(f"Error: {data_path} not found.")
        return False

    # Load data, explicitly handling customer_id as nullable integer
    df = pd.read_csv(data_path, dtype={'customer_id': 'Int64'})

    # Check 1: Assert number of rows > 10
    assert len(df) > 10, f"Expected more than 10 rows, got {len(df)}"
    print(f"Check 1: Number of rows ({len(df)}) > 10 - PASS")

    # Check 2: Assert no column named 'unnamed' (common issue with saving index)
    assert 'Unnamed: 0' not in df.columns, "Found 'Unnamed: 0' column.\nThis usually happens if you save a DataFrame to CSV with `index=True` (default) and then reload it.\nEnsure `index=False` when saving CSVs."
    print("Check 2: No 'Unnamed: 0' column - PASS")

    # Check 3: Assert 'amount' column exists
    assert 'amount' in df.columns, "Expected 'amount' column not found."
    print("Check 3: 'amount' column exists - PASS")

    # Check 4: Assert sum of amounts is positive (ignoring NaNs for sum calculation)
    # Ensure 'amount' is numeric, coercing errors to NaN
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
    assert df['amount'].sum() > 0, "Sum of 'amount' column is not positive or contains only NaNs."
    print(f"Check 4: Sum of 'amount' ({df['amount'].sum():.2f}) is positive - PASS")

    # Check 5: Assert 'customer_id' column is nullable Int64 dtype
    assert df['customer_id'].dtype == pd.Int64Dtype(), \
        f"Expected 'customer_id' dtype to be Int64, but got {df['customer_id'].dtype}"
    print("Check 5: 'customer_id' column has nullable Int64 dtype - PASS")

    print("\nALL_CHECKS_PASS")
    return True

if __name__ == '__main__':
    if run_checks():
        exit(0)
    else:
        exit(1)
