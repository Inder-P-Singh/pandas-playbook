"""
03 - Pandas: Groupby, Merge, Pivot Table

Demonstrates:
- Aggregation with groupby
- Table joins with merge (left and inner)
- Reshaping data with pivot_table
- Simple visualization with seaborn/matplotlib
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
        "data/sales_small.csv",
        dtype={"customer_id": "Int64"}
    )

    raw_sales_df["amount"] = raw_sales_df["amount"].fillna(
        raw_sales_df["amount"].median()
    )

    sales_df = raw_sales_df.dropna(subset=["customer_id"]).copy()

    mode_region = sales_df["region"].mode()[0]
    sales_df["region"] = sales_df["region"].fillna(mode_region)

    sales_df = sales_df.drop_duplicates()

    sales_df["order_date"] = pd.to_datetime(sales_df["order_date"])

    for col in ["product", "category", "region"]:
        if col in sales_df.columns and sales_df[col].dtype == "object":
            sales_df[col] = sales_df[col].astype("category")

    sales_df.to_csv("outputs/cleaned_sales.csv", index=False)

# -------------------------------------------------
# Load customers data
# -------------------------------------------------
customers_df = pd.read_csv(
    "data/customers_small.csv",
    dtype={"customer_id": "Int64"}
)

print("\nSales Data Info:")
sales_df.info()

print("\nCustomers Data Info:")
customers_df.info()

# -------------------------------------------------
# 1. Groupby Aggregation
# -------------------------------------------------
region_summary = (
    sales_df
    .groupby("region")
    .agg(
        total_sales=("amount", "sum"),
        order_count=("order_id", "count")
    )
    .reset_index()
)

print("\nRegional Sales Summary:")
print(region_summary)

# -------------------------------------------------
# 2. Merging Tables
# -------------------------------------------------
merged_left = pd.merge(
    sales_df,
    customers_df,
    on="customer_id",
    how="left",
    suffixes=("_sales", "_cust")
)

print("\nMerged (Left Join) sample:")
print(merged_left.head())
print("Rows (left join):", len(merged_left))
print(
    "Missing customer names (left join):",
    merged_left["name"].isna().sum()
)

merged_inner = pd.merge(
    sales_df,
    customers_df,
    on="customer_id",
    how="inner",
    suffixes=("_sales", "_cust")
)

print("\nMerged (Inner Join) sample:")
print(merged_inner.head())
print("Rows (inner join):", len(merged_inner))

inner_csv = "outputs/sales_customer_merged_inner.csv"
merged_inner.to_csv(inner_csv, index=False)
print(f"Saved '{inner_csv}'")

# -------------------------------------------------
# 3. Reshaping with Pivot Table
# -------------------------------------------------
merged_left["amount"] = (
    pd.to_numeric(merged_left["amount"], errors="coerce")
    .fillna(0)
)

category_region_sales = pd.pivot_table(
    merged_left,
    index="region",
    columns="category",
    values="amount",
    aggfunc="sum",
    fill_value=0
)

print("\nPivot Table: Total Sales by Region and Category")
print(category_region_sales)

# -------------------------------------------------
# 4. Visualization
# -------------------------------------------------
plt.figure(figsize=(10, 6))
sns.barplot(
    x="region",
    y="total_sales",
    data=region_summary,
    palette="viridis"
)
plt.title("Total Sales by Region")
plt.xlabel("Region")
plt.ylabel("Total Sales Amount")
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()

plot_path = "outputs/aggregated_plot.png"
plt.savefig(plot_path)
plt.close()

print(f"Saved '{plot_path}'")

# -------------------------------------------------
# Verification
# -------------------------------------------------
verification_data = {
    "script": "03_groupby_merge_pivot.py",
    "region_summary_rows": len(region_summary),
    "merged_left_rows": len(merged_left),
    "merged_inner_rows": len(merged_inner),
    "pivot_table_shape": category_region_sales.shape,
    "aggregated_plot_exists": os.path.exists(plot_path),
}

verification_path = "outputs/verification_03_groupby_merge_pivot.json"
with open(verification_path, "w") as f:
    json.dump(verification_data, f, indent=2)

print("\nGROUPBY_MERGE_PIVOT_OK")
print("\nVerification Data:")
print(json.dumps(verification_data, indent=2))

print("\nPivot table preview:")
print(category_region_sales.head())
