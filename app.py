import streamlit as st
from predict import analyze_report


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Safety Risk Analyzer",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
<style>

/* =========================
   MAIN APP
   ========================= */

.stApp {
    background:
        radial-gradient(
            circle at 8% 5%,
            rgba(56, 189, 248, 0.10),
            transparent 30%
        ),
        radial-gradient(
            circle at 92% 15%,
            rgba(14, 165, 233, 0.07),
            transparent 28%
        ),
        #070B12;
}

.block-container {
    max-width: 1050px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}


/* =========================
   HERO
   ========================= */

.hero-icon {
    text-align: center;
    font-size: 3.5rem;
    margin-bottom: 5px;
}

.hero-title {
    text-align: center;
    font-size: 3rem;
    font-weight: 800;
    letter-spacing: -1px;
    color: #F8FAFC;
    margin-bottom: 5px;
}

.hero-subtitle {
    text-align: center;
    color: #7DD3FC;
    font-size: 1.05rem;
    font-weight: 600;
    margin-bottom: 15px;
}

.hero-description {
    text-align: center;
    color: #94A3B8;
    font-size: 0.92rem;
    line-height: 1.7;
    max-width: 780px;
    margin: 0 auto 20px auto;
}

.status-container {
    text-align: center;
    margin-bottom: 25px;
}

.status-pill {
    display: inline-block;
    padding: 7px 15px;
    border-radius: 999px;
    background: rgba(34, 211, 238, 0.08);
    border: 1px solid rgba(34, 211, 238, 0.28);
    color: #67E8F9;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.7px;
}


/* =========================
   SECTION TITLES
   ========================= */

.section-title {
    color: #F8FAFC;
    font-size: 1.35rem;
    font-weight: 750;
    margin-bottom: 5px;
}

.section-description {
    color: #64748B;
    font-size: 0.88rem;
    margin-bottom: 15px;
}


/* =========================
   TEXT AREA
   ========================= */

div[data-testid="stTextArea"] textarea {
    background-color: #0E141F !important;
    border: 1px solid #26364A !important;
    border-radius: 12px !important;
    color: #E2E8F0 !important;
    font-size: 0.95rem !important;
    padding: 16px !important;
    line-height: 1.6 !important;
}

div[data-testid="stTextArea"] textarea:focus {
    border-color: #38BDF8 !important;
    box-shadow:
        0 0 0 1px #38BDF8,
        0 0 18px rgba(56, 189, 248, 0.10) !important;
}

div[data-testid="stTextArea"] textarea::placeholder {
    color: #64748B !important;
}


/* =========================
   BUTTON
   ========================= */

.stButton > button {
    width: 100%;
    height: 54px;

    border-radius: 11px;

    border: 1px solid #38BDF8;

    background:
        linear-gradient(
            135deg,
            #0284C7,
            #0EA5E9
        );

    color: #FFFFFF;

    font-size: 1rem;
    font-weight: 700;

    box-shadow:
        0 8px 25px rgba(14, 165, 233, 0.16);

    transition: all 0.2s ease;
}

.stButton > button:hover {
    background:
        linear-gradient(
            135deg,
            #0EA5E9,
            #38BDF8
        );

    border-color: #7DD3FC;

    transform: translateY(-1px);

    box-shadow:
        0 12px 32px rgba(14, 165, 233, 0.28);
}


/* =========================
   RESULT CARDS
   ========================= */

.result-card {
    background:
        linear-gradient(
            145deg,
            #101722,
            #0B1018
        );

    border: 1px solid #1F2D3D;

    border-radius: 14px;

    padding: 22px;

    min-height: 120px;

    box-shadow:
        0 8px 30px rgba(0, 0, 0, 0.15);
}

.result-label {
    color: #64748B;

    font-size: 0.76rem;

    font-weight: 700;

    text-transform: uppercase;

    letter-spacing: 0.8px;

    margin-bottom: 10px;
}

.result-value {
    font-size: 2rem;
    font-weight: 800;
}

.high-risk {
    color: #F87171;
}

.medium-risk {
    color: #FBBF24;
}

.low-risk {
    color: #34D399;
}


/* =========================
   CONFIDENCE BAR
   ========================= */

