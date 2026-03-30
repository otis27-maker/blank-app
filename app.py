
import os
import pandas as pd
import numpy as np
import altair as alt
import streamlit as st
from datetime import datetime

# ---------------------------
# Page config
# ---------------------------
st.set_page_config(
    page_title="Banking Sector CTI Dashboard",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------
# Helper functions
# ---------------------------
@st.cache_data(show_spinner=False)
def load_data():
    threats_path = os.path.join("data", "threats_sample.csv")
    assets_path = os.path.join("data", "assets_sample.csv")
    threats = pd.read_csv(threats_path, parse_dates=["date"]) if os.path.exists(threats_path) else pd.DataFrame()
    assets = pd.read_csv(assets_path) if os.path.exists(assets_path) else pd.DataFrame()
    return threats, assets


def severity_to_score(s):
    mapping = {"Low": 1, "Medium": 2, "High": 3, "Critical": 4}
    return mapping.get(s, np.nan)


# ---------------------------
# Load data
# ---------------------------
threats, assets = load_data()
if threats.empty:
    st.error("Threat dataset not found. Please place CSV in ./data/threats_sample.csv")
    st.stop()

# ---------------------------
# Sidebar - Navigation
# ---------------------------
sections = [
    "🏦 Introduction",
    "👥 Stakeholders & User Stories",
    "🎯 CTI Use Case",
    "🛡️ Threats & Critical Assets",
    "💎 Diamond Models",
    "📊 Dashboard"
]
section = st.sidebar.radio("Navigate", sections)

# Global filters (available to multiple sections where relevant)
with st.sidebar:
    st.markdown("### Global Filters")
    cats = sorted(threats["category"].dropna().unique().tolist())
    regs = sorted(threats["region"].dropna().unique().tolist())
    sevs = ["Low", "Medium", "High", "Critical"]

    f_cat = st.multiselect("Category", ["(All)"] + cats, default=["(All)"])
    f_reg = st.multiselect("Region", ["(All)"] + regs, default=["(All)"])
    f_sev = st.multiselect("Severity", ["(All)"] + sevs, default=["(All)"])

    min_d, max_d = threats["date"].min(), threats["date"].max()
    f_dates = st.slider("Date range", value=(min_d, max_d), min_value=min_d, max_value=max_d)


def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if "(All)" not in f_cat:
        df = df[df["category"].isin(f_cat)]
    if "(All)" not in f_reg:
        df = df[df["region"].isin(f_reg)]
    if "(All)" not in f_sev:
        df = df[df["severity"].isin(f_sev)]
    df = df[(df["date"] >= pd.to_datetime(f_dates[0])) & (df["date"] <= pd.to_datetime(f_dates[1]))]
    return df


filtered = apply_filters(threats)

# ---------------------------
# Section: Introduction
# ---------------------------
if section == "🏦 Introduction":
    st.title("Banking Sector CTI Dashboard")
    st.subheader("Industry Background")

    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(
            """
            **Key services** include retail/commercial banking, deposits, lending, payments, wealth, and digital channels.
            Banks are also expanding into embedded finance and tokenized digital assets.  
            *See:* [Wipfli 2026](https://www.wipfli.com/insights/research/state-of-the-banking-industry-2026).

            Between **2019–2024**, funds intermediated by the global banking system grew by **$122T (~40%)** and industry
            revenues reached **$5.5T in 2024** with net income **$1.2T** — a historic high.  
            *Source:* [McKinsey Global Banking Annual Review 2025](https://www.mckinsey.com/industries/financial-services/our-insights/global-banking-annual-review).

            The **2026 outlook** is broadly *stable* with resilient asset quality and solid liquidity, while banks continue to
            invest in AI, data, and digital assets.  
            *See:* [Moody's 2026 Outlook](https://www.moodys.com/web/en/us/insights/credit-risk/outlooks/banking-2026.html),
            [IBM IBV 2026](https://www.ibm.com/thought-leadership/institute-business-value/en-us/report/2026-banking-financial-markets-outlook).
            """
        )
    with col2:
        st.info("""**Tip**: Use the sidebar to filter threats by category, region, severity, and date
for context-aware metrics and charts.""")

    st.markdown(
        """
        **Why IT matters**: AI and data modernization are top priorities; fraud and cyber threats are intensifying.
        *See:* [KPMG 2026 Banking Trends](https://kpmg.com/us/en/articles/2026/banking-trends.html),
        [Deloitte 2026 Outlook](https://www.deloitte.com/us/en/insights/industry/financial-services/financial-services-industry-outlooks/banking-industry-outlook.html).
        """
    )

# ---------------------------
# Section: Stakeholders & User Stories
# ---------------------------
elif section == "👥 Stakeholders & User Stories":
    st.header("Stakeholders & User Stories")
    st.markdown("""
    **Persona 1 – SOC Analyst ("Jordan")**  
    - As a SOC analyst, I want to view real-time threat trends to prioritize investigations.  
    - As a SOC analyst, I want a filtered list of high-risk assets to focus monitoring efforts.

    **Persona 2 – CISO ("Alicia")**  
    - As a CISO, I want KPI summaries (threat volume, exposure) to align cyber budgets with risk.  
    - As a CISO, I want adversary capability views to support strategic planning.

    **Persona 3 – CTI Analyst ("Rahul")**  
    - As a CTI analyst, I want adversary profiles and diamond models for leadership briefings.  
    - As a CTI analyst, I want dashboards that update by threat category to identify patterns.

    *These user stories are addressed in the **Dashboard** and **Diamond Models** sections.*
    """)

# ---------------------------
# Section: CTI Use Case
# ---------------------------
elif section == "🎯 CTI Use Case":
    st.header("CTI Use Case – Threat-Model-Backed Design")
    st.markdown(
        """
        **Problem**: Banks report cybersecurity (including fraud) as the top concern for the third consecutive year; **81%** experienced a cyber incident last year.  
        *Source:* [Wipfli 2026](https://www.wipfli.com/insights/research/state-of-the-banking-industry-2026).

        **Decisions enabled**:  
        - Identify critical assets & associated threats  
        - Prioritize risks based on attacker behavior  
        - Brief leadership with adversary capability & infrastructure views  
        - Support investment decisions for AI-enabled defense and data modernization  

        **Why these analytics**: Fraud and financial crime risks are escalating with AI; fragmented data infrastructures hinder defenses.  
        *See:* [Deloitte 2026](https://www.deloitte.com/us/en/insights/industry/financial-services/financial-services-industry-outlooks/banking-industry-outlook.html),
        [KPMG 2026 Trends](https://kpmg.com/us/en/articles/2026/banking-trends.html).
        """
    )

# ---------------------------
# Section: Threats & Critical Assets
# ---------------------------
elif section == "🛡️ Threats & Critical Assets":
    st.header("Threat Trends & Critical Asset Identification")

    # KPIs quick glance (uses filtered)
    f = filtered.assign(sev_score=filtered["severity"].map(severity_to_score))
    total_threats = len(f)
    hi_pct = (f["sev_score"].ge(3).mean() * 100) if total_threats else 0
    est_loss = f["loss_usd_thousands"].sum()
    impacted_assets = f["asset"].nunique()

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Total Threats", f"{total_threats}")
    kpi2.metric("High/Critical %", f"{hi_pct:.1f}%")
    kpi3.metric("Est. Loss ($K)", f"{est_loss:,.0f}")
    kpi4.metric("Assets Impacted", f"{impacted_assets}")

    st.subheader("Top Threat Categories (filtered)")
    top_cat = f.groupby("category").size().reset_index(name="count").sort_values("count", ascending=False)
    chart = alt.Chart(top_cat).mark_bar(color="#1f77b4").encode(
        x=alt.X("count:Q", title="Incidents"),
        y=alt.Y("category:N", sort='-x', title="Category")
    ).properties(height=300)
    st.altair_chart(chart, use_container_width=True)

    st.subheader("Critical Assets (sample)")
    if not assets.empty:
        st.dataframe(assets, use_container_width=True)
    else:
        st.info("No assets dataset found.")

# ---------------------------
# Section: Diamond Models
# ---------------------------
elif section == "💎 Diamond Models":
    st.header("Diamond Models – Banking Threat Scenarios")

    with st.expander("Model 1 – AI-Enabled Financial Fraud Group"):
        st.markdown(
            """
            **Adversary**: Organized cybercrime group specializing in AI-assisted fraud and account takeover.  
            **Capabilities**: AI-generated phishing, credential stuffing, deepfake voice for high-value transfers.  
            **Infrastructure**: Botnets, anonymized proxies, compromised servers; dark‑web toolkits.  
            **Victim**: Banking customers via mobile channels; assets include IAM, digital channels, payment rails.  
            *Refs*: [Deloitte 2026](https://www.deloitte.com/us/en/insights/industry/financial-services/financial-services-industry-outlooks/banking-industry-outlook.html).
            """
        )

    with st.expander("Model 2 – Nation-State Actor Targeting Tokenized Assets"):
        st.markdown(
            """
            **Adversary**: Nation‑state team aiming to disrupt tokenized financial markets.  
            **Capabilities**: Cryptographic exploitation, API abuse, supply chain compromise.  
            **Infrastructure**: Covert cloud infra, C2, potential zero-days; blockchain analytics.  
            **Victim**: Banks adopting tokenized asset platforms; susceptible via legacy integration gaps.  
            *Refs*: [IBM IBV 2026](https://www.ibm.com/thought-leadership/institute-business-value/en-us/report/2026-banking-financial-markets-outlook).
            """
        )

# ---------------------------
# Section: Dashboard
# ---------------------------
elif section == "📊 Dashboard":
    st.header("CTI Dashboard – Interactive")

    # Additional local filters inside the section
    lcol1, lcol2, lcol3 = st.columns(3)
    with lcol1:
        actor_f = st.multiselect("Actor Type", ["(All)"] + sorted(threats["actor_type"].unique().tolist()), default=["(All)"])
    with lcol2:
        asset_f = st.multiselect("Asset", ["(All)"] + sorted(threats["asset"].unique().tolist()), default=["(All)"])
    with lcol3:
        status_f = st.multiselect("Status", ["(All)"] + sorted(threats["status"].unique().tolist()), default=["(All)"])

    df = filtered.copy()
    if "(All)" not in actor_f:
        df = df[df["actor_type"].isin(actor_f)]
    if "(All)" not in asset_f:
        df = df[df["asset"].isin(asset_f)]
    if "(All)" not in status_f:
        df = df[df["status"].isin(status_f)]

    # KPIs
    df = df.assign(sev_score=df["severity"].map(severity_to_score))
    total = len(df)
    highcrit = (df["sev_score"].ge(3).sum())
    highcrit_pct = (highcrit / total * 100) if total else 0
    loss_sum = df["loss_usd_thousands"].sum()
    uniq_assets = df["asset"].nunique()

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total Threats", f"{total}")
    k2.metric("High/Critical %", f"{highcrit_pct:.1f}%")
    k3.metric("Est. Loss ($K)", f"{loss_sum:,.0f}")
    k4.metric("Assets Impacted", f"{uniq_assets}")

    # Time series chart
    ts = df.set_index("date").resample("W").size().reset_index(name="incidents")
    ts_chart = alt.Chart(ts).mark_area(line={"color":"#1f77b4"}, color=alt.Gradient(
        gradient='linear', stops=[alt.GradientStop(color='#1f77b4', offset=0), alt.GradientStop(color='white', offset=1)], x1=1, x2=1, y1=1, y2=0)
    ).encode(
        x=alt.X("date:T", title="Week"),
        y=alt.Y("incidents:Q", title="Incidents per week")
    ).properties(height=250)

    st.altair_chart(ts_chart, use_container_width=True)

    # Bar by category
    by_cat = df.groupby("category").size().reset_index(name="count").sort_values("count", ascending=False)
    bar = alt.Chart(by_cat).mark_bar(color="#f28e2b").encode(
        x=alt.X("category:N", sort='-y', title="Category"),
        y=alt.Y("count:Q", title="Incidents")
    ).properties(height=300)
    st.altair_chart(bar, use_container_width=True)

    # Table
    st.subheader("Threat List (filtered)")
    st.dataframe(df.sort_values("date", ascending=False), use_container_width=True)

    # Download filtered CSV
    csv_bytes = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download filtered CSV", csv_bytes, file_name="threats_filtered.csv", mime="text/csv")

# Footer
st.caption("Data shown is synthetic and for educational purposes only. Citations: McKinsey 2025; Wipfli 2026; Deloitte 2026; IBM IBV 2026; KPMG 2026; Moody's 2026.")
