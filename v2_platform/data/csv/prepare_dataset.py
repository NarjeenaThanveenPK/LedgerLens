import pandas as pd

df = pd.read_csv("data/csv/financial_data.csv")

numeric_cols = ["Total Revenue", "Net Income", "Total Assets", 
                "Total Liabilities", "Operating Cash Flow"]

for col in numeric_cols:
    df[col] = (
        df[col].astype(str)
        .str.replace(",", "", regex=False)
        .astype(float)
    )

df = df.sort_values(["Company", "Year"]).reset_index(drop=True)

df["Revenue_Growth_Pct"] = df.groupby("Company")["Total Revenue"].pct_change() * 100
df["NetIncome_Growth_Pct"] = df.groupby("Company")["Net Income"].pct_change() * 100
df["Profit_Margin_Pct"] = (df["Net Income"] / df["Total Revenue"]) * 100
df["Debt_to_Assets"] = df["Total Liabilities"] / df["Total Assets"]

df = df.round(2)
df.to_csv("data/csv/financial_data_processed.csv", index=False)

print("Dataset ready.")
print(df[["Company", "Year", "Total Revenue", "Profit_Margin_Pct", "Debt_to_Assets"]])