.confidence-track {
    width: 100%;
    height: 7px;

    background: #1E293B;

    border-radius: 999px;

    overflow: hidden;

    margin-top: 14px;
}

.confidence-fill {
    height: 100%;

    border-radius: 999px;

    background:
        linear-gradient(
            90deg,
            #06B6D4,
            #38BDF8
        );
}


/* =========================
   INDICATORS
   ========================= */

.indicator-card {
    display: flex;

    align-items: center;

    gap: 12px;

    background: #0E141F;

    border: 1px solid #1F2D3D;

    border-left: 3px solid #38BDF8;

    border-radius: 10px;

    padding: 13px 16px;

    margin-bottom: 9px;

    color: #CBD5E1;

    font-size: 0.92rem;
}

.indicator-icon {
    color: #38BDF8;
}


/* =========================
   FOOTER
   ========================= */

.footer {
    text-align: center;

    color: #475569;

    font-size: 0.75rem;

    line-height: 1.6;

    margin-top: 45px;

    padding: 20px;
}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# HERO SECTION
# ============================================================

st.markdown(
    '<div class="hero-icon">🛡️</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="hero-title">Safety Risk Analyzer</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="hero-subtitle">AI-Powered Operational Safety Intelligence</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="status-container">'
    '<span class="status-pill">● ML MODEL ONLINE</span>'
    '</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="hero-description">'
    'Analyze operational safety reports and identify potential risks, '
    'key indicators, and recommended actions before they escalate '
    'into incidents.'
    '</div>',
    unsafe_allow_html=True,
)

st.divider()


# ============================================================
# INPUT SECTION
# ============================================================

st.markdown(
    '<div class="section-title">Safety Report Input</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-description">'
    'Provide an operational safety observation, incident report, '
    'or workplace hazard description.'
    '</div>',
    unsafe_allow_html=True,
)

report = st.text_area(
    "Safety report",
    height=180,
    label_visibility="collapsed",
    placeholder=(
        "Example: During the night shift at Plant B, a high-pressure "
        "valve on Line 3 began leaking hydraulic fluid near an exposed "
        "power conduit..."
    ),
)

analyze_clicked = st.button(
    "⚡  Run Risk Analysis",
    use_container_width=True,
)


# ============================================================
# ANALYSIS
# ============================================================

