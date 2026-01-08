import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def generate_report():
    # Ensure 'outputs' directory exists
    os.makedirs('outputs', exist_ok=True)

    # Load data, ensuring customer_id is read as nullable integer
    sales_df = pd.read_csv('data/sales_small.csv', dtype={'customer_id': 'Int64'})
    customers_df = pd.read_csv('data/customers_small.csv', dtype={'customer_id': 'Int64'})

    # --- Data Cleaning and Preprocessing ---
    # 1. Impute missing amounts with median
    sales_df['amount'] = sales_df['amount'].fillna(sales_df['amount'].median())
    
    # 2. Drop rows with missing customer_id for merge consistency
    sales_df_cleaned = sales_df.dropna(subset=['customer_id']).copy()
    
    # 3. Impute missing region with mode
    mode_region = sales_df_cleaned['region'].mode()[0]
    sales_df_cleaned['region'] = sales_df_cleaned['region'].fillna(mode_region)
    
    # 4. Convert categorical columns to 'category' dtype for memory optimization
    for col in ['product', 'category', 'region']:
        if col in sales_df_cleaned.columns and sales_df_cleaned[col].dtype == 'object':
            sales_df_cleaned[col] = sales_df_cleaned[col].astype('category')

    # --- Merge Data ---
    # Inner merge to combine sales and customer data where customer_id matches in both
    merged_df = pd.merge(sales_df_cleaned, customers_df, on='customer_id', how='inner', suffixes=('_sales', '_cust'))

    # --- Groupby Aggregation ---
    # Calculate total sales and order count by region and category
    region_category_sales = merged_df.groupby(['region', 'category']).agg(
        total_sales=('amount', 'sum'),
        order_count=('order_id', 'count')
    ).reset_index()

    # --- Save Aggregated CSV Report ---
    report_path_csv = 'outputs/aggregated_report.csv'
    region_category_sales.to_csv(report_path_csv, index=False)
    print(f"Generated report: {report_path_csv}")

    # --- Produce Visualization ---
    plt.figure(figsize=(12, 7))
    sns.barplot(x='region', y='total_sales', hue='category', data=region_category_sales, palette='viridis')
    plt.title('Total Sales by Region and Category')
    plt.xlabel('Region')
    plt.ylabel('Total Sales Amount')
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    # Save plot
    report_path_png = 'outputs/aggregated_plot_script.png'
    plt.savefig(report_path_png)
    print(f"Generated plot: {report_path_png}")
    plt.close() # Close plot to free memory
if __name__ == '__main__':
    generate_report()
    print("Example report generation complete.")