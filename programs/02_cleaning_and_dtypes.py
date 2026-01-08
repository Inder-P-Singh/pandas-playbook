"""
02 - Pandas: Cleaning and Data Types

Demonstrates:
- Missing value detection
- Imputation vs dropping
- Nullable dtypes (Pandas 2.x)
- Datetime conversion
- Duplicate removal
- Memory optimization with categorical dtypes
"""

import pandas as pd
import numpy as np
import os
import json

# Ensure 'outputs' directory exists
os.makedirs("outputs", exist_ok=True)

# -------------------------------------------------
# Load data (nullable Int64 for customer_id)
# -------------------------------------------------
sales_df = pd.read_csv(
    "data/sales_small.csv",
    dtype={"customer_id": "Int64"}
)

print("Original DataFrame Info:")
sales_df.info()
print("\nOriginal DataFrame Head:")
print(sales_df.head())

# -------------------------------------------------
# 1. Missing Value Detection
# -------------------------------------------------
print("\nMissing values per column:")
print(sales_df.isna().sum())

print("\nPercentage of missing values:")
missing_pct = (sales_df.isna().sum() / len(sales_df) * 100).round(2)
print(missing_pct.astype(str) + "%")

# -------------------------------------------------
# 2. Imputation and Dropping Missing Values
# -------------------------------------------------
median_amount = sales_df["amount"].median()
print(f"\nMedian amount: {median_amount:.2f}")

sales_df["amount_filled"] = sales_df["amount"].fillna(median_amount)

# Drop rows with missing customer_id (key identifier)
sales_df_cleaned_initial = sales_df.dropna(subset=["customer_id"]).copy()

# Impute region with mode
mode_region = sales_df_cleaned_initial["region"].mode()[0]
sales_df_cleaned_initial["region_filled"] = (
    sales_df_cleaned_initial["region"].fillna(mode_region)
)

print("\nMissing values after imputation and dropping:")
print(sales_df_cleaned_initial.isna().sum())

print("\nDataFrame head after initial cleaning:")
print(sales_df_cleaned_initial.head())

# -------------------------------------------------
# 3. Converting Data Types (Nullable dtypes)
# -------------------------------------------------
sales_df_cleaned_initial["customer_id"] = (
    sales_df_cleaned_initial["customer_id"].astype("Int64")
)
print("\n'customer_id' dtype:")
print(sales_df_cleaned_initial["customer_id"].dtype)

sales_df_cleaned_initial["order_date"] = pd.to_datetime(
    sales_df_cleaned_initial["order_date"]
)
print("\n'order_date' dtype:")
print(sales_df_cleaned_initial["order_date"].dtype)

sales_df_cleaned_initial["amount_filled"] = (
    sales_df_cleaned_initial["amount_filled"].astype(float)
)
print("\n'amount_filled' dtype:")
print(sales_df_cleaned_initial["amount_filled"].dtype)

# Replace original columns
sales_df_cleaned_final = sales_df_cleaned_initial.drop(
    columns=["amount", "region"]
)
sales_df_cleaned_final.rename(
    columns={
        "amount_filled": "amount",
        "region_filled": "region"
    },
    inplace=True
)

print("\nDataFrame dtypes after conversions:")
print(sales_df_cleaned_final.dtypes)

# -------------------------------------------------
# 4. Duplicate Detection and Removal
# -------------------------------------------------
dup_count = sales_df_cleaned_final.duplicated().sum()
print(f"\nDuplicate rows detected: {dup_count}")

sales_df_deduplicated = sales_df_cleaned_final.drop_duplicates()
print("Rows after dropping duplicates:", len(sales_df_deduplicated))

# -------------------------------------------------
# 5. Memory Optimization (Categorical dtypes)
# -------------------------------------------------
print("\nMemory usage BEFORE category conversion:")
sales_df_deduplicated.info(verbose=False, memory_usage="deep")

for col in ["product", "category", "region"]:
    if col in sales_df_deduplicated.columns and \
       sales_df_deduplicated[col].dtype == "object":
        sales_df_deduplicated[col] = (
            sales_df_deduplicated[col].astype("category")
        )

print("\nMemory usage AFTER category conversion:")
sales_df_deduplicated.info(verbose=False, memory_usage="deep")

# -------------------------------------------------
# Save cleaned data
# -------------------------------------------------
output_csv = "outputs/cleaned_sales.csv"
sales_df_deduplicated.to_csv(output_csv, index=False)
print(f"\nSaved '{output_csv}'")

# -------------------------------------------------
# Verification
# -------------------------------------------------
verification_data = {
    "script": "02_cleaning_and_dtypes.py",
    "final_rows": len(sales_df_deduplicated),
    "nulls_in_amount": int(
        sales_df_deduplicated["amount"].isna().sum()
    ),
    "customer_id_dtype": str(
        sales_df_deduplicated["customer_id"].dtype
    ),
    "cleaned_sales_exists": os.path.exists(output_csv),
    "memory_optimized_columns": {
        col: str(sales_df_deduplicated[col].dtype)
        for col in ["product", "category", "region"]
        if col in sales_df_deduplicated.columns
    }
}

verification_path = "outputs/verification_02_cleaning_and_dtypes.json"
with open(verification_path, "w") as f:
    json.dump(verification_data, f, indent=2)

print("\nCLEANING_AND_DTYPES_OK")
print("\nVerification Data:")
print(json.dumps(verification_data, indent=2))

print("\nSample cleaned data preview:")
print(sales_df_deduplicated.head(3))
