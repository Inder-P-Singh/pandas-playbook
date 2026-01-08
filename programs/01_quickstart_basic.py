"""
01 - Pandas Quickstart: Basic Operations

This script covers the absolute basics of Pandas:
- loading data
- inspection
- column selection
- filtering
- saving a basic report
"""

# Ensure requirements are installed:
# pip install -r ../requirements.txt

import pandas as pd
import numpy as np
import os
import json

# Ensure 'outputs' directory exists
os.makedirs("outputs", exist_ok=True)

print("Pandas version:", pd.__version__)
print("Numpy version:", np.__version__)

# -------------------------------------------------
# 1. Load Data
# -------------------------------------------------
# Explicitly set customer_id to nullable Int64 (Pandas 2.x feature)
sales_df = pd.read_csv(
    "data/sales_small.csv",
    dtype={"customer_id": "Int64"}
)

print("Data loaded successfully.")

# -------------------------------------------------
# 2. Inspect Data
# -------------------------------------------------
print("\n--- DataFrame Head ---")
print(sales_df.head())

print("\n--- DataFrame Info ---")
sales_df.info()

print("\n--- DataFrame dtypes ---")
print(sales_df.dtypes)

# -------------------------------------------------
# 3. Select Columns
# -------------------------------------------------
print("\nSingle column 'amount':")
print(sales_df["amount"].head())

print("\nMultiple columns 'order_id', 'amount', 'region':")
print(sales_df[["order_id", "amount", "region"]].head())

# -------------------------------------------------
# 4. Row Selection with .loc and .iloc
# -------------------------------------------------
print("\nFirst 3 rows (labels 0 to 2 inclusive) using .loc:")
print(sales_df.loc[0:2])

print("\nRows at index positions 0, 2, 4 using .iloc:")
print(sales_df.iloc[[0, 2, 4]])

print("\nAmount and Region for first 3 rows using .loc:")
print(sales_df.loc[0:2, ["amount", "region"]])

print("\nAmount and Region for first 3 rows using .iloc:")
print(sales_df.iloc[0:3, [5, 6]])  # amount, region column positions

# -------------------------------------------------
# 5. Conditional Filtering
# -------------------------------------------------
high_value_orders = sales_df[sales_df["amount"] > 100]

print("\nOrders with amount > 100 (first 5):")
print(high_value_orders.head())

electronics_north_orders = sales_df[
    (sales_df["category"] == "Electronics") &
    (sales_df["region"] == "North")
]

print("\n'Electronics' orders in 'North' region (first 5):")
print(electronics_north_orders.head())

# -------------------------------------------------
# 6. Save Report to CSV
# -------------------------------------------------
output_csv = "outputs/quick_report.csv"
high_value_orders.to_csv(output_csv, index=False)

print(f"Saved '{output_csv}'")

# -------------------------------------------------
# Verification
# -------------------------------------------------
verification_data = {
    "script": "01_quickstart_basic.py",
    "sales_rows": len(sales_df),
    "high_value_rows": len(high_value_orders),
    "quick_report_exists": os.path.exists(output_csv)
}

verification_path = "outputs/verification_01_quickstart_basic.json"
with open(verification_path, "w") as f:
    json.dump(verification_data, f, indent=2)

print("\nQUICKSTART_OK")
print("\nVerification Data:")
print(json.dumps(verification_data, indent=2))

print("\nSample data preview:")
print(sales_df.head(3))
