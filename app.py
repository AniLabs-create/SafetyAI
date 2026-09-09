import streamlit as st
import streamlit.components.v1 as components
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
# CURSOR GLOW EFFECT
# ============================================================
# Streamlit's st.markdown(unsafe_allow_html=True) inserts HTML via
# innerHTML, and browsers deliberately do NOT execute <script> tags
# added that way -- so a plain CSS injection can't do anything that
# needs live mouse tracking. components.html() renders inside an
# iframe where scripts DO run; from there we reach into
# window.parent.document (same-origin, so this is allowed) to attach
# the glow element and mousemove listener to the actual app page.
# The `if already exists, stop` guard matters because Streamlit
# re-runs this whole script on every interaction (button clicks,
# etc.) -- without it we'd stack up duplicate glow divs and duplicate
# mousemove listeners on every rerun.

components.html(
    """
<script>
(function() {
    const doc = window.parent.document;
    if (doc.getElementById('cursor-glow')) return;

    const style = doc.createElement('style');
    style.innerHTML = `
        #cursor-glow{
            position:fixed;top:0;left:0;width:420px;height:420px;border-radius:50%;
            background:radial-gradient(circle, rgba(56,189,248,0.32) 0%, rgba(56,189,248,0.11) 42%, transparent 70%);
            pointer-events:none;z-index:999999;transform:translate(-50%,-50%);
            will-change:transform;opacity:0;transition:opacity 0.4s ease;
            mix-blend-mode:screen;
        }
        #cursor-glow.visible{opacity:1;}
    `;
    doc.head.appendChild(style);

    const glow = doc.createElement('div');
    glow.id = 'cursor-glow';
    doc.body.appendChild(glow);

    let mouseX = window.parent.innerWidth / 2, mouseY = window.parent.innerHeight / 2;
    let glowX = mouseX, glowY = mouseY;
    let active = false;

    doc.addEventListener('mousemove', (e) => {
        mouseX = e.clientX; mouseY = e.clientY;
        if (!active) { active = true; glow.classList.add('visible'); }
    });
    doc.addEventListener('mouseleave', () => glow.classList.remove('visible'));

    function tick() {
        glowX += (mouseX - glowX) * 0.12;
        glowY += (mouseY - glowY) * 0.12;
        glow.style.transform = `translate(${glowX}px, ${glowY}px) translate(-50%, -50%)`;
        window.parent.requestAnimationFrame(tick);
    }
    tick();
})();
</script>
""",
    height=0,
    width=0,
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


/* =========================
   AMBIENT BACKGROUND ORBS
   ========================= */

.ambient-orb {
    position: fixed;
    border-radius: 50%;
    filter: blur(90px);
    pointer-events: none;
    z-index: 0;
    opacity: 0.55;
}

.orb-a {
    top: -120px;
    left: -100px;
    width: 420px;
    height: 420px;
    background: radial-gradient(circle, rgba(56,189,248,0.35), transparent 70%);
    animation: floatOrb 13s ease-in-out infinite;
}

.orb-b {
    bottom: -140px;
    right: -100px;
    width: 480px;
    height: 480px;
    background: radial-gradient(circle, rgba(14,165,233,0.28), transparent 70%);
    animation: floatOrb 16s ease-in-out infinite reverse;
}

@keyframes floatOrb {
    0%, 100% { transform: translate(0, 0) scale(1); }
    50% { transform: translate(30px, -35px) scale(1.08); }
}

.block-container { position: relative; z-index: 1; }


/* =========================
   ENTRANCE ANIMATIONS
   ========================= */

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0); }
}

.hero-icon       { animation: fadeInUp 0.6s ease both; }
.hero-title      { animation: fadeInUp 0.6s ease 0.08s both; }
.hero-subtitle   { animation: fadeInUp 0.6s ease 0.16s both; }
.status-container{ animation: fadeInUp 0.6s ease 0.24s both; }
.hero-description{ animation: fadeInUp 0.6s ease 0.32s both; }

.result-card, .indicator-card {
    animation: fadeInUp 0.5s ease both;
}


/* =========================
   BUTTON SHIMMER
   ========================= */

.stButton > button {
    position: relative;
    overflow: hidden;
}

