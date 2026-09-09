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

    /* -------------------------------------------------------
       GLOBAL
    ------------------------------------------------------- */

    .stApp {
        background:
            radial-gradient(
                circle at 15% 10%,
                rgba(37, 99, 235, 0.10),
                transparent 28%
            ),
            radial-gradient(
                circle at 85% 20%,
                rgba(16, 185, 129, 0.06),
                transparent 25%
            ),
            #080B12;
    }

    .block-container {
        max-width: 1050px;
        padding-top: 2.5rem;
        padding-bottom: 4rem;
    }


    /* -------------------------------------------------------
       REMOVE DEFAULT STREAMLIT FEEL
       ------------------------------------------------------- */

    header[data-testid="stHeader"] {
        background: transparent;
    }

    div[data-testid="stToolbar"] {
        visibility: hidden;
    }


    /* -------------------------------------------------------
       HERO
       ------------------------------------------------------- */

    .hero {
        text-align: center;
        padding: 25px 10px 10px 10px;
    }

    .hero-icon {
        font-size: 3.2rem;
        margin-bottom: 5px;
    }

    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        letter-spacing: -1.5px;
        color: #F8FAFC;
        margin-bottom: 5px;
    }

    .hero-subtitle {
        color: #94A3B8;
        font-size: 1.05rem;
        margin-bottom: 18px;
    }

    .status-pill {
        display: inline-block;
        padding: 6px 13px;
        border-radius: 999px;
        background: rgba(16, 185, 129, 0.10);
        border: 1px solid rgba(16, 185, 129, 0.25);
        color: #34D399;
        font-size: 0.82rem;
        font-weight: 600;
    }


    /* -------------------------------------------------------
       SECTION HEADERS
       ------------------------------------------------------- */

    .section-title {
        color: #F8FAFC;
        font-size: 1.35rem;
        font-weight: 700;
        margin-top: 10px;
        margin-bottom: 5px;
    }

    .section-description {
        color: #64748B;
        font-size: 0.9rem;
        margin-bottom: 15px;
    }


    /* -------------------------------------------------------
       INPUT AREA
       ------------------------------------------------------- */

    div[data-testid="stTextArea"] textarea {
        background-color: #11151F !important;
        border: 1px solid #263044 !important;
        border-radius: 12px !important;
        color: #E2E8F0 !important;
        font-size: 0.95rem !important;
        padding: 16px !important;
    }

    div[data-testid="stTextArea"] textarea:focus {
        border: 1px solid #3B82F6 !important;
        box-shadow: 0 0 0 1px #3B82F6 !important;
    }


    /* -------------------------------------------------------
       ANALYZE BUTTON
       ------------------------------------------------------- */

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
        color: white;
        font-size: 1rem;
        font-weight: 700;
        transition: 0.2s ease;
        box-shadow: 0 8px 25px rgba(37, 99, 235, 0.18);
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        border-color: #60A5FA;
        box-shadow: 0 12px 30px rgba(37, 99, 235, 0.28);
    }


    /* -------------------------------------------------------
       RESULT CARDS
       ------------------------------------------------------- */

    .result-card {
        background: linear-gradient(
            145deg,
            #11151F,
            #0D1119
        );
        border: 1px solid #202A3A;
        border-radius: 14px;
        padding: 22px;
        height: 100%;
    }

    .result-label {
        color: #64748B;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        margin-bottom: 8px;
    }

    .result-value {
        color: #F8FAFC;
        font-size: 2rem;
        font-weight: 800;
    }


    /* -------------------------------------------------------
       RISK BADGES
       ------------------------------------------------------- */

    .risk-high {
        color: #F87171;
    }

    .risk-medium {
        color: #FBBF24;
    }

    .risk-low {
        color: #34D399;
    }


    /* -------------------------------------------------------
       CONFIDENCE BAR
       ------------------------------------------------------- */

    .confidence-track {
        width: 100%;
        height: 8px;
        background: #1E293B;
        border-radius: 999px;
        overflow: hidden;
        margin-top: 12px;
    }

    .confidence-fill {
        height: 100%;
        background: linear-gradient(
            90deg,
            #2563EB,
            #60A5FA
        );
        border-radius: 999px;
    }


    /* -------------------------------------------------------
       INDICATOR CARDS
       ------------------------------------------------------- */

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
        font-size: 0.93rem;
    }

    .indicator-icon {
        font-size: 1rem;
    }


    /* -------------------------------------------------------
       RECOMMENDATION CARDS
       ------------------------------------------------------- */

    .action-card {
        border-radius: 12px;
        padding: 18px 20px;
        margin-top: 8px;
        font-size: 0.95rem;
        line-height: 1.6;
    }

    .action-high {
        background: rgba(239, 68, 68, 0.08);
        border: 1px solid rgba(239, 68, 68, 0.25);
        color: #FCA5A5;
    }

    .action-medium {
        background: rgba(245, 158, 11, 0.08);
        border: 1px solid rgba(245, 158, 11, 0.25);
        color: #FCD34D;
    }

    .action-low {
        background: rgba(16, 185, 129, 0.08);
        border: 1px solid rgba(16, 185, 129, 0.25);
        color: #6EE7B7;
    }


    /* -------------------------------------------------------
       FOOTER
       ------------------------------------------------------- */

    .footer {
        text-align: center;
        color: #475569;
        font-size: 0.78rem;
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
    """
    <div class="hero">

        <div class="hero-icon">🛡️</div>

        <div class="hero-title">
            Safety Risk Analyzer
        </div>

        <div class="hero-subtitle">
            AI-Powered Operational Safety Intelligence
        </div>

        <div class="status-pill">
            ● ML MODEL ONLINE
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


st.markdown(
    """
    <div style="
        text-align:center;
        color:#94A3B8;
        font-size:0.95rem;
        max-width:760px;
        margin:15px auto 30px auto;
        line-height:1.6;
    ">
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
    """
    <div class="section-title">
        Safety Report Input
    </div>

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
    # Empty input
    # --------------------------------------------------------

    if not report.strip():

        st.warning(
            "Please enter a safety report before running the analysis."
        )


    else:

        # ----------------------------------------------------
        # Run backend
        # ----------------------------------------------------

        with st.spinner(
            "Analyzing report with ML model..."
        ):

            result = analyze_report(report)


        # ====================================================
        # GATE 1 — NOT A SAFETY REPORT
        # ====================================================

        if not result.get(
            "is_safety_report",
            True
        ):

            st.divider()

            st.markdown(
                """
                <div class="action-card action-medium">

                <strong>⚠️ Safety Report Not Detected</strong>
                <br><br>

                The submitted text does not appear to describe
                an operational safety condition.

                </div>
                """,
                unsafe_allow_html=True,
            )

            st.info(
                result.get(
                    "recommendation",
                    "Please enter an operational safety report."
                )
            )


        # ====================================================
        # GATE 2 — INSUFFICIENT INFORMATION
        # ====================================================

        elif result.get(
            "insufficient_information",
            False
        ):

            st.divider()

            st.markdown(
                """
                <div class="action-card action-medium">

                <strong>⚠️ Insufficient Information</strong>
                <br><br>

                The report appears to be safety-related, but
                there is not enough information to confidently
                assess the risk level.

                </div>
                """,
                unsafe_allow_html=True,
            )

            st.info(
                result.get(
                    "recommendation",
                    "Please provide more details about the hazard."
                )
            )


        # ====================================================
        # VALID SAFETY REPORT
        # ====================================================

        else:

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


            st.divider()


            # =================================================
            # RESULT OVERVIEW
            # =================================================

            st.markdown(
                """
                <div class="section-title">
                    Risk Assessment
                </div>

                <div class="section-description">
                    Machine-learning assessment generated from
                    the submitted safety report.
                </div>
                """,
                unsafe_allow_html=True,
            )


            col1, col2 = st.columns(
                2,
                gap="medium"
            )


            # -------------------------------------------------
            # Risk card
            # -------------------------------------------------

            if risk == "HIGH":

                risk_icon = "🚨"
                risk_class = "risk-high"

            elif risk == "MEDIUM":

                risk_icon = "⚠️"
                risk_class = "risk-medium"

            else:

                risk_icon = "✅"
                risk_class = "risk-low"


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
            # Confidence card
            # -------------------------------------------------

            with col2:

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
                                style="width:{min(confidence, 100)}%;"
                            ></div>

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
                """
                <div class="section-title">
                    Recommended Action
                </div>
                """,
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
                """
                <div class="section-title">
                    Key Risk Indicators Identified
                </div>

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
        Designed for proactive operational safety assessment
    </div>
    """,
    unsafe_allow_html=True,
)