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

    /* ======================================================
       GLOBAL
       ====================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 10% 5%,
                rgba(37, 99, 235, 0.10),
                transparent 28%
            ),
            radial-gradient(
                circle at 90% 15%,
                rgba(16, 185, 129, 0.05),
                transparent 25%
            ),
            #080B12;
    }

    .block-container {
        max-width: 1050px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    header[data-testid="stHeader"] {
        background: transparent;
    }


    /* ======================================================
       HERO
       ====================================================== */

    .hero-title {
        text-align: center;
        font-size: 3.1rem;
        font-weight: 800;
        letter-spacing: -1.5px;
        color: #F8FAFC;
        margin-top: 0.2rem;
        margin-bottom: 0.2rem;
    }

    .hero-subtitle {
        text-align: center;
        color: #94A3B8;
        font-size: 1.05rem;
        margin-bottom: 1rem;
    }

    .hero-description {
        text-align: center;
        color: #64748B;
        font-size: 0.92rem;
        line-height: 1.7;
        max-width: 760px;
        margin-left: auto;
        margin-right: auto;
        margin-bottom: 1.8rem;
    }

    .status-container {
        text-align: center;
        margin-bottom: 1.5rem;
    }

    .status-pill {
        display: inline-block;
        padding: 6px 14px;
        border-radius: 999px;
        background: rgba(16, 185, 129, 0.08);
        border: 1px solid rgba(16, 185, 129, 0.25);
        color: #34D399;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.4px;
    }


    /* ======================================================
       SECTION TITLES
       ====================================================== */

    .section-title {
        color: #F8FAFC;
        font-size: 1.35rem;
        font-weight: 750;
        margin-bottom: 0.25rem;
    }

    .section-description {
        color: #64748B;
        font-size: 0.88rem;
        margin-bottom: 1rem;
    }


    /* ======================================================
       TEXT AREA
       ====================================================== */

    div[data-testid="stTextArea"] textarea {
        background-color: #11151F !important;
        border: 1px solid #263044 !important;
        border-radius: 12px !important;
        color: #E2E8F0 !important;
        font-size: 0.95rem !important;
        padding: 16px !important;
        line-height: 1.6 !important;
    }

    div[data-testid="stTextArea"] textarea:focus {
        border-color: #3B82F6 !important;
        box-shadow: 0 0 0 1px #3B82F6 !important;
    }


    /* ======================================================
       ANALYZE BUTTON
       ====================================================== */

    .stButton > button {
        width: 100%;
        height: 52px;
        border-radius: 10px;
        border: 1px solid #2563EB;
        background: linear-gradient(
            135deg,
            #2563EB,
            #1D4ED8
        );
        color: #FFFFFF;
        font-size: 1rem;
        font-weight: 700;
        transition: all 0.2s ease;
        box-shadow:
            0 8px 25px rgba(37, 99, 235, 0.18);
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        border-color: #60A5FA;
        box-shadow:
            0 12px 30px rgba(37, 99, 235, 0.30);
    }


    /* ======================================================
       RESULT CARDS
       ====================================================== */

    .result-card {
        background: linear-gradient(
            145deg,
            #11151F,
            #0D1119
        );
        border: 1px solid #202A3A;
        border-radius: 14px;
        padding: 22px;
        min-height: 125px;
    }

    .result-label {
        color: #64748B;
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.7px;
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


    /* ======================================================
       CONFIDENCE BAR
       ====================================================== */

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
        background: linear-gradient(
            90deg,
            #2563EB,
            #60A5FA
        );
    }


    /* ======================================================
       INDICATORS
       ====================================================== */

    .indicator-card {
        display: flex;
        align-items: center;
        gap: 12px;

        background: #11151F;

        border: 1px solid #202A3A;
        border-left: 3px solid #3B82F6;

        border-radius: 10px;

        padding: 13px 16px;

        margin-bottom: 9px;

        color: #CBD5E1;

        font-size: 0.92rem;
    }

    .indicator-icon {
        font-size: 0.95rem;
    }


    /* ======================================================
       ACTION CARDS
       ====================================================== */

    .action-card {
        border-radius: 12px;
        padding: 18px 20px;
        margin-top: 8px;

        font-size: 0.94rem;
        line-height: 1.6;
    }

    .action-high {
        background: rgba(239, 68, 68, 0.08);
        border: 1px solid rgba(239, 68, 68, 0.28);
        color: #FCA5A5;
    }

    .action-medium {
        background: rgba(245, 158, 11, 0.08);
        border: 1px solid rgba(245, 158, 11, 0.28);
        color: #FCD34D;
    }

    .action-low {
        background: rgba(16, 185, 129, 0.08);
        border: 1px solid rgba(16, 185, 129, 0.28);
        color: #6EE7B7;
    }


    /* ======================================================
       FOOTER
       ====================================================== */

    .footer {
        text-align: center;
        color: #475569;
        font-size: 0.75rem;
        line-height: 1.6;
        margin-top: 45px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HERO SECTION
# ============================================================

st.markdown(
    "<div style='text-align:center; font-size:3.2rem;'>🛡️</div>",
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="hero-title">Safety Risk Analyzer</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="hero-subtitle">'
    'AI-Powered Operational Safety Intelligence'
    '</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="status-container">
        <span class="status-pill">
            ● ML MODEL ONLINE
        </span>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero-description">
        Analyze operational safety reports and identify potential risks,
        key indicators, and recommended actions before they escalate
        into incidents.
    </div>
    """,
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
    """
    <div class="section-description">
        Provide an operational safety observation, incident report,
        or workplace hazard description.
    </div>
    """,
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
        # RUN ML BACKEND
        # ----------------------------------------------------

        with st.spinner(
            "Analyzing report with ML model..."
        ):

            result = analyze_report(report)


        # ====================================================
        # EXTRACT RESULT
        # ====================================================

        risk = result.get(
            "risk",
            "UNKNOWN"
        ).upper()

        confidence = float(
            result.get(
                "confidence",
                0
            )
        )

        indicators = result.get(
            "indicators",
            []
        )

        recommendation = result.get(
            "recommendation",
            "Further safety assessment is recommended."
        )


        # ====================================================
        # SIMPLE NON-SAFETY TEXT CHECK
        # ====================================================

        safety_keywords = [
            "machine",
            "equipment",
            "worker",
            "workers",
            "employee",
            "hazard",
            "danger",
            "risk",
            "safety",
            "fire",
            "smoke",
            "chemical",
            "leak",
            "spill",
            "injury",
            "accident",
            "maintenance",
            "warning",
            "pressure",
            "vibration",
            "electrical",
            "electric",
            "wire",
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
            "fall",
            "exposure",
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
        ]

        report_lower = report.lower()

        is_safety_related = any(
            keyword in report_lower
            for keyword in safety_keywords
        )


        # ====================================================
        # NON-SAFETY RESPONSE
        # ====================================================

        if not is_safety_related:

            st.divider()

            st.markdown(
                '<div class="section-title">'
                'Analysis Result'
                '</div>',
                unsafe_allow_html=True,
            )

            st.markdown(
                """
                <div class="action-card action-medium">

                    <strong>⚠️ Safety Report Not Detected</strong>

                    <br><br>

                    The submitted text does not appear to describe
                    an operational safety condition.

                    Please provide a report describing a workplace
                    hazard, equipment condition, incident,
                    environmental risk, or safety observation.

                </div>
                """,
                unsafe_allow_html=True,
            )


        # ====================================================
        # VALID SAFETY REPORT
        # ====================================================

        else:

            st.divider()

            st.markdown(
                '<div class="section-title">'
                'Risk Assessment'
                '</div>',
                unsafe_allow_html=True,
            )

            st.markdown(
                """
                <div class="section-description">
                    Machine-learning assessment generated from
                    the submitted safety report.
                </div>
                """,
                unsafe_allow_html=True,
            )


            # =================================================
            # RISK STYLE
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
            # RESULT CARDS
            # =================================================

            col1, col2 = st.columns(
                2,
                gap="medium"
            )


            # -------------------------------------------------
            # RISK CARD
            # -------------------------------------------------

            with col1:

                st.markdown(
                    f"""
                    <div class="result-card">

                        <div class="result-label">
                            Assessed Risk Level
                        </div>

                        <div class="result-value {risk_class}">
                            {risk_icon} {risk}
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True,
                )


            # -------------------------------------------------
            # CONFIDENCE CARD
            # -------------------------------------------------

            with col2:

                confidence_width = min(
                    max(confidence, 0),
                    100
                )

                st.markdown(
                    f"""
                    <div class="result-card">

                        <div class="result-label">
                            Model Confidence
                        </div>

                        <div class="result-value">
                            {confidence:.2f}%
                        </div>

                        <div class="confidence-track">

                            <div
                                class="confidence-fill"
                                style="width:{confidence_width}%;">
                            </div>

                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True,
                )


            st.markdown(
                "<br>",
                unsafe_allow_html=True
            )


            # =================================================
            # RECOMMENDED ACTION
            # =================================================

            st.markdown(
                '<div class="section-title">'
                'Recommended Action'
                '</div>',
                unsafe_allow_html=True,
            )


            if risk == "HIGH":

                action_class = "action-high"
                action_icon = "🚨"

            elif risk == "MEDIUM":

                action_class = "action-medium"
                action_icon = "⚠️"

            else:

                action_class = "action-low"
                action_icon = "✅"


            st.markdown(
                f"""
                <div class="action-card {action_class}">

                    <strong>
                        {action_icon} Action Required
                    </strong>

                    <br>

                    {recommendation}

                </div>
                """,
                unsafe_allow_html=True,
            )


            st.markdown(
                "<br>",
                unsafe_allow_html=True
            )


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
                """
                <div class="section-description">
                    Safety-related signals detected in the report.
                </div>
                """,
                unsafe_allow_html=True,
            )


            if indicators:

                for item in indicators:

                    st.markdown(
                        f"""
                        <div class="indicator-card">

                            <span class="indicator-icon">
                                🔍
                            </span>

                            <span>
                                {item}
                            </span>

                        </div>
                        """,
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
    """
    <div class="footer">
        Safety Risk Analyzer • Machine Learning Powered
        <br>
        Proactive operational safety assessment
    </div>
    """,
    unsafe_allow_html=True,
)