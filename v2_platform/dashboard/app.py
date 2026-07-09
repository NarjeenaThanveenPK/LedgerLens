import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from analytics.financial_engine import (
    load_data, get_company_data, get_latest,
    compute_cagr, get_top_performer, compare_two, get_all_metrics_summary
)

st.set_page_config(page_title="LedgerLens", page_icon="🔍", layout="wide")

df = load_data()
companies = sorted(df["Company"].unique().tolist())
years = sorted(df["Fiscal Year"].unique().tolist())

st.title("🔍 LedgerLens")
st.caption("Financial Intelligence Platform — Apple, Microsoft, Tesla (2023–2025)")
st.divider()

tab1, tab2, tab3 = st.tabs(["Overview", "Company Analysis", "Compare"])

with tab1:
    st.subheader("Revenue Overview")
    fig = px.bar(df, x="Fiscal Year", y="Total Revenue", color="Company",
                 barmode="group", labels={"Total Revenue": "Revenue (USD M)"},
                 title="Total Revenue by Company")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Net Income Trend")
    fig2 = px.line(df, x="Fiscal Year", y="Net Income", color="Company",
                   markers=True, labels={"Net Income": "Net Income (USD M)"},
                   title="Net Income Trend")
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Profit Margin (%)")
    fig3 = px.line(df, x="Fiscal Year", y="Profit_Margin_Pct", color="Company",
                   markers=True, title="Profit Margin Over Time",
                   labels={"Profit_Margin_Pct": "Profit Margin (%)"})
    st.plotly_chart(fig3, use_container_width=True)

with tab2:
    selected = st.selectbox("Select Company", companies)
    summary = get_all_metrics_summary(df, selected)

    col1, col2, col3 = st.columns(3)
    col1.metric("Latest Revenue", f"${summary['Latest Revenue (M)']:,.0f}M")
    col2.metric("Net Income", f"${summary['Latest Net Income (M)']:,.0f}M")
    col3.metric("Profit Margin", f"{summary['Profit Margin (%)']:.1f}%")

    col4, col5, col6 = st.columns(3)
    col4.metric("Revenue CAGR", f"{summary['Revenue CAGR (%)']:.1f}%")
    col5.metric("Debt to Assets", f"{summary['Debt to Assets']:.2f}")
    col6.metric("Operating Cash Flow", f"${summary['Operating Cash Flow (M)']:,.0f}M")

    company_data = get_company_data(df, selected)

    fig4 = px.bar(company_data, x="Fiscal Year", y="Total Revenue",
                  title=f"{selected} Revenue Trend",
                  labels={"Total Revenue": "Revenue (USD M)"})
    st.plotly_chart(fig4, use_container_width=True)

    fig5 = px.bar(company_data, x="Fiscal Year",
                  y=["Total Assets", "Total Liabilities"],
                  barmode="group",
                  title=f"{selected} Assets vs Liabilities",
                  labels={"value": "USD Millions"})
    st.plotly_chart(fig5, use_container_width=True)

with tab3:
    col1, col2 = st.columns(2)
    company_a = col1.selectbox("Company A", companies, index=0)
    company_b = col2.selectbox("Company B", companies, index=1)

    metric = st.selectbox("Metric", [
        "Total Revenue", "Net Income",
        "Operating Cash Flow", "Profit_Margin_Pct"
    ])

    filtered = df[df["Company"].isin([company_a, company_b])]
    fig6 = px.line(filtered, x="Fiscal Year", y=metric, color="Company",
                   markers=True,
                   title=f"{company_a} vs {company_b} — {metric}")
    st.plotly_chart(fig6, use_container_width=True)

    result = compare_two(df, company_a, company_b, metric)
    st.success(f"Winner on {metric}: **{result['winner']}**")