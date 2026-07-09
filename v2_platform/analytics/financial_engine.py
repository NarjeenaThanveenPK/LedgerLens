import pandas as pd

DATA_PATH = "data/csv/financial_data_processed.csv"

def load_data():
    return pd.read_csv(DATA_PATH)

def get_company_data(df, company):
    return df[df["Company"] == company].sort_values("Fiscal Year").reset_index(drop=True)

def get_latest(df, company):
    data = get_company_data(df, company)
    return data.iloc[-1]

def compute_cagr(df, company, metric):
    data = get_company_data(df, company)
    start = data[metric].iloc[0]
    end = data[metric].iloc[-1]
    years = len(data) - 1
    if start <= 0 or years == 0:
        return None
    return round(((end / start) ** (1 / years) - 1) * 100, 2)

def get_top_performer(df, metric, year):
    year_data = df[df["Fiscal Year"] == year]
    top = year_data.loc[year_data[metric].idxmax()]
    return top["Company"], round(top[metric], 2)

def compare_two(df, company_a, company_b, metric):
    a = get_latest(df, company_a)
    b = get_latest(df, company_b)
    return {
        company_a: round(a[metric], 2),
        company_b: round(b[metric], 2),
        "winner": company_a if a[metric] > b[metric] else company_b
    }

def get_all_metrics_summary(df, company):
    latest = get_latest(df, company)
    cagr = compute_cagr(df, company, "Total Revenue")
    return {
        "Company": company,
        "Latest Revenue (M)": latest["Total Revenue"],
        "Latest Net Income (M)": latest["Net Income"],
        "Profit Margin (%)": round(latest["Profit_Margin_Pct"], 2),
        "Debt to Assets": round(latest["Debt_to_Assets"], 2),
        "Revenue CAGR (%)": cagr,
        "Operating Cash Flow (M)": latest["Operating Cash Flow"]
    }

if __name__ == "__main__":
    df = load_data()
    for company in ["Apple", "Microsoft", "Tesla"]:
        print(get_all_metrics_summary(df, company))
        print()
    print("Top revenue 2025:", get_top_performer(df, "Total Revenue", 2025))
    print("Apple vs Microsoft:", compare_two(df, "Apple", "Microsoft", "Total Revenue"))
    print("Microsoft CAGR:", compute_cagr(df, "Microsoft", "Total Revenue"), "%")