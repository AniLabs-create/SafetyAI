import streamlit as st
from predict import analyze_report

# --------------------------------------------------
# Page configuration & Custom Styling
# --------------------------------------------------
st.set_page_config(
    page_title="Safety Risk Analyzer",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Custom CSS for a refined UI
st.markdown(
    """
    <style>
    /* Main container tweaks */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1000px;
    }
    
    /* Subtle background accent for metrics */
    [data-testid="stMetricValue"] {
        font-size: 1.8rem !important;
        font-weight: 700;
    }
    
    /* Primary Action Button styling */
    .stButton>button {
        width: 100%;
        background-color: #0F172A;
        color: #FFFFFF;
        border-radius: 8px;
        padding: 0.6rem 1rem;
        font-weight: 600;
        border: none;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background-color: #1E293B;
        color: #FFFFFF;
        border-color: transparent;
    }

    /* Custom card styles */
    .indicator-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-left: 4px solid #3B82F6;
        border-radius: 6px;
        padding: 12px 16px;
        margin-bottom: 8px;
        font-size: 0.95rem;
        color: #334155;
    }
    
    /* Dark mode support for custom card */
    @media (prefers-color-scheme: dark) {
        .indicator-card {
            background-color: #1E293B;
            border-color: #334155;
            border-left: 4px solid #3B82F6;
            color: #E2E8F0;
        }
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Dynamic color mapping for risk levels
RISK_STYLES = {
    "HIGH": {"color": "red", "icon": "🚨"},
    "MEDIUM": {"color": "orange", "icon": "⚠️"},
    "LOW": {"color": "green", "icon": "✅"},
}

# --------------------------------------------------
# Header Section
# --------------------------------------------------
st.title("🛡️ Safety Risk Analyzer")
st.caption("AI-Powered Operational Safety Intelligence")

st.markdown(
    "Analyze operational safety reports in real time to proactively identify "
    "potential risks and actionable indicators before they escalate into incidents."
)

st.divider()

# --------------------------------------------------
# Input Section
# --------------------------------------------------
st.subheader("Safety Report Input")
report = st.text_area(
    "Enter or paste the operational safety report below:",
    height=180,
    placeholder="e.g., During the night shift at Plant B, a high-pressure valve on Line 3 began leaking hydraulic fluid near an exposed power conduit...",
)

analyze_clicked = st.button("Run Risk Analysis", use_container_width=True)

# --------------------------------------------------
# Analysis & Output Section
# --------------------------------------------------
if analyze_clicked:
    if not report.strip():
        st.warning("Please enter a safety report before running the analysis.")
    else:
        with st.spinner("Analyzing safety report with ML model..."):
            result = analyze_report(report)

            risk = result.get("risk", "UNKNOWN").upper()
            confidence = result.get("confidence", 0)
            indicators = result.get("indicators", [])
            recommendation = result.get("recommendation", "N/A")

        st.divider()

        # Risk overview metrics
        style_info = RISK_STYLES.get(
            risk, {"color": "gray", "icon": "🔍"}
        )

        col1, col2 = st.columns([1, 1])

        with col1:
            st.metric(
                label="Assessed Risk Level",
                value=f"{style_info['icon']} {risk}",
            )

        with col2:
            st.metric(
                label="Model Confidence",
                value=f"{confidence}%",
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # Recommended action container
        st.subheader("Recommended Action")
        if risk == "HIGH":
            st.error(f"**Action Required:** {recommendation}", icon="🚨")
        elif risk == "MEDIUM":
            st.warning(f"**Action Required:** {recommendation}", icon="⚠️")
        else:
            st.success(f"**Action Required:** {recommendation}", icon="✅")

        st.markdown("<br>", unsafe_allow_html=True)

        # Key indicators list
        st.subheader("Key Risk Indicators Identified")
        if indicators:
            for item in indicators:
                st.markdown(
                    f'<div class="indicator-card">🔍 {item}</div>',
                    unsafe_allow_html=True,
                )
        else:
            st.info("No critical indicators detected in this report.")