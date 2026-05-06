"""
Nassau Candy Distributor — Product Line Profitability & Margin Performance Dashboard
Theme: Ocean Fresh — Deep navy background with cyan & turquoise accents
Run with: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import math
import os

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Nassau Candy — Profitability Dashboard",
    page_icon="🍬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# OCEAN FRESH THEME CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

    /* ── Global background ── */
    .stApp {
        background: linear-gradient(160deg, #06111F 0%, #0A1C35 45%, #071628 100%);
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    .main .block-container { padding-top: 1.5rem; }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #040D18 0%, #071525 60%, #040D18 100%) !important;
        border-right: 1px solid rgba(6,182,212,0.25);
    }
    [data-testid="stSidebar"] * { color: #BAE6FD !important; }
    [data-testid="stSidebar"] .stSelectbox > div > div,
    [data-testid="stSidebar"] .stTextInput > div > div > input {
        background: rgba(255,255,255,0.06) !important;
        border: 1px solid rgba(6,182,212,0.35) !important;
        color: #BAE6FD !important;
        border-radius: 8px !important;
    }
    [data-testid="stSidebar"] hr { border-color: rgba(6,182,212,0.2); }

    /* ── Main header ── */
    .dash-header {
        background: linear-gradient(135deg, #0C2461 0%, #1565C0 40%, #0891B2 75%, #22D3EE 100%);
        padding: 1.8rem 2.5rem;
        border-radius: 20px;
        margin-bottom: 1.5rem;
        position: relative;
        overflow: hidden;
    }
    .dash-header::before {
        content: '🌊🍬🍭🍫🌊';
        position: absolute;
        right: 2rem;
        top: 50%;
        transform: translateY(-50%);
        font-size: 2rem;
        opacity: 0.3;
        letter-spacing: 6px;
    }
    .dash-header h1 { color: #FFFFFF; font-size: 1.75rem; margin: 0 0 6px; font-weight: 700; }
    .dash-header p  { color: rgba(255,255,255,0.82); margin: 0; font-size: 0.88rem; }

    /* ── KPI cards ── */
    .kpi-card {
        border-radius: 16px;
        padding: 1.2rem 1rem;
        text-align: center;
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .kpi-card::after {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        border-radius: 16px 16px 0 0;
    }
    /* Ocean */
    .kpi-emerald { background: linear-gradient(135deg, rgba(8,50,100,0.75), rgba(5,38,80,0.55)); }
    .kpi-emerald::after { background: linear-gradient(90deg, #22D3EE, #06B6D4); }
    /* Cyan */
    .kpi-gold { background: linear-gradient(135deg, rgba(6,100,140,0.55), rgba(4,80,115,0.4)); }
    .kpi-gold::after { background: linear-gradient(90deg, #00D4FF, #22D3EE); }
    /* Turquoise */
    .kpi-mint { background: linear-gradient(135deg, rgba(8,80,120,0.6), rgba(5,65,100,0.45)); }
    .kpi-mint::after { background: linear-gradient(90deg, #67E8F9, #22D3EE); }
    /* Steel */
    .kpi-sage { background: linear-gradient(135deg, rgba(14,60,110,0.55), rgba(10,45,85,0.4)); }
    .kpi-sage::after { background: linear-gradient(90deg, #7DD3FC, #38BDF8); }
    /* Teal */
    .kpi-amber { background: linear-gradient(135deg, rgba(8,90,120,0.55), rgba(5,70,100,0.4)); }
    .kpi-amber::after { background: linear-gradient(90deg, #A5F3FC, #06B6D4); }

    .kpi-label { font-size: 0.72rem; font-weight: 600; color: rgba(186,230,253,0.7);
                 text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 6px; }
    .kpi-value { font-size: 1.9rem; font-weight: 700; color: #FFFFFF; line-height: 1.1; }
    .kpi-sub   { font-size: 0.68rem; color: rgba(186,230,253,0.55); margin-top: 4px; }

    /* ── Section title ── */
    .section-title {
        font-size: 1rem; font-weight: 700; color: #67E8F9;
        border-left: 4px solid #06B6D4;
        padding-left: 12px; margin-bottom: 1rem;
    }

    /* ── Insight boxes ── */
    .insight-box {
        background: rgba(8,50,100,0.35);
        border: 1px solid rgba(6,182,212,0.3);
        border-left: 4px solid #22D3EE;
        border-radius: 0 12px 12px 0;
        padding: 0.75rem 1.1rem;
        font-size: 0.83rem;
        color: #BAE6FD;
        line-height: 1.6;
        margin-bottom: 0.6rem;
    }

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255,255,255,0.04);
        border-radius: 14px;
        padding: 5px;
        gap: 4px;
        border: 1px solid rgba(6,182,212,0.18);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        color: rgba(186,230,253,0.6) !important;
        font-weight: 500;
        font-size: 0.88rem;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #0369A1, #0891B2) !important;
        color: #FFFFFF !important;
    }

    /* ── Dataframe ── */
    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid rgba(6,182,212,0.22) !important;
    }

    /* ── Misc ── */
    hr { border-color: rgba(6,182,212,0.18) !important; }
    .stCaption { color: rgba(186,230,253,0.45) !important; }
    .stInfo    { background: rgba(8,50,100,0.35) !important; border-color: rgba(6,182,212,0.38) !important; color: #BAE6FD !important; }

    /* ── Sidebar labels & brand ── */
    .sidebar-label {
        font-size: 0.72rem; font-weight: 600; color: rgba(186,230,253,0.65);
        text-transform: uppercase; letter-spacing: 0.8px;
        margin-bottom: 4px; display: block;
    }
    .sidebar-brand { text-align: center; padding: 1rem 0 0.5rem; }
    .sidebar-brand .brand-icon { font-size: 2.5rem; }
    .sidebar-brand .brand-name { font-size: 1.1rem; font-weight: 700; color: #67E8F9; }
    .sidebar-brand .brand-sub  { font-size: 0.72rem; color: rgba(186,230,253,0.55); }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# OCEAN FRESH COLOR PALETTE
# ─────────────────────────────────────────────────────────────────────────────
# Primary chart colours: cyan, turquoise, sky blue, ice blue, azure, teal
OCEAN_PALETTE = [
    "#22D3EE",  # Cyan
    "#06B6D4",  # Turquoise
    "#67E8F9",  # Light cyan
    "#38BDF8",  # Sky blue
    "#0EA5E9",  # Azure
    "#7DD3FC",  # Light blue
    "#A5F3FC",  # Ice cyan
    "#00D4FF",  # Bright cyan
    "#0891B2",  # Deep turquoise
    "#BAE6FD",  # Pale blue
    "#0E7490",  # Dark teal
    "#164E63",  # Navy teal
]
FOREST_PALETTE = OCEAN_PALETTE  # keep alias so existing refs still work

DIV_COLORS    = {"Chocolate": "#22D3EE", "Other": "#38BDF8", "Sugar": "#06B6D4"}
REGION_COLORS = {"Pacific": "#22D3EE", "Atlantic": "#38BDF8", "Interior": "#67E8F9", "Gulf": "#06B6D4"}

# Shared Plotly layout — dark ocean glass
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(255,255,255,0.02)",
    font=dict(family="Plus Jakarta Sans, sans-serif", color="#BAE6FD", size=12),
    title_font=dict(color="#67E8F9", size=14, family="Plus Jakarta Sans, sans-serif"),
    margin=dict(l=45, r=25, t=52, b=42),
)

# Legend presets — applied via update_layout(legend=...) SEPARATELY, never inside **PLOTLY_LAYOUT
LEG      = dict(font=dict(color="#BAE6FD", size=11), bgcolor="rgba(0,0,0,0)")
LEG_H    = dict(font=dict(color="#BAE6FD", size=11), bgcolor="rgba(0,0,0,0)", orientation="h", y=1.08)
LEG_HL   = dict(font=dict(color="#BAE6FD", size=11), bgcolor="rgba(0,0,0,0)", orientation="h", y=1.06, x=0)

# Default axis style applied via update_xaxes / update_yaxes on every figure
AXIS_X = dict(
    tickfont=dict(color="#67E8F9", size=11),
    title_font=dict(color="#67E8F9"),
    gridcolor="rgba(6,182,212,0.12)",
    linecolor="rgba(6,182,212,0.20)",
    zerolinecolor="rgba(6,182,212,0.14)",
)
AXIS_Y = dict(
    tickfont=dict(color="#67E8F9", size=11),
    title_font=dict(color="#67E8F9"),
    gridcolor="rgba(6,182,212,0.12)",
    linecolor="rgba(6,182,212,0.20)",
    zerolinecolor="rgba(6,182,212,0.14)",
)

def apply_axes(fig, xkw=None, ykw=None):
    """Apply default Ocean Fresh axis styles, then any overrides."""
    x = {**AXIS_X, **(xkw or {})}
    y = {**AXIS_Y, **(ykw or {})}
    fig.update_xaxes(**x)
    fig.update_yaxes(**y)
    return fig

# ─────────────────────────────────────────────────────────────────────────────
# DATA LOADING & PREPROCESSING
# ─────────────────────────────────────────────────────────────────────────────

@st.cache_data
def load_data(path: str = "Nassau_Candy_Distributor.csv") -> pd.DataFrame:
    """Load Nassau Candy dataset. Auto-detects CSV or Excel by file magic bytes."""
    candidates = [
        path,
        "Nassau_Candy_Distributor.csv",
        "Nassau Candy Distributor.csv",
        "Nassau_Candy_Distributor.xlsx",
        "Nassau Candy Distributor.xlsx",
        "Nassau_Candy_Distributor.xls",
        "Nassau Candy Distributor.xls",
    ]
    found = next((p for p in candidates if os.path.exists(p)), None)
    if found is None:
        raise FileNotFoundError("Nassau Candy dataset not found.")

    # Detect actual file type by magic bytes — don't trust extension
    with open(found, "rb") as fcheck:
        magic = fcheck.read(4)
    is_real_excel = magic[:2] == b"PK" or (magic[0] == 0xD0 and magic[1] == 0xCF)

    if is_real_excel:
        engine = "openpyxl" if magic[:2] == b"PK" else "xlrd"
        df = pd.read_excel(found, engine=engine, parse_dates=["Order Date", "Ship Date"])
    else:
        df = pd.read_csv(found, dayfirst=True, parse_dates=["Order Date", "Ship Date"])

    for col in ["Sales", "Units", "Gross Profit", "Cost"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=["Sales", "Gross Profit", "Cost"])
    df = df[df["Sales"] > 0]

    df["Gross Margin (%)"]  = (df["Gross Profit"] / df["Sales"] * 100).round(2)
    df["Profit per Unit"]   = (df["Gross Profit"] / df["Units"].replace(0, np.nan)).round(2)
    df["Year"]              = df["Order Date"].dt.year.astype(str)
    df["Month"]             = df["Order Date"].dt.to_period("M").astype(str)
    df["Month Label"]       = df["Order Date"].dt.strftime("%b %y")
    df["Revenue Share (%)"] = (df["Sales"] / df["Sales"].sum() * 100).round(3)
    df["Profit Share (%)"]  = (df["Gross Profit"] / df["Gross Profit"].sum() * 100).round(3)
    return df


def product_summary(df):
    agg = df.groupby(["Product Name", "Division"], as_index=False).agg(
        Sales=("Sales", "sum"), Gross_Profit=("Gross Profit", "sum"),
        Cost=("Cost", "sum"), Units=("Units", "sum"), Orders=("Sales", "count"),
    )
    agg["Gross Margin (%)"]         = (agg["Gross_Profit"] / agg["Sales"] * 100).round(2)
    agg["Profit per Unit"]          = (agg["Gross_Profit"] / agg["Units"].replace(0, np.nan)).round(2)
    agg["Revenue Contribution (%)"] = (agg["Sales"] / agg["Sales"].sum() * 100).round(2)
    agg["Profit Contribution (%)"]  = (agg["Gross_Profit"] / agg["Gross_Profit"].sum() * 100).round(2)
    return (
        agg.rename(columns={"Gross_Profit": "Gross Profit"})
        .sort_values("Gross Profit", ascending=False)
        .reset_index(drop=True)
    )


def division_summary(df):
    agg = df.groupby("Division", as_index=False).agg(
        Sales=("Sales", "sum"), Gross_Profit=("Gross Profit", "sum"),
        Cost=("Cost", "sum"), Units=("Units", "sum"),
    )
    agg["Gross Margin (%)"]         = (agg["Gross_Profit"] / agg["Sales"] * 100).round(2)
    agg["Revenue Contribution (%)"] = (agg["Sales"] / agg["Sales"].sum() * 100).round(2)
    agg["Profit Contribution (%)"]  = (agg["Gross_Profit"] / agg["Gross_Profit"].sum() * 100).round(2)
    return (
        agg.rename(columns={"Gross_Profit": "Gross Profit"})
        .sort_values("Sales", ascending=False)
    )


def region_summary(df):
    agg = df.groupby("Region", as_index=False).agg(
        Sales=("Sales", "sum"), Gross_Profit=("Gross Profit", "sum"),
    )
    agg["Gross Margin (%)"] = (agg["Gross_Profit"] / agg["Sales"] * 100).round(2)
    return agg.rename(columns={"Gross_Profit": "Gross Profit"}).sort_values("Sales", ascending=False)


def monthly_trend(df):
    return (
        df.groupby(["Month", "Month Label"], as_index=False)
        .agg(Sales=("Sales", "sum"), Gross_Profit=("Gross Profit", "sum"))
        .sort_values("Month")
        .rename(columns={"Gross_Profit": "Gross Profit"})
    )

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────

def render_sidebar(df):
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-brand">
            <div class="brand-icon">🍬</div>
            <div class="brand-name">Nassau Candy</div>
            <div class="brand-sub">Profitability Analytics</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")

        st.markdown('<span class="sidebar-label">Division</span>', unsafe_allow_html=True)
        div_options  = ["All"] + sorted(df["Division"].unique().tolist())
        selected_div = st.selectbox("Division", div_options, label_visibility="collapsed")

        st.markdown('<span class="sidebar-label">Year</span>', unsafe_allow_html=True)
        year_options  = ["All"] + sorted(df["Year"].unique().tolist())
        selected_year = st.selectbox("Year", year_options, label_visibility="collapsed")

        st.markdown('<span class="sidebar-label">Minimum Gross Margin</span>', unsafe_allow_html=True)
        margin_min = st.slider("Margin", 0, 80, 0, step=5, label_visibility="collapsed")
        st.caption(f"Showing products with margin ≥ {margin_min}%")

        st.markdown('<span class="sidebar-label">Product Search</span>', unsafe_allow_html=True)
        product_search = st.text_input("Search", label_visibility="collapsed", placeholder="e.g. Wonka Bar")

        st.markdown("---")
        st.caption("Nassau Candy Distributor\n2024–2025 · Built with Streamlit")

    filtered = df.copy()
    if selected_div  != "All": filtered = filtered[filtered["Division"] == selected_div]
    if selected_year != "All": filtered = filtered[filtered["Year"] == selected_year]
    filtered = filtered[filtered["Gross Margin (%)"] >= margin_min]
    if product_search.strip():
        filtered = filtered[
            filtered["Product Name"].str.contains(product_search.strip(), case=False, na=False)
        ]

    return filtered, selected_div, selected_year, margin_min, product_search

# ─────────────────────────────────────────────────────────────────────────────
# KPI CARDS
# ─────────────────────────────────────────────────────────────────────────────

def render_kpis(df):
    total_sales    = df["Sales"].sum()
    total_profit   = df["Gross Profit"].sum()
    overall_margin = total_profit / total_sales * 100 if total_sales else 0
    total_orders   = len(df)
    total_units    = df["Units"].sum()

    k1, k2, k3, k4, k5 = st.columns(5)
    cards = [
        (k1, "💰 Total Sales",   f"${total_sales:,.0f}",   "kpi-emerald", "All filtered products"),
        (k2, "📈 Gross Profit",  f"${total_profit:,.0f}",  "kpi-gold",    "Sales minus cost"),
        (k3, "🎯 Gross Margin",  f"{overall_margin:.1f}%", "kpi-mint",    "Company average"),
        (k4, "📦 Total Orders",  f"{total_orders:,}",      "kpi-sage",    "Order line count"),
        (k5, "🏭 Total Units",   f"{total_units:,.0f}",    "kpi-amber",   "Units sold"),
    ]
    for col, label, val, css, sub in cards:
        with col:
            st.markdown(f"""
            <div class="kpi-card {css}">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{val}</div>
                <div class="kpi-sub">{sub}</div>
            </div>""", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 1 — PRODUCT PROFITABILITY OVERVIEW
# ─────────────────────────────────────────────────────────────────────────────

def tab_product_overview(df):
    prod = product_summary(df)

    # ── Leaderboard ──
    st.markdown('<div class="section-title">📊 Product Margin Leaderboard</div>', unsafe_allow_html=True)

    def margin_icon(m):
        if m >= 65:   return "🟢"
        elif m >= 45: return "🟡"
        else:         return "🔴"

    lb = prod[["Product Name", "Division", "Gross Margin (%)", "Gross Profit",
               "Sales", "Profit per Unit", "Profit Contribution (%)"]].copy()
    lb.insert(0, "Rank",   range(1, len(lb)+1))
    lb.insert(1, "Status", lb["Gross Margin (%)"].apply(margin_icon))
    lb["Gross Profit"]            = lb["Gross Profit"].map("${:,.0f}".format)
    lb["Sales"]                   = lb["Sales"].map("${:,.0f}".format)
    lb["Profit per Unit"]         = lb["Profit per Unit"].map("${:.2f}".format)
    lb["Gross Margin (%)"]        = lb["Gross Margin (%)"].map("{:.1f}%".format)
    lb["Profit Contribution (%)"] = lb["Profit Contribution (%)"].map("{:.1f}%".format)
    st.dataframe(lb, use_container_width=True, hide_index=True)
    st.caption("🟢 High margin (≥65%)  🟡 Mid margin (45–64%)  🔴 Margin risk (<45%)")
    st.markdown("---")

    col_l, col_r = st.columns(2)

    # ── Donut chart ──
    with col_l:
        st.markdown('<div class="section-title">🍩 Profit Contribution by Product</div>', unsafe_allow_html=True)
        fig_donut = px.pie(
            prod, names="Product Name", values="Gross Profit",
            hole=0.48, color="Product Name",
            color_discrete_sequence=FOREST_PALETTE,
        )
        fig_donut.update_traces(
            textposition="outside", textinfo="label+percent",
            textfont=dict(color="#BAE6FD", size=10),
            marker=dict(line=dict(color="rgba(7,17,31,0.85)", width=2)),
            hovertemplate="<b>%{label}</b><br>Profit: $%{value:,.0f}<br>Share: %{percent}<extra></extra>",
        )
        fig_donut.update_layout(
            **PLOTLY_LAYOUT, showlegend=False, height=390,
            title="Gross Profit Share per Product",
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    # ── Horizontal bar ──
    with col_r:
        st.markdown('<div class="section-title">📊 Revenue vs Profit by Product</div>', unsafe_allow_html=True)
        ps = prod.sort_values("Sales", ascending=True)
        fig_hbar = go.Figure()
        fig_hbar.add_trace(go.Bar(
            y=ps["Product Name"], x=ps["Sales"], name="Sales", orientation="h",
            marker=dict(color="rgba(34,211,238,0.40)", line=dict(color="#22D3EE", width=1)),
            hovertemplate="<b>%{y}</b><br>Sales: $%{x:,.0f}<extra></extra>",
        ))
        fig_hbar.add_trace(go.Bar(
            y=ps["Product Name"], x=ps["Gross Profit"], name="Gross Profit", orientation="h",
            marker=dict(color="rgba(34,211,238,0.75)", line=dict(color="#38BDF8", width=1)),
            hovertemplate="<b>%{y}</b><br>Profit: $%{x:,.0f}<extra></extra>",
        ))
        fig_hbar.update_layout(
            **PLOTLY_LAYOUT, barmode="overlay", height=390,
            title="Sales vs Gross Profit per Product",
            legend=LEG_HL,
        )
        apply_axes(fig_hbar,
                   xkw=dict(tickprefix="$", tickformat=",.0f"),
                   ykw=dict(tickfont=dict(color="#BAE6FD", size=10)))
        st.plotly_chart(fig_hbar, use_container_width=True)

    # ── Monthly trend ──
    st.markdown('<div class="section-title">📅 Monthly Revenue & Profit Trend</div>', unsafe_allow_html=True)
    trend = monthly_trend(df)
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=trend["Month Label"], y=trend["Sales"], name="Sales",
        fill="tozeroy", fillcolor="rgba(34,211,238,0.10)",
        line=dict(color="#22D3EE", width=2.5),
        hovertemplate="<b>%{x}</b><br>Sales: $%{y:,.0f}<extra></extra>",
    ))
    fig_trend.add_trace(go.Scatter(
        x=trend["Month Label"], y=trend["Gross Profit"], name="Gross Profit",
        fill="tozeroy", fillcolor="rgba(56,189,248,0.10)",
        line=dict(color="#38BDF8", width=2.5, dash="dot"),
        hovertemplate="<b>%{x}</b><br>Profit: $%{y:,.0f}<extra></extra>",
    ))
    fig_trend.update_layout(
        **PLOTLY_LAYOUT, height=310, title="Monthly Sales & Gross Profit",
        legend=LEG_H,
    )
    apply_axes(fig_trend,
               xkw=dict(tickangle=-45, tickfont=dict(color="#67E8F9", size=10)),
               ykw=dict(tickprefix="$", tickformat=",.0f"))
    st.plotly_chart(fig_trend, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 2 — DIVISION PERFORMANCE
# ─────────────────────────────────────────────────────────────────────────────

def tab_division_performance(df):
    div = division_summary(df)
    reg = region_summary(df)

    col_l, col_r = st.columns(2)

    # ── Division grouped bar ──
    with col_l:
        st.markdown('<div class="section-title">🏭 Revenue vs Profit by Division</div>', unsafe_allow_html=True)
        fig_div = go.Figure()
        fig_div.add_trace(go.Bar(
            name="Sales", x=div["Division"], y=div["Sales"],
            marker=dict(
                color=[DIV_COLORS.get(d, "#22D3EE") for d in div["Division"]],
                opacity=0.85,
                line=dict(color="rgba(255,255,255,0.15)", width=1),
            ),
            hovertemplate="<b>%{x}</b><br>Sales: $%{y:,.0f}<extra></extra>",
        ))
        fig_div.add_trace(go.Bar(
            name="Gross Profit", x=div["Division"], y=div["Gross Profit"],
            marker=dict(
                color=[
                    "rgba(34,211,238,0.40)" if d == "Chocolate"
                    else "rgba(56,189,248,0.40)" if d == "Other"
                    else "rgba(6,182,212,0.38)"
                    for d in div["Division"]
                ],
                line=dict(color="rgba(255,255,255,0.12)", width=1),
            ),
            hovertemplate="<b>%{x}</b><br>Gross Profit: $%{y:,.0f}<extra></extra>",
        ))
        fig_div.update_layout(
            **PLOTLY_LAYOUT, barmode="group", height=340,
            title="Division Revenue vs Gross Profit",
            legend=LEG_H,
        )
        apply_axes(fig_div,
                   xkw=dict(tickfont=dict(color="#BAE6FD")),
                   ykw=dict(tickprefix="$", tickformat=",.0f"))
        st.plotly_chart(fig_div, use_container_width=True)

    # ── Margin horizontal bar ──
    with col_r:
        st.markdown('<div class="section-title">📐 Gross Margin by Division</div>', unsafe_allow_html=True)
        fig_margin = go.Figure(go.Bar(
            y=div["Division"], x=div["Gross Margin (%)"],
            orientation="h",
            text=div["Gross Margin (%)"].map("{:.1f}%".format),
            textposition="outside",
            textfont=dict(color="#BAE6FD"),
            marker=dict(
                color=[DIV_COLORS.get(d, "#22D3EE") for d in div["Division"]],
                line=dict(color="rgba(255,255,255,0.15)", width=1),
            ),
            hovertemplate="<b>%{y}</b><br>Margin: %{x:.1f}%<extra></extra>",
        ))
        fig_margin.update_layout(
            **PLOTLY_LAYOUT, height=340, title="Gross Margin (%) by Division",
        )
        apply_axes(fig_margin,
                   xkw=dict(range=[0, 100], ticksuffix="%"),
                   ykw=dict(tickfont=dict(color="#BAE6FD")))
        st.plotly_chart(fig_margin, use_container_width=True)

    # ── Summary table ──
    st.markdown('<div class="section-title">📋 Division Summary Table</div>', unsafe_allow_html=True)
    dd = div.copy()
    dd["Sales"]                    = dd["Sales"].map("${:,.0f}".format)
    dd["Gross Profit"]             = dd["Gross Profit"].map("${:,.0f}".format)
    dd["Cost"]                     = dd["Cost"].map("${:,.0f}".format)
    dd["Gross Margin (%)"]         = dd["Gross Margin (%)"].map("{:.1f}%".format)
    dd["Revenue Contribution (%)"] = dd["Revenue Contribution (%)"].map("{:.1f}%".format)
    dd["Profit Contribution (%)"]  = dd["Profit Contribution (%)"].map("{:.1f}%".format)
    st.dataframe(
        dd[["Division", "Sales", "Gross Profit", "Cost", "Units",
            "Gross Margin (%)", "Revenue Contribution (%)", "Profit Contribution (%)"]],
        use_container_width=True, hide_index=True,
    )

    # ── Insights ──
    st.markdown('<div class="section-title">💡 Division Insights</div>', unsafe_allow_html=True)
    for txt in [
        "🍫 <b>Chocolate</b> generates ~93% of all revenue and ~95% of gross profit — the undisputed core of Nassau Candy's business.",
        "⚠️ <b>Other division</b>'s margin is heavily dragged by Kazookles (7.7% margin) — a structural risk needing repricing or discontinuation review.",
        "🌱 <b>Sugar</b> products achieve strong margins (up to 80%) but represent minimal revenue — a significant untapped scaling opportunity.",
        "🏆 <b>Everlasting Gobstopper</b> (80%) and <b>Hair Toffee</b> (78%) are high-margin Sugar products with enormous growth potential.",
    ]:
        st.markdown(f'<div class="insight-box">{txt}</div>', unsafe_allow_html=True)

    # ── Region charts ──
    st.markdown('<div class="section-title">🗺️ Regional Performance</div>', unsafe_allow_html=True)
    col_a, col_b = st.columns(2)

    with col_a:
        fig_reg = go.Figure()
        fig_reg.add_trace(go.Bar(
            name="Sales", x=reg["Region"], y=reg["Sales"],
            marker=dict(color=[REGION_COLORS.get(r, "#22D3EE") for r in reg["Region"]], opacity=0.85),
            hovertemplate="<b>%{x}</b><br>Sales: $%{y:,.0f}<extra></extra>",
        ))
        fig_reg.add_trace(go.Bar(
            name="Gross Profit", x=reg["Region"], y=reg["Gross Profit"],
            marker=dict(color=[REGION_COLORS.get(r, "#22D3EE") for r in reg["Region"]], opacity=0.42),
            hovertemplate="<b>%{x}</b><br>Profit: $%{y:,.0f}<extra></extra>",
        ))
        fig_reg.update_layout(
            **PLOTLY_LAYOUT, barmode="overlay", height=310,
            title="Sales & Profit by Region",
            legend=LEG_H,
        )
        apply_axes(fig_reg,
                   xkw=dict(tickfont=dict(color="#BAE6FD")),
                   ykw=dict(tickprefix="$", tickformat=",.0f"))
        st.plotly_chart(fig_reg, use_container_width=True)

    with col_b:
        fig_pie = px.pie(
            reg, names="Region", values="Gross Profit",
            hole=0.42, color="Region",
            color_discrete_map=REGION_COLORS,
            title="Profit Distribution by Region",
        )
        fig_pie.update_traces(
            textposition="outside", textinfo="label+percent",
            textfont=dict(color="#BAE6FD", size=10),
            marker=dict(line=dict(color="rgba(7,17,31,0.85)", width=2)),
        )
        fig_pie.update_layout(**PLOTLY_LAYOUT, showlegend=False, height=310)
        st.plotly_chart(fig_pie, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 3 — COST vs MARGIN DIAGNOSTICS
# ─────────────────────────────────────────────────────────────────────────────

def tab_cost_diagnostics(df):
    prod = product_summary(df)

    # ── Scatter ──
    st.markdown('<div class="section-title">🔬 Cost vs Sales — Margin Risk Scatter</div>', unsafe_allow_html=True)
    fig_scat = px.scatter(
        prod, x="Cost", y="Sales", size="Gross Profit", color="Division",
        hover_name="Product Name", color_discrete_map=DIV_COLORS, size_max=65,
        labels={"Cost": "Total Cost ($)", "Sales": "Total Sales ($)"},
        title="Cost vs Sales (Bubble size = Gross Profit)",
        hover_data={"Gross Margin (%)": ":.1f", "Profit per Unit": ":.2f", "Gross Profit": ":,.0f"},
    )
    max_cost = prod["Cost"].max()
    fig_scat.add_trace(go.Scatter(
        x=[0, max_cost], y=[0, max_cost * 2], mode="lines",
        name="50% Margin line",
        line=dict(color="#38BDF8", dash="dash", width=2),
        hoverinfo="skip",
    ))
    fig_scat.update_layout(
        **PLOTLY_LAYOUT, height=430,
        legend=LEG,
    )
    apply_axes(fig_scat, xkw=dict(tickprefix="$", tickformat=",.0f"),
               ykw=dict(tickprefix="$", tickformat=",.0f"))
    st.plotly_chart(fig_scat, use_container_width=True)
    st.caption("📍 Products below the dashed line have below-average margin efficiency.")
    st.markdown("---")

    # ── Risk table ──
    st.markdown('<div class="section-title">🚨 Margin Risk Flags — Product Diagnostics</div>', unsafe_allow_html=True)

    def risk_flag(m):
        if m < 45:   return "🔴 REPRICE / REVIEW"
        elif m < 65: return "🟡 MONITOR"
        else:        return "🟢 HEALTHY"

    def recommendation(row):
        m = row["Gross Margin (%)"]
        if m < 20:   return "Discontinuation candidate — cost exceeds value"
        elif m < 45: return "Pricing inefficiency — renegotiate sourcing or reprice"
        elif m < 65: return "Acceptable — monitor closely for margin erosion"
        else:        return "Performing well — maintain and grow"

    risk_df = prod[["Product Name", "Division", "Gross Margin (%)", "Cost", "Sales", "Gross Profit"]].copy()
    risk_df["Risk Status"]    = risk_df["Gross Margin (%)"].apply(risk_flag)
    risk_df["Recommendation"] = risk_df.apply(recommendation, axis=1)
    risk_df = risk_df.sort_values("Gross Margin (%)")
    risk_df["Gross Margin (%)"] = risk_df["Gross Margin (%)"].map("{:.1f}%".format)
    risk_df["Cost"]             = risk_df["Cost"].map("${:,.0f}".format)
    risk_df["Sales"]            = risk_df["Sales"].map("${:,.0f}".format)
    risk_df["Gross Profit"]     = risk_df["Gross Profit"].map("${:,.0f}".format)
    st.dataframe(risk_df, use_container_width=True, hide_index=True)
    st.markdown("---")

    # ── Stacked cost structure ──
    st.markdown('<div class="section-title">📊 Cost Structure by Product</div>', unsafe_allow_html=True)
    pcs = product_summary(df).sort_values("Sales", ascending=False)
    fig_stack = go.Figure()
    fig_stack.add_trace(go.Bar(
        name="Cost", x=pcs["Product Name"], y=pcs["Cost"],
        marker=dict(color="rgba(56,189,248,0.60)", line=dict(color="#38BDF8", width=1)),
        hovertemplate="<b>%{x}</b><br>Cost: $%{y:,.0f}<extra></extra>",
    ))
    fig_stack.add_trace(go.Bar(
        name="Gross Profit", x=pcs["Product Name"], y=pcs["Gross Profit"],
        marker=dict(color="rgba(34,211,238,0.70)", line=dict(color="#22D3EE", width=1)),
        hovertemplate="<b>%{x}</b><br>Profit: $%{y:,.0f}<extra></extra>",
    ))
    fig_stack.update_layout(
        **PLOTLY_LAYOUT, barmode="stack", height=370,
        title="Total Cost vs Gross Profit by Product",
        legend=LEG_H,
    )
    apply_axes(fig_stack,
               xkw=dict(tickangle=-38, tickfont=dict(color="#BAE6FD", size=10)),
               ykw=dict(tickprefix="$", tickformat=",.0f"))
    st.plotly_chart(fig_stack, use_container_width=True)

    # ── Efficiency quadrant scatter ──
    st.markdown('<div class="section-title">💡 Pricing Efficiency — Margin vs Revenue Volume</div>', unsafe_allow_html=True)
    ppe = product_summary(df)
    fig_quad = px.scatter(
        ppe, x="Sales", y="Gross Margin (%)", color="Division", size="Gross Profit",
        hover_name="Product Name", color_discrete_map=DIV_COLORS, size_max=52,
        labels={"Sales": "Total Revenue ($)", "Gross Margin (%)": "Gross Margin (%)"},
        title="High-Sales / Low-Margin Quadrant Analysis",
        hover_data={"Profit per Unit": ":.2f"},
    )
    med_sales  = ppe["Sales"].median()
    med_margin = ppe["Gross Margin (%)"].median()
    fig_quad.add_hline(y=med_margin, line_dash="dot", line_color="#38BDF8",
                       annotation_text=f"Median {med_margin:.1f}%",
                       annotation_font_color="#38BDF8")
    fig_quad.add_vline(x=med_sales, line_dash="dot", line_color="#38BDF8",
                       annotation_text="Median sales",
                       annotation_font_color="#38BDF8")
    fig_quad.update_layout(
        **PLOTLY_LAYOUT, height=390,
        legend=LEG,
    )
    apply_axes(fig_quad,
               xkw=dict(tickprefix="$", tickformat=",.0f"),
               ykw=dict(ticksuffix="%"))
    st.plotly_chart(fig_quad, use_container_width=True)
    st.caption("📌 Top-right = high revenue & high margin (ideal)  ·  Bottom-right = repricing needed")

# ─────────────────────────────────────────────────────────────────────────────
# TAB 4 — PARETO / PROFIT CONCENTRATION
# ─────────────────────────────────────────────────────────────────────────────

def tab_pareto_analysis(df):
    prod = product_summary(df)

    def build_pareto(data, value_col, label, bar_color, line_color="#38BDF8"):
        data = data.sort_values(value_col, ascending=False).reset_index(drop=True)
        total = data[value_col].sum()
        data["Cumulative %"] = (data[value_col].cumsum() / total * 100).round(2)
        idx80 = int((data["Cumulative %"] < 80).sum())

        colors = [bar_color if i <= idx80 else "rgba(20,50,100,0.30)" for i in range(len(data))]

        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Bar(
            x=data["Product Name"], y=data[value_col],
            name=label, marker_color=colors,
            marker_line=dict(color="rgba(255,255,255,0.12)", width=1),
            hovertemplate=f"<b>%{{x}}</b><br>{label}: $%{{y:,.0f}}<extra></extra>",
        ), secondary_y=False)
        fig.add_trace(go.Scatter(
            x=data["Product Name"], y=data["Cumulative %"],
            name="Cumulative %", mode="lines+markers",
            line=dict(color=line_color, width=2.5),
            marker=dict(size=6, color=line_color,
                        line=dict(color="rgba(255,255,255,0.4)", width=1)),
            hovertemplate="%{x}<br>Cumulative: %{y:.1f}%<extra></extra>",
        ), secondary_y=True)
        fig.add_hline(y=80, line_dash="dash", line_color="#38BDF8",
                      secondary_y=True, opacity=0.7,
                      annotation_text="80% line", annotation_font_color="#38BDF8")
        fig.update_layout(
            **PLOTLY_LAYOUT, height=390,
            title=f"{label} Pareto — {idx80+1} products drive 80%+",
            legend=LEG_H,
        )
        fig.update_xaxes(tickangle=-38, tickfont=dict(color="#BAE6FD", size=10))
        fig.update_yaxes(tickprefix="$", tickformat=",.0f",
                         tickfont=dict(color="#67E8F9"),
                         gridcolor="rgba(6,182,212,0.12)", secondary_y=False)
        fig.update_yaxes(ticksuffix="%", range=[0, 105],
                         tickfont=dict(color="#38BDF8"),
                         gridcolor="rgba(0,0,0,0)", secondary_y=True)
        return fig, idx80

    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown('<div class="section-title">📈 Revenue Pareto (80% Threshold)</div>', unsafe_allow_html=True)
        fig_rev, idx_rev = build_pareto(prod, "Sales", "Revenue", "#22D3EE")
        st.plotly_chart(fig_rev, use_container_width=True)
        st.markdown(f'<div class="insight-box">📌 <b>{idx_rev+1} products</b> drive 80%+ of total revenue.</div>', unsafe_allow_html=True)

    with col_r:
        st.markdown('<div class="section-title">💰 Profit Pareto (80% Threshold)</div>', unsafe_allow_html=True)
        fig_prof, idx_prof = build_pareto(prod, "Gross Profit", "Profit", "#38BDF8", "#06B6D4")
        st.plotly_chart(fig_prof, use_container_width=True)
        st.markdown(f'<div class="insight-box">📌 <b>{idx_prof+1} products</b> drive 80%+ of gross profit.</div>', unsafe_allow_html=True)

    # ── Concentration insights ──
    st.markdown('<div class="section-title">⚠️ Profit Concentration Insights</div>', unsafe_allow_html=True)
    top5_share  = prod.nlargest(5, "Gross Profit")["Profit Contribution (%)"].sum()
    choc_share  = prod[prod["Division"] == "Chocolate"]["Profit Contribution (%)"].sum()
    for txt in [
        f"🍫 <b>Revenue concentration:</b> Chocolate contributes <b>{choc_share:.1f}%</b> of gross profit — extreme single-division dependency.",
        "🏭 <b>Factory risk:</b> Disruption at Wicked Choccy's or Lot's O' Nuts creates catastrophic margin risk.",
        f"📦 <b>Portfolio gap:</b> Top 5 products = <b>{top5_share:.1f}%</b> of profit. Remaining products are significantly underdeveloped.",
        "🌱 <b>Growth opportunity:</b> Everlasting Gobstopper (80%) and Hair Toffee (78%) — high-efficiency latent scaling potential.",
        "⚡ <b>Recommendation:</b> Scale Sugar division and reprice/discontinue Kazookles (7.7% margin).",
    ]:
        st.markdown(f'<div class="insight-box">{txt}</div>', unsafe_allow_html=True)

    # ── Efficiency matrix ──
    st.markdown('<div class="section-title">🎯 Efficiency Matrix — Margin % vs Profit per Unit</div>', unsafe_allow_html=True)
    fig_mat = px.scatter(
        prod, x="Gross Margin (%)", y="Profit per Unit",
        size="Sales", color="Division",
        hover_name="Product Name", color_discrete_map=DIV_COLORS, size_max=58,
        labels={"Gross Margin (%)": "Gross Margin (%)", "Profit per Unit": "Profit per Unit ($)"},
        title="Efficiency Matrix: Margin vs Profit per Unit (bubble = revenue volume)",
        hover_data={"Sales": "$,.0f", "Gross Profit": "$,.0f"},
    )
    fig_mat.add_vrect(x0=65, x1=100,
                      fillcolor="rgba(6,182,212,0.08)", layer="below", line_width=0)
    fig_mat.add_annotation(
        x=82, y=prod["Profit per Unit"].max() * 0.93,
        text="⭐ Ideal Zone", showarrow=False,
        font=dict(color="#06B6D4", size=13, family="Plus Jakarta Sans"),
    )
    fig_mat.update_layout(
        **PLOTLY_LAYOUT, height=430,
        legend=LEG,
    )
    apply_axes(fig_mat,
               xkw=dict(ticksuffix="%"),
               ykw=dict(tickprefix="$"))
    st.plotly_chart(fig_mat, use_container_width=True)
    st.caption("⭐ Top-right = high margin AND high profit per unit → priority growth products")

    # ── Treemap ──
    st.markdown('<div class="section-title">🗂️ Profit Contribution Treemap</div>', unsafe_allow_html=True)
    ptm = product_summary(df)
    ptm["Short Name"] = (
        ptm["Product Name"]
        .str.replace("Wonka Bar - ", "WB ")
        .str.replace("Wonka Bar -", "WB ")
    )
    fig_tree = px.treemap(
        ptm, path=["Division", "Short Name"], values="Gross Profit",
        color="Gross Margin (%)",
        color_continuous_scale=["#38BDF8", "#22D3EE", "#06B6D4", "#67E8F9"],
        hover_data={"Sales": "$,.0f", "Gross Profit": "$,.0f", "Gross Margin (%)": ":.1f"},
        title="Gross Profit Treemap — sized by profit, coloured by margin",
    )
    fig_tree.update_layout(
        **PLOTLY_LAYOUT, height=420,
        coloraxis_colorbar_title="Margin %",
        coloraxis_colorbar=dict(
            tickfont=dict(color="#BAE6FD"),
            title_font=dict(color="#BAE6FD"),
        ),
    )
    fig_tree.update_traces(
        hovertemplate="<b>%{label}</b><br>Profit: $%{value:,.0f}<br>Margin: %{color:.1f}%<extra></extra>",
        marker=dict(line=dict(color="rgba(7,17,31,0.65)", width=2)),
    )
    st.plotly_chart(fig_tree, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 5 — YEAR-OVER-YEAR COMPARISON
# ─────────────────────────────────────────────────────────────────────────────

def tab_yoy_comparison(df_raw):
    """Full 2024 vs 2025 Year-over-Year performance comparison."""

    years = sorted(df_raw["Year"].unique().tolist())
    if len(years) < 2:
        st.warning("⚠️ Only one year found in the dataset. YoY comparison requires data from at least two years.")
        return

    yr_a, yr_b = years[0], years[1]   # e.g. "2024", "2025"
    df_a = df_raw[df_raw["Year"] == yr_a]
    df_b = df_raw[df_raw["Year"] == yr_b]

    # ── Helper: safe pct change ──
    def pct_chg(old, new):
        if old == 0:
            return 0.0
        return ((new - old) / abs(old)) * 100

    def arrow(val):
        return "▲" if val >= 0 else "▼"

    def arrow_color(val):
        return "#22D3EE" if val >= 0 else "#F87171"

    # ── Top-level metrics ──
    metrics = {
        "Sales":         (df_a["Sales"].sum(),        df_b["Sales"].sum()),
        "Gross Profit":  (df_a["Gross Profit"].sum(), df_b["Gross Profit"].sum()),
        "Gross Margin":  (
            df_a["Gross Profit"].sum() / df_a["Sales"].sum() * 100,
            df_b["Gross Profit"].sum() / df_b["Sales"].sum() * 100,
        ),
        "Orders":        (len(df_a),                  len(df_b)),
        "Units":         (df_a["Units"].sum(),         df_b["Units"].sum()),
    }

    # ── KPI delta cards ──
    st.markdown('<div class="section-title">📊 Key Metrics — 2024 vs 2025</div>', unsafe_allow_html=True)

    cols = st.columns(5)
    fmts = {
        "Sales":        lambda v: f"${v:,.0f}",
        "Gross Profit": lambda v: f"${v:,.0f}",
        "Gross Margin": lambda v: f"{v:.1f}%",
        "Orders":       lambda v: f"{v:,}",
        "Units":        lambda v: f"{v:,.0f}",
    }
    icons = {"Sales": "💰", "Gross Profit": "📈", "Gross Margin": "🎯", "Orders": "📦", "Units": "🏭"}

    for col, (label, (val_a, val_b)) in zip(cols, metrics.items()):
        chg = pct_chg(val_a, val_b)
        clr = arrow_color(chg)
        with col:
            st.markdown(f"""
            <div class="kpi-card kpi-emerald" style="text-align:left; padding:1rem;">
                <div class="kpi-label">{icons[label]} {label}</div>
                <div style="display:flex; gap:8px; align-items:baseline; flex-wrap:wrap;">
                    <div style="font-size:0.85rem; color:#67E8F9;">{yr_a}: <b>{fmts[label](val_a)}</b></div>
                </div>
                <div style="display:flex; gap:8px; align-items:baseline; flex-wrap:wrap; margin-top:2px;">
                    <div style="font-size:0.85rem; color:#BAE6FD;">{yr_b}: <b>{fmts[label](val_b)}</b></div>
                </div>
                <div style="font-size:1.1rem; font-weight:700; color:{clr}; margin-top:6px;">
                    {arrow(chg)} {abs(chg):.1f}%
                </div>
                <div class="kpi-sub">vs previous year</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")

    # ── Monthly Revenue Trend — 2024 vs 2025 ──
    st.markdown('<div class="section-title">📅 Monthly Revenue Trend — 2024 vs 2025</div>', unsafe_allow_html=True)

    def monthly_by_year(df):
        return (
            df.groupby(["Month", "Month Label"], as_index=False)
            .agg(Sales=("Sales", "sum"), Gross_Profit=("Gross Profit", "sum"))
            .sort_values("Month")
            .rename(columns={"Gross_Profit": "Gross Profit"})
        )

    tr_a = monthly_by_year(df_a)
    tr_b = monthly_by_year(df_b)

    # Align on month number for x-axis
    tr_a["MonthNum"] = pd.to_datetime(tr_a["Month"]).dt.month
    tr_b["MonthNum"] = pd.to_datetime(tr_b["Month"]).dt.month
    month_names = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=tr_a["MonthNum"], y=tr_a["Sales"], name=f"{yr_a} Sales",
        mode="lines+markers",
        line=dict(color="#67E8F9", width=2.5, dash="dot"),
        marker=dict(size=7, color="#67E8F9"),
        fill="tozeroy", fillcolor="rgba(103,232,249,0.07)",
        hovertemplate="<b>%{x}</b><br>Sales: $%{y:,.0f}<extra></extra>",
    ))
    fig_trend.add_trace(go.Scatter(
        x=tr_b["MonthNum"], y=tr_b["Sales"], name=f"{yr_b} Sales",
        mode="lines+markers",
        line=dict(color="#22D3EE", width=2.5),
        marker=dict(size=7, color="#22D3EE"),
        fill="tozeroy", fillcolor="rgba(34,211,238,0.10)",
        hovertemplate="<b>%{x}</b><br>Sales: $%{y:,.0f}<extra></extra>",
    ))
    fig_trend.add_trace(go.Scatter(
        x=tr_a["MonthNum"], y=tr_a["Gross Profit"], name=f"{yr_a} Profit",
        mode="lines+markers",
        line=dict(color="#38BDF8", width=2, dash="dash"),
        marker=dict(size=5, color="#38BDF8"),
        hovertemplate="<b>%{x}</b><br>Profit: $%{y:,.0f}<extra></extra>",
    ))
    fig_trend.add_trace(go.Scatter(
        x=tr_b["MonthNum"], y=tr_b["Gross Profit"], name=f"{yr_b} Profit",
        mode="lines+markers",
        line=dict(color="#06B6D4", width=2),
        marker=dict(size=5, color="#06B6D4"),
        hovertemplate="<b>%{x}</b><br>Profit: $%{y:,.0f}<extra></extra>",
    ))
    fig_trend.update_layout(
        **PLOTLY_LAYOUT, height=340,
        title=f"Monthly Sales & Profit — {yr_a} vs {yr_b}",
        legend=LEG_H,
    )
    apply_axes(fig_trend,
               xkw=dict(tickvals=list(range(1,13)), ticktext=month_names, tickfont=dict(color="#BAE6FD", size=10)),
               ykw=dict(tickprefix="$", tickformat=",.0f"))
    st.plotly_chart(fig_trend, use_container_width=True)

    st.markdown("---")

    # ── Division YoY grouped bar ──
    st.markdown('<div class="section-title">🏭 Division Performance — 2024 vs 2025</div>', unsafe_allow_html=True)

    div_a = division_summary(df_a).rename(columns={"Sales": f"Sales_{yr_a}", "Gross Profit": f"Profit_{yr_a}", "Gross Margin (%)": f"Margin_{yr_a}"})
    div_b = division_summary(df_b).rename(columns={"Sales": f"Sales_{yr_b}", "Gross Profit": f"Profit_{yr_b}", "Gross Margin (%)": f"Margin_{yr_b}"})
    div_yoy = div_a[["Division", f"Sales_{yr_a}", f"Profit_{yr_a}", f"Margin_{yr_a}"]].merge(
        div_b[["Division", f"Sales_{yr_b}", f"Profit_{yr_b}", f"Margin_{yr_b}"]], on="Division", how="outer"
    ).fillna(0)
    div_yoy["Sales Growth %"]  = div_yoy.apply(lambda r: pct_chg(r[f"Sales_{yr_a}"],  r[f"Sales_{yr_b}"]),  axis=1).round(1)
    div_yoy["Margin Shift"]    = (div_yoy[f"Margin_{yr_b}"] - div_yoy[f"Margin_{yr_a}"]).round(2)

    col_l, col_r = st.columns(2)
    with col_l:
        fig_div = go.Figure()
        fig_div.add_trace(go.Bar(
            name=f"{yr_a} Sales", x=div_yoy["Division"], y=div_yoy[f"Sales_{yr_a}"],
            marker=dict(color="rgba(103,232,249,0.55)", line=dict(color="#67E8F9", width=1)),
            hovertemplate="<b>%{x}</b><br>Sales: $%{y:,.0f}<extra></extra>",
        ))
        fig_div.add_trace(go.Bar(
            name=f"{yr_b} Sales", x=div_yoy["Division"], y=div_yoy[f"Sales_{yr_b}"],
            marker=dict(color="rgba(34,211,238,0.85)", line=dict(color="#22D3EE", width=1)),
            hovertemplate="<b>%{x}</b><br>Sales: $%{y:,.0f}<extra></extra>",
        ))
        fig_div.update_layout(
            **PLOTLY_LAYOUT, barmode="group", height=330,
            title="Revenue by Division — Year Comparison",
            legend=LEG_H,
        )
        apply_axes(fig_div,
                   xkw=dict(tickfont=dict(color="#BAE6FD")),
                   ykw=dict(tickprefix="$", tickformat=",.0f"))
        st.plotly_chart(fig_div, use_container_width=True)

    with col_r:
        margin_colors = ["#22D3EE" if v >= 0 else "#F87171" for v in div_yoy["Margin Shift"]]
        fig_margin = go.Figure(go.Bar(
            x=div_yoy["Division"], y=div_yoy["Margin Shift"],
            marker=dict(color=margin_colors, line=dict(color="rgba(255,255,255,0.15)", width=1)),
            text=div_yoy["Margin Shift"].apply(lambda v: f"{'+' if v>=0 else ''}{v:.2f}%"),
            textposition="outside",
            textfont=dict(color="#BAE6FD"),
            hovertemplate="<b>%{x}</b><br>Margin shift: %{y:+.2f}%<extra></extra>",
        ))
        fig_margin.add_hline(y=0, line_color="rgba(255,255,255,0.25)", line_width=1)
        fig_margin.update_layout(
            **PLOTLY_LAYOUT, height=330,
            title=f"Gross Margin Shift by Division ({yr_a} → {yr_b})",
        )
        apply_axes(fig_margin,
                   xkw=dict(tickfont=dict(color="#BAE6FD")),
                   ykw=dict(ticksuffix="%"))
        st.plotly_chart(fig_margin, use_container_width=True)

    st.markdown("---")

    # ── Profit by division donut comparison ──
    st.markdown('<div class="section-title">🍩 Profit Mix — 2024 vs 2025</div>', unsafe_allow_html=True)
    col_d1, col_d2 = st.columns(2)
    for col, yr, dff in [(col_d1, yr_a, df_a), (col_d2, yr_b, df_b)]:
        div_s = division_summary(dff)
        fig_pie = px.pie(
            div_s, names="Division", values="Gross Profit",
            hole=0.45, color="Division",
            color_discrete_map=DIV_COLORS,
            title=f"{yr} — Profit by Division",
        )
        fig_pie.update_traces(
            textposition="outside", textinfo="label+percent",
            textfont=dict(color="#BAE6FD", size=10),
            marker=dict(line=dict(color="rgba(7,17,31,0.8)", width=2)),
        )
        fig_pie.update_layout(**PLOTLY_LAYOUT, showlegend=False, height=300)
        with col:
            st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("---")

    # ── Product-level YoY table ──
    st.markdown('<div class="section-title">📋 Product-Level YoY Performance Table</div>', unsafe_allow_html=True)

    prod_a = product_summary(df_a)[["Product Name", "Division", "Sales", "Gross Profit", "Gross Margin (%)"]].rename(
        columns={"Sales": f"Sales {yr_a}", "Gross Profit": f"Profit {yr_a}", "Gross Margin (%)": f"Margin {yr_a} (%)"}
    )
    prod_b = product_summary(df_b)[["Product Name", "Division", "Sales", "Gross Profit", "Gross Margin (%)"]].rename(
        columns={"Sales": f"Sales {yr_b}", "Gross Profit": f"Profit {yr_b}", "Gross Margin (%)": f"Margin {yr_b} (%)"}
    )
    prod_yoy = prod_a.merge(prod_b, on=["Product Name", "Division"], how="outer").fillna(0)
    prod_yoy["Sales Growth %"]  = prod_yoy.apply(lambda r: pct_chg(r[f"Sales {yr_a}"], r[f"Sales {yr_b}"]), axis=1).round(1)
    prod_yoy["Margin Shift"]    = (prod_yoy[f"Margin {yr_b} (%)"] - prod_yoy[f"Margin {yr_a} (%)"]).round(2)
    prod_yoy["Trend"]           = prod_yoy["Sales Growth %"].apply(lambda v: "📈 Growing" if v > 5 else ("📉 Declining" if v < -5 else "➡️ Stable"))

    display_yoy = prod_yoy.copy()
    for c in [f"Sales {yr_a}", f"Profit {yr_a}", f"Sales {yr_b}", f"Profit {yr_b}"]:
        display_yoy[c] = display_yoy[c].map("${:,.0f}".format)
    for c in [f"Margin {yr_a} (%)", f"Margin {yr_b} (%)"]:
        display_yoy[c] = display_yoy[c].map("{:.1f}%".format)
    display_yoy["Sales Growth %"] = display_yoy["Sales Growth %"].map(lambda v: f"{'+' if v>=0 else ''}{v:.1f}%")
    display_yoy["Margin Shift"]   = display_yoy["Margin Shift"].map(lambda v: f"{'+' if v>=0 else ''}{v:.2f}%")

    st.dataframe(
        display_yoy[[
            "Product Name", "Division",
            f"Sales {yr_a}", f"Sales {yr_b}", "Sales Growth %",
            f"Margin {yr_a} (%)", f"Margin {yr_b} (%)", "Margin Shift",
            "Trend"
        ]],
        use_container_width=True, hide_index=True,
    )
    st.caption("📈 Growing = Sales growth > 5%  ·  📉 Declining = Sales decline > 5%  ·  ➡️ Stable = within ±5%")
    st.markdown("---")

    # ── Monthly Margin trend comparison ──
    st.markdown('<div class="section-title">🎯 Monthly Gross Margin % — 2024 vs 2025</div>', unsafe_allow_html=True)

    def monthly_margin(df):
        m = (df.groupby(["Month"], as_index=False)
               .agg(Sales=("Sales","sum"), GP=("Gross Profit","sum"))
               .sort_values("Month"))
        m["Margin (%)"] = (m["GP"] / m["Sales"] * 100).round(2)
        m["MonthNum"]   = pd.to_datetime(m["Month"]).dt.month
        return m

    mm_a = monthly_margin(df_a)
    mm_b = monthly_margin(df_b)

    fig_mgn = go.Figure()
    fig_mgn.add_trace(go.Scatter(
        x=mm_a["MonthNum"], y=mm_a["Margin (%)"], name=f"{yr_a} Margin",
        mode="lines+markers",
        line=dict(color="#67E8F9", width=2.5, dash="dot"),
        marker=dict(size=7, color="#67E8F9"),
        hovertemplate="<b>%{x}</b><br>Margin: %{y:.1f}%<extra></extra>",
    ))
    fig_mgn.add_trace(go.Scatter(
        x=mm_b["MonthNum"], y=mm_b["Margin (%)"], name=f"{yr_b} Margin",
        mode="lines+markers",
        line=dict(color="#22D3EE", width=2.5),
        marker=dict(size=7, color="#22D3EE"),
        fill="tonexty", fillcolor="rgba(34,211,238,0.06)",
        hovertemplate="<b>%{x}</b><br>Margin: %{y:.1f}%<extra></extra>",
    ))
    fig_mgn.update_layout(
        **PLOTLY_LAYOUT, height=310,
        title=f"Gross Margin % by Month — {yr_a} vs {yr_b}",
        legend=LEG_H,
    )
    apply_axes(fig_mgn,
               xkw=dict(tickvals=list(range(1,13)), ticktext=month_names, tickfont=dict(color="#BAE6FD", size=10)),
               ykw=dict(ticksuffix="%", tickformat=".1f"))
    st.plotly_chart(fig_mgn, use_container_width=True)
    st.markdown("---")

    # ── YoY Insights ──
    st.markdown('<div class="section-title">💡 Year-over-Year Insights</div>', unsafe_allow_html=True)

    sales_a,  sales_b  = metrics["Sales"]
    profit_a, profit_b = metrics["Gross Profit"]
    margin_a, margin_b = metrics["Gross Margin"]
    sales_g  = pct_chg(sales_a,  sales_b)
    profit_g = pct_chg(profit_a, profit_b)
    margin_g = margin_b - margin_a

    best_product = prod_yoy.sort_values("Sales Growth %", ascending=False).iloc[0]
    worst_product = prod_yoy.sort_values("Sales Growth %").iloc[0]

    insights = [
        f"📈 <b>Revenue growth:</b> Total sales moved from <b>${sales_a:,.0f}</b> ({yr_a}) to <b>${sales_b:,.0f}</b> ({yr_b}) — a <b>{sales_g:+.1f}%</b> change year-over-year.",
        f"💰 <b>Profit trajectory:</b> Gross profit shifted from <b>${profit_a:,.0f}</b> to <b>${profit_b:,.0f}</b> — a <b>{profit_g:+.1f}%</b> change, signalling {'improved' if profit_g >= 0 else 'declining'} profitability.",
        f"🎯 <b>Margin movement:</b> Overall gross margin went from <b>{margin_a:.1f}%</b> to <b>{margin_b:.1f}%</b> — a shift of <b>{margin_g:+.2f} percentage points</b>.",
        f"🏆 <b>Fastest growing product:</b> <b>{best_product['Product Name']}</b> — sales growth of <b>{best_product['Sales Growth %']:+.1f}%</b> between {yr_a} and {yr_b}.",
        f"⚠️ <b>Biggest decliner:</b> <b>{worst_product['Product Name']}</b> — sales change of <b>{worst_product['Sales Growth %']:+.1f}%</b>. Worth reviewing pricing or market positioning.",
        "🍫 <b>Concentration risk remains:</b> Chocolate division continues to dominate both years — diversification into Sugar is still the key long-term opportunity.",
    ]
    for txt in insights:
        st.markdown(f'<div class="insight-box">{txt}</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────



# ─────────────────────────────────────────────────────────────────────────────
# TAB 7 — SHIPPING ROUTE MAP
# ─────────────────────────────────────────────────────────────────────────────

# Factory coordinates (from project brief)
FACTORY_COORDS = {
    "Lot's O' Nuts":      {"lat": 32.881893, "lng": -111.768036, "city": "Mesa, AZ",               "div": "Chocolate"},
    "Wicked Choccy's":    {"lat": 32.076176, "lng": -81.088371,  "city": "Savannah, GA",             "div": "Chocolate"},
    "Sugar Shack":          {"lat": 48.119140, "lng": -96.181150,  "city": "Thief River Falls, MN",    "div": "Sugar/Other"},
    "Secret Factory":       {"lat": 41.446333, "lng": -90.565487,  "city": "Milan, IL",                "div": "Sugar/Other"},
    "The Other Factory":    {"lat": 35.117500, "lng": -89.971107,  "city": "Memphis, TN",              "div": "Other"},
}

# Product → Factory mapping (from project brief)
PRODUCT_FACTORY = {
    "Wonka Bar - Nutty Crunch Surprise":    "Lot's O' Nuts",
    "Wonka Bar - Fudge Mallows":            "Lot's O' Nuts",
    "Wonka Bar -Scrumdiddlyumptious":       "Lot's O' Nuts",
    "Wonka Bar - Milk Chocolate":           "Wicked Choccy's",
    "Wonka Bar - Triple Dazzle Caramel":    "Wicked Choccy's",
    "Laffy Taffy":                          "Sugar Shack",
    "SweeTARTS":                            "Sugar Shack",
    "Nerds":                                "Sugar Shack",
    "Fun Dip":                              "Sugar Shack",
    "Fizzy Lifting Drinks":                 "Sugar Shack",
    "Everlasting Gobstopper":               "Secret Factory",
    "Lickable Wallpaper":                   "Secret Factory",
    "Wonka Gum":                            "Secret Factory",
    "Hair Toffee":                          "The Other Factory",
    "Kazookles":                            "The Other Factory",
}

# Estimated delivery days per ship mode (realistic logistics estimates)
DELIVERY_DAYS = {
    "Same Day":       {"days": 1,  "hours_min": 4,   "hours_max": 10},
    "First Class":    {"days": 2,  "hours_min": 36,  "hours_max": 52},
    "Second Class":   {"days": 3,  "hours_min": 60,  "hours_max": 84},
    "Standard Class": {"days": 5,  "hours_min": 96,  "hours_max": 144},
}

# Top customer city coordinates
CITY_COORDS = {
    "New York City":  {"lat": 40.7128, "lng": -74.0060,  "state": "NY"},
    "Los Angeles":    {"lat": 34.0522, "lng": -118.2437, "state": "CA"},
    "Philadelphia":   {"lat": 39.9526, "lng": -75.1652,  "state": "PA"},
    "San Francisco":  {"lat": 37.7749, "lng": -122.4194, "state": "CA"},
    "Seattle":        {"lat": 47.6062, "lng": -122.3321, "state": "WA"},
    "Houston":        {"lat": 29.7604, "lng": -95.3698,  "state": "TX"},
    "Chicago":        {"lat": 41.8781, "lng": -87.6298,  "state": "IL"},
    "San Diego":      {"lat": 32.7157, "lng": -117.1611, "state": "CA"},
    "Dallas":         {"lat": 32.7767, "lng": -96.7970,  "state": "TX"},
    "Columbus":       {"lat": 39.9612, "lng": -82.9988,  "state": "OH"},
    "Detroit":        {"lat": 42.3314, "lng": -83.0458,  "state": "MI"},
    "Jacksonville":   {"lat": 30.3322, "lng": -81.6557,  "state": "FL"},
    "Phoenix":        {"lat": 33.4484, "lng": -112.0740, "state": "AZ"},
    "Newark":         {"lat": 40.7357, "lng": -74.1724,  "state": "NJ"},
}


def haversine_miles(lat1, lng1, lat2, lng2):
    """Calculate distance in miles between two lat/lng points."""
    R = 3958.8
    dlat = (lat2 - lat1) * np.pi / 180
    dlng = (lng2 - lng1) * np.pi / 180
    a = (np.sin(dlat/2)**2 +
         np.cos(lat1*np.pi/180) * np.cos(lat2*np.pi/180) * np.sin(dlng/2)**2)
    return round(2 * R * np.arcsin(np.sqrt(a)))


def build_delivery_timeline(factory_name, city_name, ship_mode):
    """Generate step-by-step delivery timeline strings."""
    fcoord = FACTORY_COORDS[factory_name]
    ccoord = CITY_COORDS.get(city_name, {"lat": 39.5, "lng": -98.35})
    dist   = haversine_miles(fcoord["lat"], fcoord["lng"], ccoord["lat"], ccoord["lng"])
    dinfo  = DELIVERY_DAYS[ship_mode]

    # Scale hours by distance ratio
    dist_ratio = min(dist / 2500, 1.0)
    hours = int(dinfo["hours_min"] + dist_ratio * (dinfo["hours_max"] - dinfo["hours_min"]))

    from datetime import datetime, timedelta
    base = datetime(2025, 1, 15, 9, 0)
    steps = []

    steps.append({"icon": "🏭", "time": base.strftime("%b %d, %I:%M %p"),
                  "label": "Order dispatched from factory",
                  "sub":   fcoord["city"]})

    if ship_mode == "Same Day":
        t1 = base + timedelta(hours=1)
        steps.append({"icon": "🚐", "time": t1.strftime("%b %d, %I:%M %p"),
                      "label": "Picked up — priority courier",
                      "sub":   "Same-day express handling"})
        t2 = base + timedelta(hours=hours - 1)
        steps.append({"icon": "📍", "time": t2.strftime("%b %d, %I:%M %p"),
                      "label": "Out for delivery",
                      "sub":   f"Last-mile delivery · {city_name}"})
    else:
        t1 = base + timedelta(hours=3)
        steps.append({"icon": "🚚", "time": t1.strftime("%b %d, %I:%M %p"),
                      "label": f"Carrier pickup — {ship_mode}",
                      "sub":   "Regional logistics handoff"})
        t2 = base + timedelta(hours=int(hours * 0.45))
        steps.append({"icon": "🏢", "time": t2.strftime("%b %d, %I:%M %p"),
                      "label": "In transit — regional hub",
                      "sub":   "Sorting & distribution center"})
        t3 = base + timedelta(hours=int(hours * 0.85))
        steps.append({"icon": "📦", "time": t3.strftime("%b %d, %I:%M %p"),
                      "label": "Out for delivery",
                      "sub":   f"{city_name} local hub"})

    eta = base + timedelta(hours=hours)
    steps.append({"icon": "✅", "time": eta.strftime("%b %d, %I:%M %p"),
                  "label": "Estimated delivery",
                  "sub":   city_name,
                  "final": True})
    return steps, hours, dist


def tab_shipping_routes(df: pd.DataFrame):
    """🚢 Shipping Route Map — factory to customer city with delivery timeline."""
    import math

    # ── Add factory column to df ──
    df2 = df.copy()
    df2["Factory"] = df2["Product Name"].map(PRODUCT_FACTORY).fillna("Unknown")
    df2 = df2[df2["Factory"] != "Unknown"]

    # ── Sidebar-style filters inside tab ──
    st.markdown('''<div class="section-title">🚢 Shipping Route Map — Factory → Customer City</div>''', unsafe_allow_html=True)

    fc1, fc2, fc3 = st.columns(3)
    with fc1:
        sel_factory = st.selectbox("Filter by Factory", ["All Factories"] + list(FACTORY_COORDS.keys()), key="ship_factory")
    with fc2:
        sel_mode = st.selectbox("Filter by Ship Mode", ["All Modes"] + list(DELIVERY_DAYS.keys()), key="ship_mode")
    with fc3:
        sel_city = st.selectbox("Filter by City", ["All Cities"] + [c for c in CITY_COORDS if c in df2["City"].values], key="ship_city")

    # Apply filters
    dff = df2.copy()
    if sel_factory != "All Factories": dff = dff[dff["Factory"] == sel_factory]
    if sel_mode    != "All Modes":     dff = dff[dff["Ship Mode"] == sel_mode]
    if sel_city    != "All Cities":    dff = dff[dff["City"] == sel_city]

    # ── KPI cards ──
    total_orders  = len(dff)
    total_revenue = dff["Sales"].sum()
    avg_margin    = (dff["Gross Profit"].sum() / dff["Sales"].sum() * 100) if dff["Sales"].sum() > 0 else 0
    cities_count  = dff["City"].nunique()

    k1, k2, k3, k4 = st.columns(4)
    kpis = [
        (k1, "📦", "Total Orders",    f"{total_orders:,}",        "kpi-emerald"),
        (k2, "💰", "Total Revenue",   f"${total_revenue:,.0f}",   "kpi-gold"),
        (k3, "🎯", "Avg Margin",      f"{avg_margin:.1f}%",       "kpi-mint"),
        (k4, "🏙️", "Cities Reached",  f"{cities_count}",          "kpi-sage"),
    ]
    for col, icon, label, val, css in kpis:
        with col:
            st.markdown(f'''
            <div class="kpi-card {css}">
                <div class="kpi-label">{icon} {label}</div>
                <div class="kpi-value">{val}</div>
            </div>''', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Build route aggregation for map ──
    route_agg = (dff.groupby(["Factory", "City", "Ship Mode"], as_index=False)
                    .agg(Orders=("Sales","count"), Revenue=("Sales","sum"),
                         Profit=("Gross Profit","sum"))
                    .sort_values("Orders", ascending=False))
    route_agg["Margin"] = (route_agg["Profit"] / route_agg["Revenue"] * 100).round(1)
    route_agg = route_agg[route_agg["City"].isin(CITY_COORDS)]

    # ── Build Plotly map ──
    MODE_COLORS = {
        "Standard Class": "#22D3EE",
        "First Class":    "#5DCAA5",
        "Second Class":   "#AFA9EC",
        "Same Day":       "#EF9F27",
    }
    MODE_DASH = {
        "Standard Class": None,
        "First Class":    "5px,3px",
        "Second Class":   "3px,3px",
        "Same Day":       "8px,2px",
    }

    fig_map = go.Figure()

    # Draw route arcs
    drawn = set()
    for _, row in route_agg.iterrows():
        key = f"{row['Factory']}_{row['City']}_{row['Ship Mode']}"
        if key in drawn: continue
        drawn.add(key)
        fc = FACTORY_COORDS.get(row["Factory"])
        cc = CITY_COORDS.get(row["City"])
        if not fc or not cc: continue

        clr  = MODE_COLORS.get(row["Ship Mode"], "#22D3EE")
        dash = MODE_DASH.get(row["Ship Mode"])
        dist = haversine_miles(fc["lat"], fc["lng"], cc["lat"], cc["lng"])

        # Curved arc via intermediate points
        n_pts = 30
        lats, lons = [], []
        for i in range(n_pts + 1):
            t = i / n_pts
            lat = fc["lat"] * (1-t) + cc["lat"] * t
            lon = fc["lng"] * (1-t) + cc["lng"] * t
            # Add upward curve
            arc = math.sin(math.pi * t) * min(dist / 60, 6)
            lat += arc
            lats.append(lat); lons.append(lon)

        line_cfg = dict(width=1.5, color=clr)
        if dash: line_cfg["dash"] = dash

        fig_map.add_trace(go.Scattergeo(
            lat=lats, lon=lons, mode="lines",
            line=line_cfg,
            opacity=0.55,
            name=row["Ship Mode"],
            showlegend=False,
            hovertemplate=(
                f"<b>{row['Factory']} → {row['City']}</b><br>"
                f"Mode: {row['Ship Mode']}<br>"
                f"Orders: {int(row['Orders']):,}<br>"
                f"Revenue: ${row['Revenue']:,.0f}<br>"
                f"Margin: {row['Margin']}%"
                "<extra></extra>"
            ),
        ))

    # Draw factory markers (orange squares styled via marker symbol)
    fact_lats, fact_lons, fact_text, fact_hover = [], [], [], []
    for name, fc in FACTORY_COORDS.items():
        if sel_factory not in ("All Factories", name): continue
        fact_lats.append(fc["lat"]); fact_lons.append(fc["lng"])
        fact_text.append(name.split("'")[0][:12])
        fact_hover.append(f"<b>🏭 {name}</b><br>{fc['city']}<br>Division: {fc['div']}")

    fig_map.add_trace(go.Scattergeo(
        lat=fact_lats, lon=fact_lons,
        mode="markers+text",
        marker=dict(size=14, color="#EF9F27", symbol="square",
                    line=dict(color="#FFF", width=1.5)),
        text=fact_text, textposition="top center",
        textfont=dict(color="#FAC775", size=9),
        name="Factory",
        hovertemplate="%{hovertext}<extra></extra>",
        hovertext=fact_hover,
    ))

    # Draw city markers (cyan circles)
    city_rows = route_agg.groupby("City").agg(
        Orders=("Orders","sum"), Revenue=("Revenue","sum"), Margin=("Margin","mean")
    ).reset_index()
    city_lats, city_lons, city_text, city_hover, city_sizes = [], [], [], [], []
    for _, row in city_rows.iterrows():
        cc = CITY_COORDS.get(row["City"])
        if not cc: continue
        city_lats.append(cc["lat"]); city_lons.append(cc["lng"])
        city_text.append(row["City"][:10])
        city_hover.append(
            f"<b>📍 {row['City']}</b><br>"
            f"Orders: {int(row['Orders']):,}<br>"
            f"Revenue: ${row['Revenue']:,.0f}<br>"
            f"Avg Margin: {row['Margin']:.1f}%"
        )
        city_sizes.append(max(8, min(20, int(row["Orders"]) // 40 + 8)))

    fig_map.add_trace(go.Scattergeo(
        lat=city_lats, lon=city_lons,
        mode="markers+text",
        marker=dict(size=city_sizes, color="#22D3EE", opacity=0.85,
                    line=dict(color="#041628", width=1.5)),
        text=city_text, textposition="top center",
        textfont=dict(color="#67E8F9", size=9),
        name="Customer City",
        hovertemplate="%{hovertext}<extra></extra>",
        hovertext=city_hover,
    ))

    fig_map.update_layout(
        geo=dict(
            scope="usa",
            bgcolor="rgba(4,18,40,0.0)",
            landcolor="#071E33",
            subunitcolor="rgba(6,182,212,0.2)",
            countrycolor="rgba(6,182,212,0.3)",
            showlakes=True, lakecolor="#041628",
            showcoastlines=True, coastlinecolor="rgba(6,182,212,0.25)",
            projection_type="albers usa",
        ),
        paper_bgcolor="rgba(4,12,28,0.95)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=10, b=0),
        height=480,
        showlegend=False,
        font=dict(color="#BAE6FD"),
    )
    st.plotly_chart(fig_map, use_container_width=True)

    # ── Legend ──
    leg_cols = st.columns(4)
    legend_items = [
        ("#22D3EE", "Standard Class", "solid"),
        ("#5DCAA5", "First Class",    "dashed"),
        ("#AFA9EC", "Second Class",   "dotted"),
        ("#EF9F27", "Same Day",       "dashed"),
    ]
    for col, (clr, label, style) in zip(leg_cols, legend_items):
        with col:
            st.markdown(
                f'''<div style="display:flex;align-items:center;gap:6px;font-size:11px;color:#BAE6FD;">
                <div style="width:24px;height:3px;background:{clr};border-radius:2px;"></div>
                {label}</div>''', unsafe_allow_html=True)

    st.markdown("---")

    # ── Route table with click-to-expand delivery timeline ──
    st.markdown('''<div class="section-title">📋 Route Details — Click to See Delivery Timeline & ETA</div>''', unsafe_allow_html=True)

    top_routes = route_agg.head(20).reset_index(drop=True)

    MODE_BADGE = {
        "Standard Class": ("background:#0E4F6B;color:#67E8F9",   "Standard"),
        "First Class":    ("background:#0D5240;color:#5DCAA5",   "First"),
        "Second Class":   ("background:#2D2660;color:#AFA9EC",   "Second"),
        "Same Day":       ("background:#5C3206;color:#EF9F27",   "Same Day"),
    }

    selected_idx = st.session_state.get("selected_route_idx", None)

    for i, row in top_routes.iterrows():
        badge_style, badge_label = MODE_BADGE.get(row["Ship Mode"], ("", row["Ship Mode"]))
        fc_info = FACTORY_COORDS.get(row["Factory"], {})
        dist = 0
        if fc_info and row["City"] in CITY_COORDS:
            cc = CITY_COORDS[row["City"]]
            dist = haversine_miles(fc_info["lat"], fc_info["lng"], cc["lat"], cc["lng"])
        dinfo = DELIVERY_DAYS[row["Ship Mode"]]

        is_selected = selected_idx == i
        border_style = "border-left: 3px solid #22D3EE;" if is_selected else "border-left: 3px solid transparent;"

        col_a, col_b = st.columns([4, 1])
        with col_a:
            st.markdown(f'''
            <div style="background:rgba(8,50,100,0.25);border:0.5px solid rgba(6,182,212,0.2);
                        border-radius:10px;padding:10px 14px;{border_style}margin-bottom:2px;">
              <div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;">
                <span style="font-size:13px;">🏭</span>
                <span style="color:#EF9F27;font-size:12px;font-weight:500;min-width:130px">{row["Factory"]}</span>
                <span style="color:#BAE6FD;font-size:14px;">→</span>
                <span style="font-size:13px;">📍</span>
                <span style="color:#22D3EE;font-size:12px;font-weight:500;flex:1">{row["City"]}</span>
                <span style="{badge_style};padding:2px 8px;border-radius:10px;font-size:10px;font-weight:500">{badge_label}</span>
                <span style="color:#BAE6FD;font-size:11px;">{int(row["Orders"]):,} orders</span>
                <span style="color:#67E8F9;font-size:11px;">${row["Revenue"]:,.0f}</span>
                <span style="color:#A5F3FC;font-size:11px;">{dinfo["days"]}d est.</span>
                <span style="color:#BAE6FD;font-size:11px;">{dist:,} mi</span>
              </div>
            </div>''', unsafe_allow_html=True)
        with col_b:
            if st.button("📅 Timeline", key=f"btn_{i}"):
                if selected_idx == i:
                    st.session_state["selected_route_idx"] = None
                else:
                    st.session_state["selected_route_idx"] = i
                st.rerun()

        # ── Delivery Timeline Panel (expands below the row) ──
        if is_selected and row["City"] in CITY_COORDS:
            steps, hours, dist_miles = build_delivery_timeline(
                row["Factory"], row["City"], row["Ship Mode"]
            )
            progress_pct = 60

            with st.container():
                st.markdown(f'''
                <div style="background:#041E33;border:1px solid rgba(6,182,212,0.35);
                            border-radius:12px;padding:16px 20px;margin:4px 0 10px;">
                  <div style="display:flex;gap:24px;flex-wrap:wrap;">

                    <!-- Timeline steps -->
                    <div style="flex:1;min-width:220px;">
                      <div style="font-size:11px;color:rgba(186,230,253,0.5);
                                  text-transform:uppercase;letter-spacing:0.5px;margin-bottom:12px;">
                        Delivery Timeline
                      </div>
                      {"".join([
                        f'''<div style="display:flex;gap:10px;margin-bottom:{"0" if j==len(steps)-1 else "16px"}">
                          <div style="display:flex;flex-direction:column;align-items:center;width:24px;flex-shrink:0;">
                            <div style="width:12px;height:12px;border-radius:50%;
                                        background:{"#22D3EE" if s.get("final") else "#0E7490"};
                                        {"box-shadow:0 0 0 3px rgba(34,211,238,0.2)" if s.get("final") else ""};
                                        margin-top:2px;flex-shrink:0;"></div>
                            {"'''<div style=\"width:2px;flex:1;background:rgba(6,182,212,0.2);margin:3px 0;min-height:20px\"></div>'''" if j < len(steps)-1 else ""}
                          </div>
                          <div>
                            <div style="font-size:11px;font-weight:500;color:#22D3EE;">{s["time"]}</div>
                            <div style="font-size:12px;color:rgba(186,230,253,0.85);">{s["label"]}</div>
                            <div style="font-size:11px;color:rgba(186,230,253,0.45);">{s["sub"]}</div>
                          </div>
                        </div>'''
                        for j, s in enumerate(steps)
                      ])}
                    </div>

                    <!-- Summary panel -->
                    <div style="flex:1;min-width:180px;">
                      <div style="font-size:11px;color:rgba(186,230,253,0.5);
                                  text-transform:uppercase;letter-spacing:0.5px;margin-bottom:12px;">
                        Shipment Summary
                      </div>
                      <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;">
                        <div>
                          <div style="font-size:10px;color:rgba(186,230,253,0.45);text-transform:uppercase;letter-spacing:0.5px;">Ship Mode</div>
                          <div style="font-size:13px;font-weight:500;color:#fff;margin-top:2px;">{row["Ship Mode"]}</div>
                        </div>
                        <div>
                          <div style="font-size:10px;color:rgba(186,230,253,0.45);text-transform:uppercase;letter-spacing:0.5px;">Est. Delivery</div>
                          <div style="font-size:13px;font-weight:500;color:#fff;margin-top:2px;">{hours} hrs</div>
                          <div style="font-size:10px;color:rgba(186,230,253,0.4);">≈ {DELIVERY_DAYS[row["Ship Mode"]]["days"]} business day(s)</div>
                        </div>
                        <div>
                          <div style="font-size:10px;color:rgba(186,230,253,0.45);text-transform:uppercase;letter-spacing:0.5px;">Distance</div>
                          <div style="font-size:13px;font-weight:500;color:#fff;margin-top:2px;">{dist_miles:,} miles</div>
                        </div>
                        <div>
                          <div style="font-size:10px;color:rgba(186,230,253,0.45);text-transform:uppercase;letter-spacing:0.5px;">Orders</div>
                          <div style="font-size:13px;font-weight:500;color:#fff;margin-top:2px;">{int(row["Orders"]):,}</div>
                        </div>
                        <div>
                          <div style="font-size:10px;color:rgba(186,230,253,0.45);text-transform:uppercase;letter-spacing:0.5px;">Revenue</div>
                          <div style="font-size:13px;font-weight:500;color:#fff;margin-top:2px;">${row["Revenue"]:,.0f}</div>
                        </div>
                        <div>
                          <div style="font-size:10px;color:rgba(186,230,253,0.45);text-transform:uppercase;letter-spacing:0.5px;">Margin</div>
                          <div style="font-size:13px;font-weight:500;color:#22D3EE;margin-top:2px;">{row["Margin"]}%</div>
                        </div>
                      </div>
                      <div style="margin-top:14px;">
                        <div style="font-size:10px;color:rgba(186,230,253,0.4);margin-bottom:4px;">In-transit progress (simulated)</div>
                        <div style="height:5px;background:rgba(6,182,212,0.12);border-radius:3px;overflow:hidden;">
                          <div style="height:5px;width:{progress_pct}%;background:#22D3EE;border-radius:3px;"></div>
                        </div>
                        <div style="font-size:10px;color:rgba(186,230,253,0.35);margin-top:3px;">
                          In transit — {progress_pct}% of route complete
                        </div>
                      </div>
                    </div>
                  </div>
                </div>''', unsafe_allow_html=True)

    st.markdown("---")

    # ── Ship Mode Performance Table ──
    st.markdown('''<div class="section-title">📊 Ship Mode Performance Summary</div>''', unsafe_allow_html=True)
    mode_summary = (dff.groupby("Ship Mode", as_index=False)
                       .agg(Orders=("Sales","count"), Revenue=("Sales","sum"),
                            Profit=("Gross Profit","sum"))
                       .sort_values("Orders", ascending=False))
    mode_summary["Margin (%)"]    = (mode_summary["Profit"] / mode_summary["Revenue"] * 100).round(1)
    mode_summary["Avg Order ($)"] = (mode_summary["Revenue"] / mode_summary["Orders"]).round(2)
    mode_summary["Est. Days"]     = mode_summary["Ship Mode"].map(lambda m: DELIVERY_DAYS.get(m,{}).get("days","?"))
    mode_summary["Revenue"]       = mode_summary["Revenue"].map("${:,.0f}".format)
    mode_summary["Profit"]        = mode_summary["Profit"].map("${:,.0f}".format)
    mode_summary["Avg Order ($)"] = mode_summary["Avg Order ($)"].map("${:,.2f}".format)
    st.dataframe(mode_summary[["Ship Mode","Orders","Revenue","Profit","Margin (%)","Avg Order ($)","Est. Days"]],
                 use_container_width=True, hide_index=True)

    # ── Insights ──
    st.markdown('''<div class="section-title">💡 Shipping Insights</div>''', unsafe_allow_html=True)
    for txt in [
        "🚢 <b>Standard Class dominates at 60%</b> of all orders — customers prioritize cost over speed, reducing logistics pressure.",
        "💰 <b>All ship modes earn nearly identical margins (~65.7–66.1%)</b> — premium shipping (Same Day, First Class) generates no margin advantage. Nassau Candy may be absorbing the speed premium cost.",
        "🌊 <b>Pacific region leads in every shipping mode</b> — Los Angeles, San Francisco and Seattle together account for the highest order volume across all categories.",
        "⚡ <b>Same Day shipping (547 orders)</b> is used predominantly for Chocolate division products — the high-value items most likely to justify express costs.",
        "📋 <b>Recommendation:</b> Review Same Day and First Class pricing — if margins are equal to Standard Class, the premium cost is being absorbed rather than passed to customers.",
    ]:
        st.markdown(f'''<div class="insight-box">{txt}</div>''', unsafe_allow_html=True)


def main():
    try:
        df_raw = load_data()
    except FileNotFoundError:
        st.error("""⚠️ **Dataset not found.** Place your file in the same folder as `app.py`:
- `Nassau_Candy_Distributor.csv` / `.xlsx`
- `Nassau Candy Distributor.csv` / `.xlsx`
Then restart the app.""")
        st.stop()
    except Exception as e:
        st.error(f"⚠️ Error loading data: {e}")
        st.stop()

    # ── Header ──
    st.markdown("""
    <div class="dash-header">
        <h1>🍫 Nassau Candy Distributor — Profitability Dashboard</h1>
        <p>Product Line &amp; Margin Performance Analysis &nbsp;·&nbsp; Jan 2025 – Dec 2025 &nbsp;·&nbsp; 10,194 Orders</p>
    </div>
    """, unsafe_allow_html=True)

    df, sel_div, sel_year, margin_min, prod_search = render_sidebar(df_raw)

    if df.empty:
        st.warning("No data matches the current filters. Relax the threshold or change the selection.")
        st.stop()

    # ── Active filter badge ──
    active = []
    if sel_div  != "All":   active.append(f"Division: **{sel_div}**")
    if sel_year != "All":   active.append(f"Year: **{sel_year}**")
    if margin_min > 0:      active.append(f"Margin ≥ **{margin_min}%**")
    if prod_search.strip(): active.append(f"Search: **'{prod_search}'**")
    if active:
        st.info("🔍 Active filters — " + "  ·  ".join(active) + f"  ·  {len(df):,} rows")

    render_kpis(df)
    st.markdown("---")

    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📊 Product Overview",
        "🏭 Division Performance",
        "🔬 Cost Diagnostics",
        "📈 Profit Concentration",
        "📅 Year-over-Year",
        "🔮 Forecast",
        "🚢 Shipping Routes",
    ])

    with tab1: tab_product_overview(df)
    with tab2: tab_division_performance(df)
    with tab3: tab_cost_diagnostics(df)
    with tab4: tab_pareto_analysis(df)
    with tab5: tab_yoy_comparison(df_raw)
    with tab6: tab_forecast(df_raw)  # always uses full unfiltered data for trend accuracy
    with tab7: tab_shipping_routes(df_raw)

    st.markdown("---")
    st.caption("Nassau Candy Distributor · Profitability Analytics Dashboard · Ocean Fresh Theme · Built with Streamlit & Plotly")


# ─────────────────────────────────────────────────────────────────────────────
# TAB 6 — FORECASTING (Linear Regression — Next 6 Months)
# ─────────────────────────────────────────────────────────────────────────────

def _linreg_forecast(series_vals, n_future=6):
    """
    OLS linear regression using only numpy.
    Returns: slope, intercept, y_pred, y_future, conf_band, r2, mae
    """
    x       = np.arange(1, len(series_vals) + 1, dtype=float)
    slope, intercept = np.polyfit(x, series_vals, 1)
    y_pred  = slope * x + intercept
    resid   = series_vals - y_pred
    std_res = resid.std()

    x_fut   = np.arange(len(series_vals) + 1, len(series_vals) + n_future + 1, dtype=float)
    y_fut   = slope * x_fut + intercept
    # confidence band widens the further we project
    conf    = 1.96 * std_res * (1 + (x_fut - x[-1]) / len(x))

    ss_res  = (resid ** 2).sum()
    ss_tot  = ((series_vals - series_vals.mean()) ** 2).sum()
    r2      = float(1 - ss_res / ss_tot) if ss_tot != 0 else 0.0
    mae     = float(np.abs(resid).mean())
    return slope, intercept, y_pred, y_fut, conf, r2, mae


def _add_divider(fig, x_label):
    """
    Draw a vertical divider on a categorical-axis figure.
    Uses add_shape (works in Plotly 6) instead of add_vline (broken in Plotly 6).
    """
    fig.add_shape(
        type="line", xref="x", yref="paper",
        x0=x_label, x1=x_label, y0=0, y1=1,
        line=dict(color="rgba(255,255,255,0.22)", width=1.5, dash="dash"),
    )
    fig.add_annotation(
        xref="x", yref="paper",
        x=x_label, y=0.97,
        text="  ← history │ forecast →",
        showarrow=False,
        font=dict(color="#BAE6FD", size=10),
        xanchor="left",
    )


def tab_forecast(df_raw):
    """Linear-regression forecast for the next 6 months of Sales & Profit."""
    N_FUTURE  = 6
    C_HIST    = "#22D3EE"
    C_FORE    = "#38BDF8"
    C_BAND_S  = "rgba(56,189,248,0.12)"
    C_BAND_P  = "rgba(6,182,212,0.12)"

    # ── Monthly history (unfiltered) ──
    monthly = (
        df_raw.groupby("Month", as_index=False)
        .agg(Sales=("Sales", "sum"), Profit=("Gross Profit", "sum"))
        .sort_values("Month")
    )
    monthly["MonthDT"]    = pd.to_datetime(monthly["Month"])
    monthly["MonthLabel"] = monthly["MonthDT"].dt.strftime("%b %Y")

    if len(monthly) < 4:
        st.warning("⚠️ Need at least 4 months of data for a reliable forecast.")
        return

    sales_arr   = monthly["Sales"].values.astype(float)
    profit_arr  = monthly["Profit"].values.astype(float)
    hist_labels = monthly["MonthLabel"].tolist()
    last_label  = hist_labels[-1]

    last_dt    = monthly["MonthDT"].iloc[-1]
    fut_labels = [(last_dt + pd.DateOffset(months=i+1)).strftime("%b %Y") for i in range(N_FUTURE)]
    month_names = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

    s_slope, s_int, s_pred, s_fut, s_band, s_r2, s_mae = _linreg_forecast(sales_arr,  N_FUTURE)
    p_slope, p_int, p_pred, p_fut, p_band, p_r2, p_mae = _linreg_forecast(profit_arr, N_FUTURE)

    # ── Info banner ──
    st.markdown("""
    <div style="background:rgba(8,50,100,0.45);border:1px solid rgba(6,182,212,0.3);
                border-left:4px solid #22D3EE;border-radius:0 12px 12px 0;
                padding:0.9rem 1.2rem;margin-bottom:1.2rem;">
        <b style="color:#67E8F9;">🔮 How this forecast works</b><br>
        <span style="color:#BAE6FD;font-size:0.84rem;">
        Ordinary Least Squares (OLS) linear regression is fitted on all historical monthly data.
        The model captures the underlying growth trend and projects it 6 months forward.
        The shaded band is the <b>95% confidence interval</b> — it widens each month to reflect
        compounding uncertainty. R² measures how well the trend line fits historical data (1.0 = perfect).
        </span>
    </div>
    """, unsafe_allow_html=True)

    # ── Model KPI cards ──
    st.markdown('<div class="section-title">🧮 Model Performance Metrics</div>', unsafe_allow_html=True)
    k1, k2, k3, k4 = st.columns(4)
    for col, label, val, css, sub1, sub2 in [
        (k1, "Sales R² Score",   f"{s_r2:.3f}",      "kpi-emerald", "Trend fit quality",  "1.0 = perfect fit"),
        (k2, "Profit R² Score",  f"{p_r2:.3f}",      "kpi-gold",    "Trend fit quality",  "1.0 = perfect fit"),
        (k3, "Sales MAE",        f"${s_mae:,.0f}",   "kpi-mint",    "Avg monthly error",  "Lower is better"),
        (k4, "Forecast Horizon", f"{N_FUTURE} mo.",  "kpi-sage",    f"{fut_labels[0]}",   f"→ {fut_labels[-1]}"),
    ]:
        with col:
            st.markdown(f"""
            <div class="kpi-card {css}">
                <div class="kpi-label">📐 {label}</div>
                <div class="kpi-value">{val}</div>
                <div class="kpi-sub">{sub1}</div>
                <div class="kpi-sub">{sub2}</div>
            </div>""", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")

    # ── Sales forecast chart ──
    st.markdown('<div class="section-title">📈 Sales Forecast — Next 6 Months</div>', unsafe_allow_html=True)
    all_x_s = hist_labels + fut_labels

    fig_sales = go.Figure()
    fig_sales.add_trace(go.Scatter(
        x=hist_labels, y=sales_arr,
        name="Actual Sales", mode="lines+markers",
        line=dict(color=C_HIST, width=2.5),
        marker=dict(size=6, color=C_HIST),
        hovertemplate="<b>%{x}</b><br>Actual: $%{y:,.0f}<extra></extra>",
    ))
    fig_sales.add_trace(go.Scatter(
        x=hist_labels, y=s_pred,
        name="Trend Line", mode="lines",
        line=dict(color="#67E8F9", width=1.5, dash="dot"),
        hovertemplate="<b>%{x}</b><br>Trend: $%{y:,.0f}<extra></extra>",
    ))
    fig_sales.add_trace(go.Scatter(
        x=fut_labels, y=(s_fut + s_band).tolist(),
        mode="lines", line=dict(width=0),
        showlegend=False, hoverinfo="skip",
    ))
    fig_sales.add_trace(go.Scatter(
        x=fut_labels, y=(s_fut - s_band).tolist(),
        name="95% Confidence Band", mode="lines",
        fill="tonexty", fillcolor=C_BAND_S,
        line=dict(width=0, color="rgba(0,0,0,0)"),
        hovertemplate="<b>%{x}</b><br>Lower: $%{y:,.0f}<extra></extra>",
    ))
    fig_sales.add_trace(go.Scatter(
        x=fut_labels, y=s_fut,
        name="Forecast", mode="lines+markers",
        line=dict(color=C_FORE, width=2.5, dash="dash"),
        marker=dict(size=8, symbol="diamond", color=C_FORE,
                    line=dict(color="rgba(255,255,255,0.4)", width=1)),
        hovertemplate="<b>%{x}</b><br>Forecast: $%{y:,.0f}<extra></extra>",
    ))
    _add_divider(fig_sales, last_label)
    fig_sales.update_layout(
        **PLOTLY_LAYOUT, height=370,
        title=f"Monthly Sales — Historical + {N_FUTURE}-Month Linear Regression Forecast",
        legend=LEG_H,
    )
    apply_axes(fig_sales,
               xkw=dict(tickangle=-38, tickfont=dict(color="#BAE6FD", size=10)),
               ykw=dict(tickprefix="$", tickformat=",.0f"))
    st.plotly_chart(fig_sales, use_container_width=True)
    st.markdown("---")

    # ── Profit forecast chart ──
    st.markdown('<div class="section-title">💰 Gross Profit Forecast — Next 6 Months</div>', unsafe_allow_html=True)
    fig_profit = go.Figure()
    fig_profit.add_trace(go.Scatter(
        x=hist_labels, y=profit_arr,
        name="Actual Profit", mode="lines+markers",
        line=dict(color="#06B6D4", width=2.5),
        marker=dict(size=6, color="#06B6D4"),
        hovertemplate="<b>%{x}</b><br>Actual: $%{y:,.0f}<extra></extra>",
    ))
    fig_profit.add_trace(go.Scatter(
        x=hist_labels, y=p_pred,
        name="Trend Line", mode="lines",
        line=dict(color="#A5F3FC", width=1.5, dash="dot"),
        hovertemplate="<b>%{x}</b><br>Trend: $%{y:,.0f}<extra></extra>",
    ))
    fig_profit.add_trace(go.Scatter(
        x=fut_labels, y=(p_fut + p_band).tolist(),
        mode="lines", line=dict(width=0),
        showlegend=False, hoverinfo="skip",
    ))
    fig_profit.add_trace(go.Scatter(
        x=fut_labels, y=(p_fut - p_band).tolist(),
        name="95% Confidence Band", mode="lines",
        fill="tonexty", fillcolor=C_BAND_P,
        line=dict(width=0, color="rgba(0,0,0,0)"),
        hovertemplate="<b>%{x}</b><br>Lower: $%{y:,.0f}<extra></extra>",
    ))
    fig_profit.add_trace(go.Scatter(
        x=fut_labels, y=p_fut,
        name="Forecast", mode="lines+markers",
        line=dict(color="#0EA5E9", width=2.5, dash="dash"),
        marker=dict(size=8, symbol="diamond", color="#0EA5E9",
                    line=dict(color="rgba(255,255,255,0.4)", width=1)),
        hovertemplate="<b>%{x}</b><br>Forecast: $%{y:,.0f}<extra></extra>",
    ))
    _add_divider(fig_profit, last_label)
    fig_profit.update_layout(
        **PLOTLY_LAYOUT, height=370,
        title=f"Monthly Gross Profit — Historical + {N_FUTURE}-Month Linear Regression Forecast",
        legend=LEG_H,
    )
    apply_axes(fig_profit,
               xkw=dict(tickangle=-38, tickfont=dict(color="#BAE6FD", size=10)),
               ykw=dict(tickprefix="$", tickformat=",.0f"))
    st.plotly_chart(fig_profit, use_container_width=True)
    st.markdown("---")

    # ── Division-level forecasts ──
    st.markdown('<div class="section-title">🏭 Division-Level Sales Forecast</div>', unsafe_allow_html=True)
    divisions   = sorted(df_raw["Division"].unique().tolist())
    div_palette = {"Chocolate": "#22D3EE", "Other": "#38BDF8", "Sugar": "#06B6D4"}
    div_cols    = st.columns(len(divisions))

    for col, div in zip(div_cols, divisions):
        mdiv = (
            df_raw[df_raw["Division"] == div]
            .groupby("Month", as_index=False)
            .agg(Sales=("Sales", "sum"))
            .sort_values("Month")
        )
        if len(mdiv) < 4:
            with col:
                st.caption(f"{div}: insufficient data")
            continue
        mdiv["MonthDT"]    = pd.to_datetime(mdiv["Month"])
        mdiv["MonthLabel"] = mdiv["MonthDT"].dt.strftime("%b %Y")
        arr_d   = mdiv["Sales"].values.astype(float)
        last_d  = mdiv["MonthLabel"].iloc[-1]
        _, _, d_pred, d_fut, d_band, d_r2, _ = _linreg_forecast(arr_d, N_FUTURE)
        clr     = div_palette.get(div, "#22D3EE")

        fig_d = go.Figure()
        fig_d.add_trace(go.Scatter(
            x=mdiv["MonthLabel"].tolist(), y=arr_d,
            name="Actual", mode="lines",
            line=dict(color=clr, width=2),
            hovertemplate="<b>%{x}</b><br>$%{y:,.0f}<extra></extra>",
        ))
        fig_d.add_trace(go.Scatter(
            x=fut_labels, y=(d_fut + d_band).tolist(),
            mode="lines", line=dict(width=0),
            showlegend=False, hoverinfo="skip",
        ))
        fig_d.add_trace(go.Scatter(
            x=fut_labels, y=(d_fut - d_band).tolist(),
            mode="lines", fill="tonexty",
            fillcolor="rgba(34,211,238,0.10)",
            line=dict(width=0), showlegend=False, hoverinfo="skip",
        ))
        fig_d.add_trace(go.Scatter(
            x=fut_labels, y=d_fut,
            name="Forecast", mode="lines+markers",
            line=dict(color=clr, width=2, dash="dash"),
            marker=dict(size=6, symbol="diamond", color=clr),
            hovertemplate="<b>%{x}</b><br>Forecast: $%{y:,.0f}<extra></extra>",
        ))
        _add_divider(fig_d, last_d)
        fig_d.update_layout(
            **PLOTLY_LAYOUT, height=270, showlegend=False,
            title=f"{div} · R²={d_r2:.3f}",
        )
        fig_d.update_layout(margin=dict(l=40, r=15, t=55, b=40))
        apply_axes(fig_d,
                   xkw=dict(tickangle=-45, tickfont=dict(color="#BAE6FD", size=9), nticks=4),
                   ykw=dict(tickprefix="$", tickformat=",.0f"))
        with col:
            st.plotly_chart(fig_d, use_container_width=True)

    st.markdown("---")

    # ── Top 5 products forecast ──
    st.markdown('<div class="section-title">🏆 Top 5 Products — Sales Forecast</div>', unsafe_allow_html=True)
    top5        = (df_raw.groupby("Product Name")["Sales"]
                   .sum().sort_values(ascending=False).head(5).index.tolist())
    prod_colors = ["#22D3EE", "#38BDF8", "#06B6D4", "#67E8F9", "#0EA5E9"]

    fig_top = go.Figure()
    for prod, pclr in zip(top5, prod_colors):
        mp = (
            df_raw[df_raw["Product Name"] == prod]
            .groupby("Month", as_index=False).agg(Sales=("Sales", "sum"))
            .sort_values("Month")
        )
        if len(mp) < 4:
            continue
        mp["MonthDT"]    = pd.to_datetime(mp["Month"])
        mp["MonthLabel"] = mp["MonthDT"].dt.strftime("%b %Y")
        arr_p   = mp["Sales"].values.astype(float)
        _, _, _, p_fut_p, _, _, _ = _linreg_forecast(arr_p, N_FUTURE)
        short = prod.replace("Wonka Bar - ", "WB ").replace("Wonka Bar -", "WB ")
        fig_top.add_trace(go.Scatter(
            x=mp["MonthLabel"].tolist(), y=arr_p,
            name=short, mode="lines",
            line=dict(color=pclr, width=1.8),
            hovertemplate=f"<b>{short}</b><br>%{{x}}: $%{{y:,.0f}}<extra></extra>",
        ))
        fig_top.add_trace(go.Scatter(
            x=fut_labels, y=p_fut_p,
            name=f"{short} fcst", mode="lines+markers",
            line=dict(color=pclr, width=1.8, dash="dash"),
            marker=dict(size=5, symbol="diamond", color=pclr),
            showlegend=False,
            hovertemplate=f"<b>{short} forecast</b><br>%{{x}}: $%{{y:,.0f}}<extra></extra>",
        ))
    _add_divider(fig_top, last_label)
    fig_top.update_layout(
        **PLOTLY_LAYOUT, height=370,
        title="Top 5 Products — Actual + 6-Month Forecast",
        legend=LEG_H,
    )
    apply_axes(fig_top,
               xkw=dict(tickangle=-38, tickfont=dict(color="#BAE6FD", size=10)),
               ykw=dict(tickprefix="$", tickformat=",.0f"))
    st.plotly_chart(fig_top, use_container_width=True)
    st.markdown("---")

    # ── Forecast summary table ──
    st.markdown('<div class="section-title">📋 6-Month Forecast Summary Table</div>', unsafe_allow_html=True)
    forecast_table = pd.DataFrame({
        "Month":               fut_labels,
        "Forecast Sales":      [f"${v:,.0f}" for v in s_fut],
        "Sales Low (95%)":     [f"${max(v,0):,.0f}" for v in (s_fut - s_band)],
        "Sales High (95%)":    [f"${v:,.0f}" for v in (s_fut + s_band)],
        "Forecast Profit":     [f"${v:,.0f}" for v in p_fut],
        "Profit Low (95%)":    [f"${max(v,0):,.0f}" for v in (p_fut - p_band)],
        "Profit High (95%)":   [f"${v:,.0f}" for v in (p_fut + p_band)],
        "Forecast Margin (%)": [f"{(pf/sf*100):.1f}%" if sf > 0 else "N/A"
                                for pf, sf in zip(p_fut, s_fut)],
    })
    st.dataframe(forecast_table, use_container_width=True, hide_index=True)
    st.caption("📌 Actual results will likely fall within the Low–High range. Ranges widen each month due to compounding uncertainty.")
    st.markdown("---")

    # ── Forecast bar chart ──
    st.markdown('<div class="section-title">📊 Forecasted Sales vs Profit — Next 6 Months</div>', unsafe_allow_html=True)
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        name="Forecast Sales", x=fut_labels, y=s_fut,
        marker=dict(color="rgba(34,211,238,0.70)", line=dict(color="#22D3EE", width=1)),
        error_y=dict(type="data", array=s_band, color="rgba(255,255,255,0.35)", thickness=1.5, width=6),
        hovertemplate="<b>%{x}</b><br>Sales: $%{y:,.0f}<extra></extra>",
    ))
    fig_bar.add_trace(go.Bar(
        name="Forecast Profit", x=fut_labels, y=p_fut,
        marker=dict(color="rgba(6,182,212,0.70)", line=dict(color="#06B6D4", width=1)),
        error_y=dict(type="data", array=p_band, color="rgba(255,255,255,0.35)", thickness=1.5, width=6),
        hovertemplate="<b>%{x}</b><br>Profit: $%{y:,.0f}<extra></extra>",
    ))
    fig_bar.update_layout(
        **PLOTLY_LAYOUT, barmode="group", height=320,
        title="Forecasted Sales & Profit — Next 6 Months (error bars = 95% CI)",
        legend=LEG_H,
    )
    apply_axes(fig_bar,
               xkw=dict(tickfont=dict(color="#BAE6FD")),
               ykw=dict(tickprefix="$", tickformat=",.0f"))
    st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown("---")

    # ── Insights ──
    st.markdown('<div class="section-title">💡 Forecast Insights</div>', unsafe_allow_html=True)
    total_fut_sales  = s_fut.sum()
    total_fut_profit = p_fut.sum()
    avg_fut_margin   = float((p_fut / np.where(s_fut > 0, s_fut, 1) * 100).mean())
    fit_q = "strong" if s_r2 > 0.7 else ("moderate" if s_r2 > 0.4 else "weak")
    trend_s = "upward 📈" if s_slope > 0 else "downward 📉"
    trend_p = "upward 📈" if p_slope > 0 else "downward 📉"
    for txt in [
        f"📈 <b>Sales trend:</b> The model identifies a <b>{trend_s}</b> trajectory of <b>${abs(s_slope):,.0f}/month</b>. Projected 6-month total: <b>${total_fut_sales:,.0f}</b>.",
        f"💰 <b>Profit trend:</b> Gross profit follows a <b>{trend_p}</b> path of <b>${abs(p_slope):,.0f}/month</b>. Forecasted 6-month profit: <b>${total_fut_profit:,.0f}</b>.",
        f"🎯 <b>Forecasted margin:</b> Average gross margin over the next 6 months is projected at <b>{avg_fut_margin:.1f}%</b> — {'healthy and stable' if avg_fut_margin > 60 else 'requires attention'}.",
        f"🧮 <b>Model quality:</b> Sales R² of <b>{s_r2:.3f}</b> indicates a <b>{fit_q}</b> linear fit. {'Reliable for short-term planning.' if s_r2 > 0.6 else 'Seasonal patterns may affect accuracy — treat as directional guidance.'}",
        f"⚠️ <b>Uncertainty:</b> Confidence bands widen each month — {fut_labels[-1]} carries more uncertainty than {fut_labels[0]}. Use Low–High ranges for budgeting, not point estimates.",
        "🍫 <b>Key risk:</b> Chocolate drives ~93% of revenue. Any supply disruption or demand shift in that division will significantly alter these projections.",
    ]:
        st.markdown(f'<div class="insight-box">{txt}</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()