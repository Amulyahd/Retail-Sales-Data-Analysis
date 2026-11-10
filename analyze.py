from pathlib import Path
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).parent
DATA = ROOT / "data" / "retail_sales.csv"
OUT = ROOT / "outputs"
DB = ROOT / "retail_sales.db"
OUT.mkdir(exist_ok=True)

df = pd.read_csv(DATA, parse_dates=["OrderDate"])
df["Sales"] = df["Quantity"] * df["UnitPrice"]

with sqlite3.connect(DB) as conn:
    df.to_sql("Sales", conn, if_exists="replace", index=False)
    df[["Product", "Category"]].drop_duplicates().to_sql("Products", conn, if_exists="replace", index=False)
    df[["Country"]].drop_duplicates().to_sql("Countries", conn, if_exists="replace", index=False)
    df[["TransactionID", "OrderDate", "Country", "Product", "Quantity", "UnitPrice", "Sales"]].to_sql(
        "Transactions", conn, if_exists="replace", index=False)

summary = pd.DataFrame({
    "Metric": ["Total Revenue", "Total Transactions", "Units Sold", "Average Transaction Value"],
    "Value": [df["Sales"].sum(), df["TransactionID"].nunique(), df["Quantity"].sum(),
              df.groupby("TransactionID")["Sales"].sum().mean()]
})
summary.to_csv(OUT / "sales_summary.csv", index=False)

monthly = df.set_index("OrderDate").resample("MS")["Sales"].sum()
plt.figure(figsize=(10, 5))
monthly.plot(marker="o")
plt.title("Monthly Retail Revenue")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.tight_layout()
plt.savefig(OUT / "monthly_revenue.png", dpi=150)
plt.close()

product_sales = df.groupby("Product")["Sales"].sum().sort_values(ascending=False)
plt.figure(figsize=(9, 5))
product_sales.plot(kind="bar")
plt.title("Revenue by Product")
plt.xlabel("Product")
plt.ylabel("Revenue")
plt.tight_layout()
plt.savefig(OUT / "product_sales.png", dpi=150)
plt.close()

country_sales = df.groupby("Country")["Sales"].sum().sort_values(ascending=False)
country_sales.to_csv(OUT / "country_sales.csv", header=["Revenue"])

print("Analysis complete.")
print(summary.to_string(index=False))
print(f"\nSQLite database created: {DB}")
print(f"Charts and reports saved in: {OUT}")