if analyze_clicked:

    # --------------------------------------------------------
    # EMPTY INPUT
    # --------------------------------------------------------

    if not report.strip():

        st.warning(
            "Please enter a safety report before running the analysis."
        )

    else:

        # ----------------------------------------------------
        # SAFETY CONTEXT CHECK
        # ----------------------------------------------------

        safety_keywords = [
            "machine",
            "machines",
            "equipment",
            "worker",
            "workers",
            "employee",
            "employees",
            "hazard",
            "hazards",
            "danger",
            "risk",
            "safety",
            "fire",
            "smoke",
            "chemical",
            "chemicals",
            "leak",
            "leaking",
            "spill",
            "injury",
            "injured",
            "accident",
            "maintenance",
            "warning",
            "pressure",
            "vibration",
            "electrical",
            "electric",
            "wire",
            "wires",
            "voltage",
            "helmet",
            "ppe",
            "protective",
            "unsafe",
            "emergency",
            "factory",
            "plant",
            "inspection",
            "slip",
            "slipping",
            "fall",
            "fallen",
            "exposure",
            "exposed",
            "ventilation",
            "conduit",
            "valve",
            "boiler",
            "conveyor",
            "motor",
            "pump",
            "gas",
            "toxic",
            "corrosion",
            "hazardous",
        ]

        report_lower = report.lower()

        is_safety_related = any(
            keyword in report_lower
            for keyword in safety_keywords
        )


        # ====================================================
        # NON-SAFETY INPUT
        # ====================================================

        if not is_safety_related:

            st.divider()

            st.markdown(
                '<div class="section-title">Analysis Result</div>',
                unsafe_allow_html=True,
            )

            st.warning(
                "⚠️ Safety Report Not Detected"
            )

            st.info(
                "The submitted text does not appear to describe "
                "an operational safety condition."
            )

            st.caption(
                "Please provide a report describing a workplace hazard, "
                "equipment condition, incident, environmental risk, "
                "or safety observation."
            )


        # ====================================================
        # ML ANALYSIS
        # ====================================================

        else:

            with st.spinner(
                "Analyzing report with ML model..."
            ):

                try:

                    result = analyze_report(report)

                except Exception as error:

                    st.error(
                        "The risk analysis could not be completed."
                    )

                    st.caption(
                        f"Backend error: {error}"
                    )

                    st.stop()


            # =================================================
            # SAFE RESULT EXTRACTION
            # =================================================

            risk = str(
                result.get("risk") or "UNKNOWN"
            ).upper()

            try:

                confidence = float(
                    result.get("confidence") or 0
                )

            except (TypeError, ValueError):

                confidence = 0.0

            indicators = result.get("indicators") or []

            recommendation = str(
                result.get("recommendation")
                or "Further safety assessment is recommended."
            )


            # =================================================
            # RISK STYLING
            # =================================================

            if risk == "HIGH":

                risk_icon = "🚨"
                risk_class = "high-risk"

            elif risk == "MEDIUM":

                risk_icon = "⚠️"
                risk_class = "medium-risk"

            elif risk == "LOW":

                risk_icon = "✅"
                risk_class = "low-risk"

            else:

                risk_icon = "🔍"
                risk_class = ""


            # =================================================
            # RESULT HEADER
            # =================================================

            st.divider()

            st.markdown(
                '<div class="section-title">Risk Assessment</div>',
                unsafe_allow_html=True,
            )

            st.markdown(
                '<div class="section-description">'
                'Machine-learning assessment generated from '
                'the submitted safety report.'
                '</div>',
                unsafe_allow_html=True,
            )


            # =================================================
            # RESULT CARDS
            # =================================================

            col1, col2 = st.columns(2)


            # -------------------------------------------------
            # RISK LEVEL
            # -------------------------------------------------

            with col1:

                st.markdown(
                    f"""
<div class="result-card">
<div class="result-label">Assessed Risk Level</div>
<div class="result-value {risk_class}">
{risk_icon} {risk}
</div>
</div>
""",
                    unsafe_allow_html=True,
                )


            # -------------------------------------------------
            # CONFIDENCE
            # -------------------------------------------------

            with col2:

                confidence_width = min(
                    max(confidence, 0),
                    100
                )

                st.markdown(
                    f"""
<div class="result-card">
<div class="result-label">Model Confidence</div>
<div class="result-value">{confidence:.2f}%</div>
<div class="confidence-track">
<div class="confidence-fill" style="width:{confidence_width}%"></div>
</div>
</div>
""",
                    unsafe_allow_html=True,
                )


            st.write("")


            # =================================================
            # RECOMMENDED ACTION
            # =================================================

            st.markdown(
                '<div class="section-title">Recommended Action</div>',
                unsafe_allow_html=True,
            )


            if risk == "HIGH":

                st.error(
                    f"🚨 **Action Required:** {recommendation}"
                )

            elif risk == "MEDIUM":

                st.warning(
                    f"⚠️ **Action Required:** {recommendation}"
                )

            elif risk == "LOW":

                st.success(
                    f"✅ **Action Required:** {recommendation}"
                )

            else:

                st.info(
                    f"🔍 **Recommendation:** {recommendation}"
                )


            st.write("")


            # =================================================
            # KEY INDICATORS
            # =================================================

            st.markdown(
                '<div class="section-title">'
                'Key Risk Indicators Identified'
                '</div>',
                unsafe_allow_html=True,
            )

            st.markdown(
                '<div class="section-description">'
                'Safety-related signals detected in the report.'
                '</div>',
                unsafe_allow_html=True,
            )


            if indicators:

                for item in indicators:

                    # Escape basic HTML-sensitive characters
                    safe_item = (
                        str(item)
                        .replace("&", "&amp;")
                        .replace("<", "&lt;")
                        .replace(">", "&gt;")
                    )

                    st.markdown(
                        f'<div class="indicator-card">'
                        f'<span class="indicator-icon">🔍</span>'
                        f'<span>{safe_item}</span>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )

            else:

                st.info(
                    "No specific risk indicators were detected."
                )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    '<div class="footer">'
    '🛡️ Safety Risk Analyzer'
    '<br>'
    'Machine Learning Powered • Proactive Safety Assessment'
    '</div>',
    unsafe_allow_html=True,
)