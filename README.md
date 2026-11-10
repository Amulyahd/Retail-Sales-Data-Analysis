# Retail Sales Data Analysis

A beginner-friendly data analytics project using **Python, Pandas, SQLite, Matplotlib and Streamlit**.

## Features
- Reads retail transaction data from CSV.
- Calculates revenue, number of transactions, units sold and average order value.
- Analyzes monthly revenue, product performance and country performance.
- Saves structured tables to SQLite.
- Provides an interactive dashboard with country, product and date filters.
- Allows filtered data to be downloaded as CSV.

## Project structure
```text
Retail-Sales-Data-Analysis/
├── app.py
├── analyze.py
├── requirements.txt
├── README.md
├── data/
│   └── retail_sales.csv
└── outputs/
```

## Run on Windows (PowerShell)
```powershell
python -m venv venv
venv\\Scripts\\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python analyze.py
streamlit run app.py
```
Open the local URL shown by Streamlit (usually http://localhost:8501).

## Dataset columns
- `TransactionID`: unique transaction identifier
- `OrderDate`: transaction date
- `Country`: customer country
- `Product`: product name
- `Category`: product category
- `Quantity`: number of units
- `UnitPrice`: price per unit
- `Sales`: Quantity × UnitPrice

## Database
Running `analyze.py` creates `retail_sales.db` with four tables: `Countries`, `Products`, `Transactions`, and `Sales`.

## Notes
The included CSV is synthetic sample data created for this project. It is not real customer or company data. The project is for educational demonstration and portfolio use.
