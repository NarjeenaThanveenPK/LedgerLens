import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from analytics.financial_engine import (
    load_data, get_company_data, get_latest,
    compute_cagr, get_top_performer, compare_two, get_all_metrics_summary
)

st.set_page_config(
    page_title="LedgerLens",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background-color: #0F172A;
    color: #F1F5F9;
    font-family: 'Inter', sans-serif;
}
[data-testid="stSidebar"] {
    background-color: #0B1120;
    border-right: 1px solid #1E293B;
    min-width: 220px !important;
    max-width: 220px !important;
}
section[data-testid="stSidebarContent"] {
    padding: 0 12px !important;
}
#MainMenu, footer, header {visibility: hidden;}
[data-testid="stToolbar"] {display: none;}

/* Ghost nav buttons */
[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    color: #64748B !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 9px 14px !important;
    font-weight: 500 !important;
    font-size: 13px !important;
    text-align: left !important;
    width: 100% !important;
    transition: all 0.15s !important;
    box-shadow: none !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: #1E293B !important;
    color: #F1F5F9 !important;
    box-shadow: none !important;
}
[data-testid="stSidebar"] .stButton > button:focus {
    box-shadow: none !important;
    outline: none !important;
}

/* Main content buttons stay blue */
[data-testid="stMain"] .stButton > button {
    background: #2563EB !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 10px 20px !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    transition: all 0.15s !important;
}
[data-testid="stMain"] .stButton > button:hover {
    background: #1D4ED8 !important;
}

