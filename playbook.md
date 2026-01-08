# Pandas Playbook

## Playbook Metadata
-   **Audience**: Data Analysts, ML engineers (Beginner → Intermediate)
-   **Estimated time**: 20–40 minutes
-   **Outcome**: User will load CSV, inspect data, clean missing values, do groupby aggregation, merge two tables, reshape with pivot_table, and produce one simple visualization and a saved CSV report.
-   **Video URL**: Pandas Tutorial for Beginners (6 min) https://youtu.be/ZzCu5YddpEU

---

## Why Pandas Matters
Pandas is the cornerstone of data manipulation and analysis in Python. Its DataFrame structure provides an intuitive and efficient way to work with tabular data, making tasks like data cleaning, transformation, aggregation, and analysis straightforward. Mastering Pandas is essential for anyone working with data in Python, from exploratory data analysis to preparing features for machine learning models.

## Prerequisites
To get started, you'll need:
-   Python 3.10+ installed on your system.
-   `pip` for package installation.
-   A code editor (like VS Code) or an IDE (like PyCharm).

**Installation Steps:**
1.  **Clone this repository** (if you haven't already):
    `git clone https://github.com/Inder-P-Singh/pandas-playbook.git`
    `cd pandas-playbook`
2.  **Create a virtual environment**: `python3 -m venv venv`
3.  **Activate the virtual environment**: `source venv/bin/activate` (or `venv\\Scripts\\activate` on Windows)
4.  **Install requirements**: `pip install -r requirements.txt`

---

## Step-by-Step Quickstart
Follow these steps to run through the playbook programs in the `programs/` directory. Each program is designed to build on the previous one.

### 1. Explore `01_quickstart_basic.py`
This program introduces fundamental Pandas operations.
*   Load `data/sales_small.csv`.
    ```python
    import pandas as pd
    df = pd.read_csv('../data/sales_small.csv')
    ```
*   Inspect with `df.head()`, `df.info()`, `df.dtypes`.
    ```python
    df.head()
    df.info()
    df.dtypes
    ```
*   Select specific columns: `df[['order_id', 'amount', 'region']]`.
    ```python
    df[['order_id', 'amount', 'region']].head()
    ```
*   Understand `.loc` vs `.iloc` for row/column selection.
    ```python
    df.loc[0:2] # label-based, includes end
    df.iloc[[0, 2, 4]] # integer-position based
    ```
*   Filter data: `df[df.amount > 100]`.
    ```python
    df[df.amount > 100].head()
    ```
*   Save a basic report: `df.to_csv('outputs/quick_report.csv', index=False)`.

### 2. Clean Data with `02_cleaning_and_dtypes.py`
Learn how to handle common data quality issues.
*   Identify missing values: `df.isna().sum()`.
*   Impute or drop missing data: `df['amount'].fillna(df['amount'].median())`, `df.dropna(subset=['customer_id'])`.
*   Convert data types: `df['customer_id'] = df['customer_id'].astype('Int64')` (using nullable `Int64`).
*   Handle duplicates: `df.duplicated().sum()`, `df.drop_duplicates()`.
*   Memory optimization: `df['category'] = df['category'].astype('category')`.

### 3. Transform Data with `03_groupby_merge_pivot.py`
Dive into powerful data transformation techniques.
*   Aggregate data: `df.groupby('region').agg(total_sales=('amount', 'sum'))`.
*   Merge datasets: `pd.merge(sales_df, customers_df, on='customer_id', how='left')`.
*   Reshape data: `pd.pivot_table(df, index='region', columns='category', values='amount', aggfunc='sum')`.
*   Visualize: Create a simple bar chart with Matplotlib/Seaborn and save it.

### 4. Time-Series Analysis with `04_time_series_and_resample.py`
Work with date and time data.
*   Convert to datetime: `pd.to_datetime(df['order_date'])`.
*   Set datetime index: `df.set_index('order_date')`.
*   Resample data: `df.resample('M').sum()` (e.g., monthly sum).
*   Calculate rolling mean: `df['amount'].rolling(window=3).mean()`.

---

## 30-minute Lab Section
This lab section provides hands-on tasks to solidify your understanding of Pandas. Complete these tasks after reviewing the programs.

### Lab A: High-Value Orders Report
-   **Task**: Filter the `sales_small.csv` data to include only orders where `amount` is greater than 200. Save this filtered data to a new CSV file named `outputs/high_value.csv`.
-   **Estimated Time**: 5 minutes
-   **Hints**:
    1.  Load `sales_small.csv`.
    2.  Apply a boolean filter on the 'amount' column.
    3.  Use `to_csv()` to save the result, ensuring `index=False`.
-   **Success Criteria**:
    -   File `outputs/high_value.csv` exists.
    -   The file contains more than 0 rows.
-   **Verification Command**:
    ```bash
    python -c "import pandas as pd; df = pd.read_csv('outputs/high_value.csv'); assert len(df) > 0; print('LAB_A_OK')"
    ```

### Lab B: Clean Sales Data and Verify No Nulls
-   **Task**: Load `sales_small.csv`. Impute any missing values in the `amount` column with the median of the `amount` column. Convert `customer_id` to nullable integer type (`Int64`). Save the cleaned DataFrame to `outputs/cleaned_sales_lab.csv`.
-   **Estimated Time**: 10 minutes
-   **Hints**:
    1.  Load `sales_small.csv`.
    2.  Calculate the median of the 'amount' column (handle NaNs if present by dropping them first for median calculation).
    3.  Use `fillna()` for the 'amount' column.
    4.  Use `astype('Int64')` for 'customer_id'.
    5.  Save the result, ensuring `index=False`.
-   **Success Criteria**:
    -   File `outputs/cleaned_sales_lab.csv` exists.
    -   The `amount` column in `outputs/cleaned_sales_lab.csv` has no null values.
    -   The `customer_id` column in `outputs/cleaned_sales_lab.csv` has dtype `Int64`.
-   **Verification Command**:
    ```bash
    python -c "import pandas as pd; df = pd.read_csv('outputs/cleaned_sales_lab.csv', dtype={'customer_id': 'Int64'}); assert df['amount'].isnull().sum() == 0; assert df['customer_id'].dtype == pd.Int64Dtype(); print('LAB_B_OK')"
    ```

### Lab C: Region-Level Sales Totals
-   **Task**: Load `sales_small.csv`. Compute the total `amount` for each `region`. Save the results to `outputs/region_totals.csv`.
-   **Estimated Time**: 10 minutes
-   **Hints**:
    1.  Load `sales_small.csv`.
    2.  Use `groupby('region')` followed by `agg()` on 'amount' with 'sum'.
    3.  Ensure to handle potential NaNs in 'amount' before summing (e.g., `fillna(0)` or `dropna()` for aggregation).
    4.  Save the aggregated DataFrame, ensuring `index=False` if 'region' is a column, or `reset_index()` first.
-   **Success Criteria**:
    -   File `outputs/region_totals.csv` exists.
    -   The file contains data for at least 4 unique regions (e.g., North, South, East, West, Central).
-   **Verification Command**:
    ```bash
    python -c "import pandas as pd; df = pd.read_csv('outputs/region_totals.csv'); assert df['region'].nunique() >= 4; assert df['total_sales'].sum() > 0; print('LAB_C_OK')"
    ```

---

## Advanced & Reference
-   **Pandas 2.x Features**: This playbook already introduces `nullable dtypes` (like `Int64`, `boolean`, `string`) which significantly improve handling of missing data and memory efficiency. Explore more about these and the new `PyArrow` backend for even faster operations with `pd.read_csv('file.csv', engine='pyarrow')`.
-   **Suggested Next Steps**:
    -   Explore more advanced data cleaning techniques (e.g., regex, string operations).
    -   Learn about time-series specific functions (e.g., `shift()`, `diff()`, window functions).
    -   Integrate with other libraries: Scikit-learn for machine learning, Plotly for interactive visualizations.
    -   Consider alternative data manipulation libraries for large datasets, such as [Polars](https://pola.rs/).

---

## Call to Action
For training and team enablement, contact **Software and Testing Training**.
Watch our Pandas Tutorial for Beginners (6 min) https://youtu.be/ZzCu5YddpEU for a quick overview.

© 2026 Software and Testing Training — Inder P Singh
Commercial use, redistribution, or resale requires permission.