.stButton > button::after {
    content: "";
    position: absolute;
    top: 0; left: 0;
    width: 60%; height: 100%;
    background: linear-gradient(120deg, transparent, rgba(255,255,255,0.35), transparent);
    transform: translateX(-160%) skewX(-15deg);
    transition: transform 0.6s ease;
}

.stButton > button:hover::after {
    transform: translateX(220%) skewX(-15deg);
}


/* =========================
   HIGH RISK PULSE
   ========================= */

@keyframes pulseRing {
    0%   { box-shadow: 0 0 0 0 rgba(248,113,113,0.45); }
    70%  { box-shadow: 0 0 0 16px rgba(248,113,113,0); }
    100% { box-shadow: 0 0 0 0 rgba(248,113,113,0); }
}

.pulse-ring {
    animation: pulseRing 1.8s ease-out infinite;
    border-radius: 14px;
}


/* =========================
   SCANNING LOADER
   ========================= */

.scan-loader {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 18px 22px;
    background: linear-gradient(145deg, #101722, #0B1018);
    border: 1px solid #1F2D3D;
    border-radius: 14px;
    margin: 10px 0 20px;
}

.scan-bar {
    position: relative;
    flex: 1;
    height: 6px;
    background: #1E293B;
    border-radius: 999px;
    overflow: hidden;
}

.scan-bar::after {
    content: "";
    position: absolute;
    top: 0; left: 0;
    height: 100%; width: 40%;
    background: linear-gradient(90deg, transparent, #38BDF8, transparent);
    animation: scanSweep 1.1s ease-in-out infinite;
}

@keyframes scanSweep {
    0%   { left: -40%; }
    100% { left: 100%; }
}

.scan-text {
    color: #7DD3FC;
    font-size: 0.85rem;
    font-weight: 600;
    white-space: nowrap;
}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# AMBIENT ORBS (decorative, no JS needed)
# ============================================================

st.markdown(
    '<div class="ambient-orb orb-a"></div><div class="ambient-orb orb-b"></div>',
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

            scan_placeholder = st.empty()
            scan_placeholder.markdown(
                '<div class="scan-loader">'
                '<div class="scan-bar"></div>'
                '<div class="scan-text">Scanning report for risk indicators…</div>'
                '</div>',
                unsafe_allow_html=True,
            )

            # A brief deliberate pause -- the model itself predicts in
            # milliseconds, but showing the result instantly reads as
            # "this didn't really analyze anything." This lets the
            # scanning animation actually be seen before the reveal.
            import time
            time.sleep(0.9)

            try:

                result = analyze_report(report)

            except Exception as error:

                scan_placeholder.empty()

                st.error(
                    "The risk analysis could not be completed."
                )

                st.caption(
                    f"Backend error: {error}"
                )

                st.stop()

            scan_placeholder.empty()


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

                pulse_class = "pulse-ring" if risk == "HIGH" else ""

                st.markdown(
                    f"""
<div class="result-card {pulse_class}">
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
<style>
@keyframes fillBar {{ from {{ width: 0%; }} to {{ width: {confidence_width}%; }} }}
</style>
<div class="result-card">
<div class="result-label">Model Confidence</div>
<div class="result-value" id="confidence-number">0.00%</div>
<div class="confidence-track">
<div class="confidence-fill" style="width:{confidence_width}%; animation: fillBar 1s ease-out;"></div>
</div>
</div>
""",
                    unsafe_allow_html=True,
                )

                components.html(
                    f"""
<script>
(function() {{
    const doc = window.parent.document;
    const target = {confidence:.2f};
    const el = doc.getElementById('confidence-number');
    if (!el) return;
    const start = performance.now();
    const duration = 900;
    function step(now) {{
        const t = Math.min((now - start) / duration, 1);
        const eased = 1 - Math.pow(1 - t, 3);
        el.textContent = (target * eased).toFixed(2) + '%';
        if (t < 1) window.parent.requestAnimationFrame(step);
    }}
    window.parent.requestAnimationFrame(step);
}})();
</script>
""",
                    height=0,
                    width=0,
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

                for i, item in enumerate(indicators):

                    # Escape basic HTML-sensitive characters
                    safe_item = (
                        str(item)
                        .replace("&", "&amp;")
                        .replace("<", "&lt;")
                        .replace(">", "&gt;")
                    )

                    st.markdown(
                        f'<div class="indicator-card" '
                        f'style="animation-delay:{i * 0.08:.2f}s">'
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