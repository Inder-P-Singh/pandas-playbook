"""
04 - Pandas: Time Series Analysis and Resampling

Demonstrates:
- Datetime conversion and indexing
- Resampling time-series data
- Rolling window statistics
- Time-series visualizations
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import json

# Ensure 'outputs' directory exists
os.makedirs("outputs", exist_ok=True)

# -------------------------------------------------
# Load sales data (prefer cleaned output from step 02)
# -------------------------------------------------
try:
    sales_df = pd.read_csv(
        "outputs/cleaned_sales.csv",
        dtype={"customer_id": "Int64"}
    )
    print("Loaded cleaned_sales.csv from outputs/")
except FileNotFoundError:
    print(
        "outputs/cleaned_sales.csv not found. "
        "Performing minimal cleaning on raw data."
    )
    raw_sales_df = pd.read_csv(
        "../data/sales_small.csv",
        dtype={"customer_id": "Int64"}
    )

    raw_sales_df["amount"] = raw_sales_df["amount"].fillna(
        raw_sales_df["amount"].median()
    )

    sales_df = raw_sales_df.dropna(subset=["customer_id"]).copy()

    mode_region = sales_df["region"].mode()[0]
    sales_df["region"] = sales_df["region"].fillna(mode_region)

    sales_df = sales_df.drop_duplicates()

    for col in ["product", "category", "region"]:
        if col in sales_df.columns and sales_df[col].dtype == "object":
            sales_df[col] = sales_df[col].astype("category")

print("\nOriginal Sales Data Head:")
print(sales_df.head())

print("\nOriginal Data Types:")
print(sales_df.dtypes)

# -------------------------------------------------
# 1. Convert to Datetime and Set Index
# -------------------------------------------------
sales_df["order_date"] = pd.to_datetime(sales_df["order_date"])

sales_ts = (
    sales_df
    .set_index("order_date")
    .sort_index()
)

print("\nTime Series DataFrame Head:")
print(sales_ts.head())

print("\nTime Series Index Type:")
print(sales_ts.index.dtype)

# -------------------------------------------------
# 2. Resample by Month
# -------------------------------------------------
monthly_sales = (
    sales_ts["amount"]
    .resample("M")
    .sum()
    .fillna(0)
)

print("\nMonthly Sales Sum (first 5 months):")
print(monthly_sales.head())

plt.figure(figsize=(12, 6))
monthly_sales.plot(
    title="Monthly Total Sales",
    marker="o",
    linestyle="-",
    color="skyblue"
)
plt.xlabel("Date")
plt.ylabel("Total Sales Amount")
plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()

monthly_plot = "outputs/monthly_sales_plot.png"
plt.savefig(monthly_plot)
plt.close()

print(f"Saved '{monthly_plot}'")

# -------------------------------------------------
# 3. Rolling Mean Example
# -------------------------------------------------
rolling_mean_3m = monthly_sales.rolling(window=3).mean()

print("\n3-Month Rolling Mean (first 5 values):")
print(rolling_mean_3m.head())

plt.figure(figsize=(12, 6))
monthly_sales.plot(
    label="Monthly Sales",
    alpha=0.7,
    color="skyblue"
)
rolling_mean_3m.plot(
    label="3-Month Rolling Mean",
    color="red",
    linestyle="--",
    linewidth=2
)
plt.title("Monthly Sales vs. 3-Month Rolling Mean")
plt.xlabel("Date")
plt.ylabel("Amount")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()

rolling_plot = "outputs/rolling_mean_plot.png"
plt.savefig(rolling_plot)
plt.close()

print(f"Saved '{rolling_plot}'")

# -------------------------------------------------
# Save Time Series Report
# -------------------------------------------------
report_csv = "outputs/time_series_report.csv"
monthly_sales.reset_index().to_csv(report_csv, index=False)

print(f"Saved '{report_csv}'")

# -------------------------------------------------
# Verification
# -------------------------------------------------
verification_data = {
    "script": "04_time_series_and_resample.py",
    "sales_ts_rows": len(sales_ts),
    "monthly_sales_periods": len(monthly_sales),
    "time_series_report_exists": os.path.exists(report_csv),
    "monthly_sales_plot_exists": os.path.exists(monthly_plot),
    "rolling_mean_plot_exists": os.path.exists(rolling_plot),
}

verification_path = "outputs/verification_04_time_series_and_resample.json"
with open(verification_path, "w") as f:
    json.dump(verification_data, f, indent=2)

print("\nTIME_SERIES_OK")
print("\nVerification Data:")
print(json.dumps(verification_data, indent=2))

print("\nMonthly sales preview:")
print(monthly_sales.head())