.card {
    background: #1E293B;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 16px;
}
.clickable-card {
    background: #1E293B;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 24px;
    cursor: pointer;
    transition: all 0.2s;
    height: 100%;
}
.clickable-card:hover {
    border-color: #2563EB;
    background: #1a2744;
}
.metric-card {
    background: #1E293B;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 20px 24px;
}
.metric-label {
    color: #64748B;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 8px;
}
.metric-value {
    color: #F1F5F9;
    font-size: 22px;
    font-weight: 700;
    margin-bottom: 4px;
}
.metric-delta-pos { color: #22C55E; font-size: 12px; font-weight: 600; }
.metric-delta-neg { color: #EF4444; font-size: 12px; font-weight: 600; }
.stat-card {
    background: #1E293B;
    border: 1px solid #334155;
    border-radius: 10px;
    padding: 16px 20px;
    text-align: center;
}
.stat-number {
    font-size: 28px;
    font-weight: 700;
    color: #2563EB;
}
.stat-label {
    font-size: 11px;
    color: #64748B;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-top: 4px;
}
.section-title {
    font-size: 16px;
    font-weight: 600;
    color: #F1F5F9;
    margin-bottom: 16px;
    margin-top: 8px;
}
.page-title {
    font-size: 24px;
    font-weight: 700;
    color: #F1F5F9;
    margin-bottom: 4px;
}
.page-subtitle {
    font-size: 13px;
    color: #64748B;
    margin-bottom: 28px;
}
.home-title {
    font-size: 44px;
    font-weight: 700;
    color: #F1F5F9;
    text-align: center;
    letter-spacing: -0.5px;
}
.home-subtitle {
    font-size: 15px;
    color: #64748B;
    text-align: center;
    margin-bottom: 36px;
    line-height: 1.6;
}
.suggestion-chip {
    display: inline-block;
    padding: 7px 14px;
    background: #1E293B;
    border: 1px solid #334155;
    border-radius: 20px;
    color: #94A3B8;
    font-size: 12px;
    margin: 4px;
}
.chat-message-user {
    background: #1E3A5F;
    border-radius: 12px 12px 4px 12px;
    padding: 14px 18px;
    margin: 12px 0;
    color: #F1F5F9;
    font-size: 14px;
    max-width: 75%;
    margin-left: auto;
}
.chat-message-ai {
    background: #1E293B;
    border: 1px solid #334155;
    border-radius: 12px 12px 12px 4px;
    padding: 14px 18px;
    margin: 12px 0;
    color: #F1F5F9;
    font-size: 14px;
    max-width: 85%;
}
.chat-label {
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 8px;
}
.chat-label-user { color: #3B82F6; }
.chat-label-ai { color: #22C55E; }
.winner-badge {
    background: #14532D;
    border: 1px solid #22C55E;
    color: #22C55E;
    border-radius: 6px;
    padding: 3px 10px;
    font-size: 11px;
    font-weight: 600;
    display: inline-block;
    margin-top: 6px;
}
.stSelectbox > div > div {
    background-color: #1E293B !important;
    border-color: #334155 !important;
    color: #F1F5F9 !important;
}
.stTextInput > div > div > input {
    background-color: #1E293B !important;
    border: 1.5px solid #334155 !important;
    color: #F1F5F9 !important;
    border-radius: 24px !important;
    padding: 14px 20px !important;
    font-size: 15px !important;
    box-shadow: 0 2px 12px rgba(0,0,0,0.3) !important;
    transition: all 0.2s !important;
}
.stTextInput > div > div > input:focus {
    border-color: #2563EB !important;
    box-shadow: 0 0 0 3px rgba(37,99,235,0.15) !important;
    outline: none !important;
}
.stTextInput > div {
    border: none !important;
}
div[data-testid="stHorizontalBlock"] { gap: 12px; }
</style>
""", unsafe_allow_html=True)

# ── Session State ──
if "page" not in st.session_state:
    st.session_state.page = "Home"
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ── Data ──
df = load_data()
df["Fiscal Year"] = df["Fiscal Year"].astype(str)
companies = sorted(df["Company"].unique().tolist())
years = sorted(df["Fiscal Year"].unique().tolist())

CHART_THEME = dict(
    paper_bgcolor="#0F172A",
    plot_bgcolor="#0F172A",
    font_color="#94A3B8",
    font_size=12,
    xaxis=dict(gridcolor="#1E293B", linecolor="#334155"),
    yaxis=dict(gridcolor="#1E293B", linecolor="#334155")
)
COLORS = ["#2563EB", "#22C55E", "#F59E0B"]

# ── Sidebar ──
with st.sidebar:
    st.markdown("""
    <div style="padding:24px 8px 20px;">
        <div style="font-size:18px;font-weight:700;color:#F1F5F9;letter-spacing:-0.3px;">LedgerLens</div>
        <div style="font-size:10px;color:#334155;margin-top:3px;text-transform:uppercase;letter-spacing:0.1em;">Financial Intelligence</div>
    </div>
    """, unsafe_allow_html=True)

    nav_items = ["Home", "AI Assistant", "Dashboard", "Compare", "Reports", "About"]
    for item in nav_items:
        if st.button(item, key=f"nav_{item}", use_container_width=True):
            st.session_state.page = item
            st.rerun()

    st.markdown("<div style='height:1px;background:#1E293B;margin:20px 0 16px;'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="padding:0 4px;">
        <div style="font-size:10px;color:#334155;font-weight:600;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:10px;">Coverage</div>
        <div style="font-size:12px;color:#475569;line-height:1.8;">
            Apple · Microsoft · Tesla<br>
            FY 2023 · 2024 · 2025<br>
            SEC 10-K Filings
        </div>
    </div>
    """, unsafe_allow_html=True)

page = st.session_state.page

# ────────────────────────────────────────
# HOME
# ────────────────────────────────────────
if page == "Home":
    st.markdown("<div style='height:48px'></div>", unsafe_allow_html=True)
    st.markdown("<div class='home-title'>LedgerLens</div>", unsafe_allow_html=True)
    st.markdown("<div class='home-subtitle'>Financial Intelligence Platform<br>Analyze SEC 10-K filings using AI, financial analytics, and semantic search.</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2.5, 1])
    with col2:
        query = st.text_input("", placeholder="Ask anything — Compare Apple and Microsoft, Analyze Tesla risks...", label_visibility="collapsed")
        if st.button("Analyze", use_container_width=True):
            if query:
                st.session_state.chat_history.append({"role": "user", "content": query})
                st.session_state.page = "AI Assistant"
                st.rerun()

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align:center;margin-bottom:48px;'>
        <div style='font-size:11px;color:#334155;margin-bottom:10px;text-transform:uppercase;letter-spacing:0.1em;'>Try asking</div>
        <span class='suggestion-chip'>Compare Microsoft and Apple</span>
        <span class='suggestion-chip'>Analyze Tesla's risks</span>
        <span class='suggestion-chip'>Apple revenue trend</span>
        <span class='suggestion-chip'>What is ROE?</span>
        <span class='suggestion-chip'>Microsoft profit margin 2025</span>
    </div>
    """, unsafe_allow_html=True)

    # Stats row
    st.markdown("<div style='font-size:11px;color:#334155;text-align:center;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:16px;'>Platform Coverage</div>", unsafe_allow_html=True)
    s1, s2, s3, s4 = st.columns(4)
    for col, num, label in zip(
        [s1, s2, s3, s4],
        ["3", "3", "9", "15+"],
        ["Companies", "Fiscal Years", "SEC Reports", "Financial Metrics"]
    ):
        col.markdown(f"""
        <div class='stat-card'>
            <div class='stat-number'>{num}</div>
            <div class='stat-label'>{label}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:11px;color:#334155;text-align:center;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:16px;'>What would you like to do?</div>", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    cards = [
        ("AI Assistant", "Ask questions about SEC filings in plain English with cited answers."),
        ("Analytics Dashboard", "Interactive financial charts, ratios, and trend analysis."),
        ("Company Compare", "Side-by-side comparison across all financial metrics."),
        ("Report Generator", "Generate executive summaries with charts and insights."),
    ]
    for col, (title, desc) in zip([c1, c2, c3, c4], cards):
        clicked = col.button(title, key=f"home_card_{title}", use_container_width=True)
        if clicked:
            page_map = {
                "AI Assistant": "AI Assistant",
                "Analytics Dashboard": "Dashboard",
                "Company Compare": "Compare",
                "Report Generator": "Reports"
            }
            st.session_state.page = page_map[title]
            st.rerun()
        col.markdown(f"<div style='font-size:12px;color:#475569;padding:8px 4px;'>{desc}</div>", unsafe_allow_html=True)

# ────────────────────────────────────────
# AI ASSISTANT
# ────────────────────────────────────────
elif page == "AI Assistant":
    st.markdown("<div class='page-title'>AI Assistant</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-subtitle'>Ask questions about Apple, Microsoft, and Tesla SEC 10-K filings</div>", unsafe_allow_html=True)

    if not st.session_state.chat_history:
        st.markdown("""
        <div class='card' style='text-align:center;padding:48px 40px;'>
            <div style='font-size:15px;color:#475569;font-weight:600;margin-bottom:12px;'>Start a conversation</div>
            <div style='font-size:13px;color:#334155;'>Ask about revenue, profit margins, risks, AI investments, or compare companies.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(f"""
                <div style='display:flex;justify-content:flex-end;margin:8px 0;'>
                    <div class='chat-message-user'>
                        <div class='chat-label chat-label-user'>You</div>
                        {msg['content']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class='chat-message-ai'>
                    <div class='chat-label chat-label-ai'>LedgerLens</div>
                    {msg['content']}
                </div>
                """, unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.text_input("", placeholder="Ask about financials, risks, strategy, or comparisons...", label_visibility="collapsed", key="chat_input")
    with col2:
        send = st.button("Send", use_container_width=True)

    if send and user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": "Gemini integration coming in Phase 5. RAG pipeline will power responses with citations from actual 10-K filings."
        })
        st.rerun()

    if st.session_state.chat_history:
        if st.button("Clear conversation"):
            st.session_state.chat_history = []
            st.rerun()

# ────────────────────────────────────────
# DASHBOARD
# ────────────────────────────────────────
elif page == "Dashboard":
    st.markdown("<div class='page-title'>Analytics Dashboard</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-subtitle'>Financial metrics and trends — Apple, Microsoft, Tesla (FY 2023–2025)</div>", unsafe_allow_html=True)

    selected_company = st.selectbox("Select Company", ["All Companies"] + companies)

    if selected_company == "All Companies":
        view_df = df.copy()
    else:
        view_df = get_company_data(df, selected_company)
        view_df["Fiscal Year"] = view_df["Fiscal Year"].astype(str)

    if selected_company != "All Companies":
        summary = get_all_metrics_summary(df, selected_company)
        cagr = summary["Revenue CAGR (%)"]
        c1, c2, c3, c4, c5, c6 = st.columns(6)
        metrics = [
            ("Revenue", f"${summary['Latest Revenue (M)']:,.0f}M", None),
            ("Net Income", f"${summary['Latest Net Income (M)']:,.0f}M", None),
            ("Profit Margin", f"{summary['Profit Margin (%)']:.1f}%", None),
            ("Revenue CAGR", f"{cagr:.1f}%", cagr),
            ("Debt / Assets", f"{summary['Debt to Assets']:.2f}", None),
            ("Cash Flow", f"${summary['Operating Cash Flow (M)']:,.0f}M", None),
        ]
        for col, (label, value, delta) in zip([c1, c2, c3, c4, c5, c6], metrics):
            delta_html = ""
            if delta is not None:
                cls = "metric-delta-pos" if delta >= 0 else "metric-delta-neg"
                arrow = "↑" if delta >= 0 else "↓"
                delta_html = f"<div class='{cls}'>{arrow} {abs(delta):.1f}%</div>"
            col.markdown(f"""
            <div class='metric-card'>
                <div class='metric-label'>{label}</div>
                <div class='metric-value'>{value}</div>
                {delta_html}
            </div>
            """, unsafe_allow_html=True)
        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    st.markdown("<div class='section-title'>Revenue Trend</div>", unsafe_allow_html=True)
    fig1 = px.bar(view_df, x="Fiscal Year", y="Total Revenue",
                  color="Company" if selected_company == "All Companies" else None,
                  barmode="group", color_discrete_sequence=COLORS,
                  category_orders={"Fiscal Year": years})
    fig1.update_layout(**CHART_THEME, height=360, margin=dict(l=0, r=0, t=10, b=0))
    st.plotly_chart(fig1, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='section-title'>Net Income</div>", unsafe_allow_html=True)
        fig2 = px.line(view_df, x="Fiscal Year", y="Net Income",
                       color="Company" if selected_company == "All Companies" else None,
                       markers=True, color_discrete_sequence=COLORS,
                       category_orders={"Fiscal Year": years})
        fig2.update_layout(**CHART_THEME, height=300, margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        st.markdown("<div class='section-title'>Profit Margin (%)</div>", unsafe_allow_html=True)
        fig3 = px.line(view_df, x="Fiscal Year", y="Profit_Margin_Pct",
                       color="Company" if selected_company == "All Companies" else None,
                       markers=True, color_discrete_sequence=COLORS,
                       category_orders={"Fiscal Year": years})
        fig3.update_layout(**CHART_THEME, height=300, margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig3, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown("<div class='section-title'>Operating Cash Flow</div>", unsafe_allow_html=True)
        fig4 = px.bar(view_df, x="Fiscal Year", y="Operating Cash Flow",
                      color="Company" if selected_company == "All Companies" else None,
                      barmode="group", color_discrete_sequence=COLORS,
                      category_orders={"Fiscal Year": years})
        fig4.update_layout(**CHART_THEME, height=300, margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig4, use_container_width=True)

    with col4:
        st.markdown("<div class='section-title'>Debt to Assets</div>", unsafe_allow_html=True)
        fig5 = px.line(view_df, x="Fiscal Year", y="Debt_to_Assets",
                       color="Company" if selected_company == "All Companies" else None,
                       markers=True, color_discrete_sequence=COLORS,
                       category_orders={"Fiscal Year": years})
        fig5.update_layout(**CHART_THEME, height=300, margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig5, use_container_width=True)

# ────────────────────────────────────────
# COMPARE
# ────────────────────────────────────────
elif page == "Compare":
    st.markdown("<div class='page-title'>Compare Companies</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-subtitle'>Side-by-side financial comparison across all metrics</div>", unsafe_allow_html=True)

    col1, col_vs, col2 = st.columns([2, 1, 2])
    with col1:
        company_a = st.selectbox("Company A", companies, index=0)
    with col_vs:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        st.markdown("<div style='text-align:center;padding:8px;font-size:12px;font-weight:700;color:#475569;background:#1E293B;border-radius:50%;width:36px;height:36px;line-height:20px;margin:auto;'>VS</div>", unsafe_allow_html=True)
    with col2:
        company_b = st.selectbox("Company B", companies, index=1)

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    sum_a = get_all_metrics_summary(df, company_a)
    sum_b = get_all_metrics_summary(df, company_b)

    metrics_compare = [
        ("Latest Revenue (M)", "Revenue", "$", "M"),
        ("Latest Net Income (M)", "Net Income", "$", "M"),
        ("Profit Margin (%)", "Profit Margin", "", "%"),
        ("Revenue CAGR (%)", "Revenue CAGR", "", "%"),
        ("Debt to Assets", "Debt to Assets", "", ""),
        ("Operating Cash Flow (M)", "Cash Flow", "$", "M"),
    ]

    for metric_key, label, prefix, suffix in metrics_compare:
        val_a = sum_a[metric_key]
        val_b = sum_b[metric_key]
        winner = company_a if val_a > val_b else company_b
        ca, cb, cc = st.columns([2, 1, 2])
        with ca:
            border = "border-color:#22C55E;" if winner == company_a else ""
            st.markdown(f"""
            <div class='metric-card' style='{border}margin-bottom:8px;'>
                <div class='metric-label'>{company_a}</div>
                <div class='metric-value'>{prefix}{val_a:,.1f}{suffix}</div>
                {"<span class='winner-badge'>Winner</span>" if winner == company_a else ""}
            </div>""", unsafe_allow_html=True)
        with cb:
            st.markdown(f"<div style='text-align:center;padding-top:24px;font-size:11px;color:#475569;font-weight:600;text-transform:uppercase;letter-spacing:0.06em;'>{label}</div>", unsafe_allow_html=True)
        with cc:
            border = "border-color:#22C55E;" if winner == company_b else ""
            st.markdown(f"""
            <div class='metric-card' style='{border}margin-bottom:8px;'>
                <div class='metric-label'>{company_b}</div>
                <div class='metric-value'>{prefix}{val_b:,.1f}{suffix}</div>
                {"<span class='winner-badge'>Winner</span>" if winner == company_b else ""}
            </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Revenue Trend Comparison</div>", unsafe_allow_html=True)
    filtered = df[df["Company"].isin([company_a, company_b])]
    fig_comp = px.line(filtered, x="Fiscal Year", y="Total Revenue",
                       color="Company", markers=True,
                       color_discrete_sequence=[COLORS[0], COLORS[1]],
                       category_orders={"Fiscal Year": years})
    fig_comp.update_layout(**CHART_THEME, height=350, margin=dict(l=0, r=0, t=10, b=0))
    st.plotly_chart(fig_comp, use_container_width=True)

    st.markdown("<div class='section-title'>Financial Profile Radar</div>", unsafe_allow_html=True)
    radar_metrics = ["Profit_Margin_Pct", "Revenue_Growth_Pct", "Debt_to_Assets"]
    radar_labels = ["Profit Margin", "Revenue Growth", "Debt Ratio"]
    latest_a = get_latest(df, company_a)
    latest_b = get_latest(df, company_b)
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=[abs(float(latest_a[m])) for m in radar_metrics],
        theta=radar_labels, fill='toself', name=company_a, line_color=COLORS[0]))
    fig_radar.add_trace(go.Scatterpolar(
        r=[abs(float(latest_b[m])) for m in radar_metrics],
        theta=radar_labels, fill='toself', name=company_b, line_color=COLORS[1]))
    fig_radar.update_layout(
        polar=dict(bgcolor="#1E293B",
                   radialaxis=dict(visible=True, gridcolor="#334155", color="#64748B"),
                   angularaxis=dict(gridcolor="#334155", color="#64748B")),
        paper_bgcolor="#0F172A", font_color="#94A3B8",
        height=400, margin=dict(l=40, r=40, t=40, b=40))
    st.plotly_chart(fig_radar, use_container_width=True)

# ────────────────────────────────────────
# REPORTS
# ────────────────────────────────────────
elif page == "Reports":
    st.markdown("<div class='page-title'>Report Generator</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-subtitle'>Generate executive financial summaries from SEC 10-K data</div>", unsafe_allow_html=True)

    selected = st.selectbox("Select Company", companies)

    if st.button("Generate Report"):
        with st.spinner("Compiling financial data..."):
            summary = get_all_metrics_summary(df, selected)
            company_data = get_company_data(df, selected)
            company_data["Fiscal Year"] = company_data["Fiscal Year"].astype(str)

            st.markdown(f"""
            <div class='card'>
                <div style='font-size:10px;color:#475569;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:6px;'>Executive Report</div>
                <div style='font-size:20px;font-weight:700;color:#F1F5F9;'>{selected} Corporation</div>
                <div style='font-size:12px;color:#64748B;margin-top:4px;'>Based on SEC 10-K Filings · FY 2023–2025</div>
            </div>
            """, unsafe_allow_html=True)

            c1, c2, c3 = st.columns(3)
            c1.markdown(f"<div class='metric-card'><div class='metric-label'>Revenue (Latest FY)</div><div class='metric-value'>${summary['Latest Revenue (M)']:,.0f}M</div></div>", unsafe_allow_html=True)
            c2.markdown(f"<div class='metric-card'><div class='metric-label'>Net Income</div><div class='metric-value'>${summary['Latest Net Income (M)']:,.0f}M</div></div>", unsafe_allow_html=True)
            c3.markdown(f"<div class='metric-card'><div class='metric-label'>Profit Margin</div><div class='metric-value'>{summary['Profit Margin (%)']:.1f}%</div></div>", unsafe_allow_html=True)

            fig_r = px.bar(company_data, x="Fiscal Year", y="Total Revenue",
                           color_discrete_sequence=[COLORS[0]],
                           category_orders={"Fiscal Year": years})
            fig_r.update_layout(**CHART_THEME, height=280, margin=dict(l=0, r=0, t=10, b=0))
            st.plotly_chart(fig_r, use_container_width=True)

            cagr = summary["Revenue CAGR (%)"]
            direction = "grew" if cagr > 0 else "declined"
            st.markdown(f"""
            <div class='card'>
                <div style='font-size:13px;font-weight:600;color:#F1F5F9;margin-bottom:10px;'>Financial Summary</div>
                <div style='font-size:13px;color:#94A3B8;line-height:1.8;'>
                    {selected}'s revenue {direction} at a CAGR of {abs(cagr):.1f}% between FY2023 and FY2025.
                    The latest profit margin stands at {summary['Profit Margin (%)']:.1f}%, with a debt-to-assets ratio of {summary['Debt to Assets']:.2f}.
                    Operating cash flow of ${summary['Operating Cash Flow (M)']:,.0f}M reflects the company's ability to generate cash from core operations.
                </div>
            </div>
            <div class='card' style='border-left:3px solid #2563EB;margin-top:0;'>
                <div style='font-size:11px;color:#2563EB;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:6px;'>Coming in Phase 5</div>
                <div style='font-size:13px;color:#64748B;'>AI-generated insights and PDF export will be available after Gemini integration.</div>
            </div>
            """, unsafe_allow_html=True)

# ────────────────────────────────────────
# ABOUT
# ────────────────────────────────────────
elif page == "About":
    st.markdown("<div class='page-title'>About LedgerLens</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-subtitle'>Purpose, architecture, and technology</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class='card'>
        <div style='font-size:13px;font-weight:600;color:#F1F5F9;margin-bottom:8px;'>Why LedgerLens?</div>
        <div style='font-size:13px;color:#94A3B8;line-height:1.8;'>
        Financial reports contain thousands of pages of information that are difficult for non-finance professionals to analyze.
        LedgerLens combines a financial analytics engine, semantic search over SEC filings, and large language models
        to help users explore corporate financial data through natural language — with every answer grounded in real documents.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='section-title'>Platform Statistics</div>", unsafe_allow_html=True)
    s1, s2, s3, s4, s5 = st.columns(5)
    for col, num, label in zip(
        [s1, s2, s3, s4, s5],
        ["3", "9", "15+", "2,000+", "5"],
        ["Companies", "SEC Reports", "Financial Metrics", "Vector Chunks", "Platform Modules"]
    ):
        col.markdown(f"<div class='stat-card'><div class='stat-number'>{num}</div><div class='stat-label'>{label}</div></div>", unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Architecture</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='card' style='font-family:monospace;font-size:12px;color:#64748B;line-height:2.2;'>
        User Query &nbsp;→&nbsp; Streamlit Interface &nbsp;→&nbsp; Query Processing<br>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↓&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↓<br>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style='color:#2563EB;'>Financial Engine</span>&nbsp;&nbsp;&nbsp;&nbsp;<span style='color:#22C55E;'>RAG Pipeline</span><br>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Pandas · Ratios&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;LangChain · FAISS<br>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↓&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↓<br>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style='color:#F59E0B;'>Gemini LLM</span><br>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↓<br>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Summary · Metrics · Charts · Sources
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='section-title'>Tech Stack</div>", unsafe_allow_html=True)
    tech = [
        ("Python + Pandas", "Data processing and financial ratio computation"),
        ("LangChain", "RAG pipeline orchestration"),
        ("FAISS", "Vector database for semantic search"),
        ("HuggingFace", "Sentence embeddings"),
        ("Google Gemini", "LLM for answer generation"),
        ("PyMuPDF", "PDF text extraction from SEC filings"),
        ("Plotly", "Interactive financial charts"),
        ("Streamlit", "Web platform framework"),
    ]
    c1, c2 = st.columns(2)
    for i, (name, desc) in enumerate(tech):
        col = c1 if i % 2 == 0 else c2
        col.markdown(f"""
        <div class='card' style='padding:14px 18px;margin-bottom:8px;'>
            <div style='font-size:13px;font-weight:600;color:#F1F5F9;margin-bottom:3px;'>{name}</div>
            <div style='font-size:12px;color:#475569;'>{desc}</div>
        </div>
        """, unsafe_allow_html=True)