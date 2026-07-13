def compute_health_score(df, company):
    data = df[df["Company"] == company].sort_values("Fiscal Year")
    latest = data.iloc[-1]

    margin = latest["Profit_Margin_Pct"]
    if margin >= 30: prof = 25
    elif margin >= 20: prof = 20
    elif margin >= 10: prof = 14
    elif margin >= 5: prof = 8
    else: prof = 3

    cagr = latest.get("Revenue_Growth_Pct", 0)
    if cagr >= 15: growth = 25
    elif cagr >= 10: growth = 20
    elif cagr >= 5: growth = 14
    elif cagr >= 0: growth = 8
    else: growth = 3

    debt_ratio = latest["Debt_to_Assets"]
    if debt_ratio <= 0.3: safety = 25
    elif debt_ratio <= 0.5: safety = 20
    elif debt_ratio <= 0.65: safety = 14
    elif debt_ratio <= 0.8: safety = 8
    else: safety = 3

    cash_margin = (latest["Operating Cash Flow"] / latest["Total Revenue"]) * 100
    if cash_margin >= 25: cash = 25
    elif cash_margin >= 15: cash = 20
    elif cash_margin >= 8: cash = 14
    elif cash_margin >= 3: cash = 8
    else: cash = 3

    total = prof + growth + safety + cash

    if total >= 85: grade = "Excellent"
    elif total >= 70: grade = "Strong"
    elif total >= 55: grade = "Good"
    elif total >= 40: grade = "Fair"
    else: grade = "Weak"

    return {
        "total": total, "grade": grade,
        "profitability": prof, "growth": growth,
        "safety": safety, "cash": cash
    }