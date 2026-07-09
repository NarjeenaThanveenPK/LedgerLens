
import pandas as pd

# ==============================
# GFC Financial Insights Assistant
# BCG GenAI Job Simulation - Task 2
# ==============================

# Load dataset
df = pd.read_csv("financial_data.csv")

# Convert numeric columns
numeric_cols = [
    "Total Revenue",
    "Net Income",
    "Total Assets",
    "Total Liabilities",
    "Operating Cash Flow"
]

for col in numeric_cols:
    df[col] = (
        df[col]
        .astype(str)
        .str.replace(",", "", regex=False)
        .astype(float)
    )

# Sort and calculate growth metrics
df = df.sort_values(["Company", "Year"])

df["Revenue Growth (%)"] = (
    df.groupby("Company")["Total Revenue"].pct_change() * 100
)

df["Net Income Growth (%)"] = (
    df.groupby("Company")["Net Income"].pct_change() * 100
)

def get_company_data(company, year=2025):
    return df[(df["Company"] == company) & (df["Year"] == year)].iloc[0]

def suggest():
    print("\n💡 You can also ask:")
    print("• Which company had the highest revenue?")
    print("• Which company had the highest net income?")
    print("• How did Microsoft's revenue change?")
    print("• How did Tesla's profit change?")
    print("• Compare Apple and Microsoft")
    print("• Which company appears financially strongest?")
    print("• What is operating cash flow?")

def chatbot():
    print("=" * 60)
    print("        GFC Financial Insights Assistant")
    print("=" * 60)
    print("\nHello! 👋")
    print("Welcome to the GFC Financial Insights Assistant.")
    print("I can help you understand the financial performance")
    print("of Microsoft, Apple and Tesla using their annual reports.")

    print("\nType HELP to see the available questions.")
    print("Type EXIT to quit.")

    while True:
        query = input("\nAsk your question: ").strip().lower()

        if query == "exit":
            print("\nThank you for using GFC Financial Insights Assistant!")
            break

        elif query == "help":
            suggest()

        elif ("highest" in query or "top" in query) and ("revenue" in query or "sales" in query):
            highest = df[df["Year"] == 2025].sort_values("Total Revenue", ascending=False).iloc[0]
            print("\n📊 Financial Insight")
            print("-"*50)
            print(f"{highest['Company']} generated the highest revenue in 2025 with approximately USD {highest['Total Revenue']:,.0f} million.")
            print(
                f"\nIn simple terms, {highest['Company']} earned more money "
                "from selling its products and services than the other "
                "companies during 2025."
            )
            suggest()

        elif ("highest" in query or "top" in query) and ("profit" in query or "net income" in query):
            highest = df[df["Year"] == 2025].sort_values("Net Income", ascending=False).iloc[0]
            print("\n📊 Financial Insight")
            print("-"*50)
            print(f"{highest['Company']} reported the highest net income in 2025 with approximately USD {highest['Net Income']:,.0f} million.")
            print("\nThis means it retained the most profit after covering its business expenses.")
            suggest()

        elif "microsoft" in query and ("growth" in query or "change" in query or "revenue" in query):
            data = get_company_data("Microsoft")
            g = data["Revenue Growth (%)"]
            print("\n📊 Financial Insight")
            print("-"*50)
            print(f"Microsoft's revenue increased by {g:.2f}% from 2024 to 2025.")
            print("\nIn simple terms, Microsoft earned more money from its products and services than it did the previous year.")
            suggest()

        elif "tesla" in query and ("profit" in query or "net income" in query):
            data = get_company_data("Tesla")
            g = data["Net Income Growth (%)"]
            direction = "decreased" if g < 0 else "increased"
            print("\n📊 Financial Insight")
            print("-"*50)
            print(f"Tesla's net income {direction} by {abs(g):.2f}% from 2024 to 2025.")
            print("\nIn simple terms, Tesla made less profit in 2025 than in the previous year." if g<0 else "\nTesla earned more profit than the previous year.")
            suggest()

        elif "operating cash flow" in query or ("cash flow" in query and "what" in query):
            print("\n📘 Operating Cash Flow")
            print("-"*50)
            print("Operating cash flow is the cash a company generates")
            print("from its everyday business activities.")
            print("In simple terms, it shows whether a company's normal")
            print("business operations are bringing in cash.")
            print("A healthy operating cash flow usually indicates")
            print("that the business is financially stable.")
            suggest()

        elif "compare" in query and "apple" in query and "microsoft" in query:
            a = get_company_data("Apple")
            m = get_company_data("Microsoft")
            print("\n📊 Company Comparison")
            print("-"*50)
            print(f"Apple generated higher revenue (USD {a['Total Revenue']:,.0f} million) than Microsoft (USD {m['Total Revenue']:,.0f} million) in 2025.")
            print(f"Apple also reported higher net income than Microsoft.")
            print("However, Microsoft maintained strong and consistent revenue growth.")
            suggest()

        elif ("best" in query or "strongest" in query) and ("company" in query or "performance" in query):
            print("\n📊 Overall Financial Performance")
            print("-"*50)
            print("Based on the available data, Apple appears to have the strongest overall financial performance in 2025.")
            print("It recorded the highest revenue and highest net income among the three companies.")
            print("This suggests Apple generated the most sales while also retaining the highest profit.")
            suggest()

        else:
            print("\nSorry, I can only answer predefined financial questions.")
            print("Type HELP to see available questions.")

if __name__ == "__main__":
    chatbot()
