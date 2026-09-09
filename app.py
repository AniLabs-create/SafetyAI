import streamlit as st

from predict import analyze_report


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Safety Risk Analyzer",
    page_icon="🛡️",
    layout="wide"
)


# --------------------------------------------------
# Title
# --------------------------------------------------

st.title("Safety Risk Analyzer")

st.write("AI-Powered Safety Intelligence")

st.write(
    "Analyze operational safety reports and identify potential risks "
    "before they become incidents"
)


# --------------------------------------------------
# Safety Report Input
# --------------------------------------------------

st.subheader("Safety Report Input")

report = st.text_area(
    "Enter or paste the operational safety report below:",
    height=200
)


# --------------------------------------------------
# Analyze Button
# --------------------------------------------------

if st.button("Run Risk Analysis"):

    # Check if the user entered anything
    if not report.strip():

        st.warning("Please enter a safety report first.")

    else:

        # Send the report to the backend
        result = analyze_report(report)


        # --------------------------------------------------
        # Check whether this is actually a safety report
        # --------------------------------------------------

        if not result["is_safety_report"]:

            st.warning(
                "⚠️ " + result["recommendation"]
            )


        # --------------------------------------------------
        # If it is a safety report, show ML results
        # --------------------------------------------------

        else:

            risk = result["risk"]
            confidence = result["confidence"]
            indicators = result["indicators"]
            recommendation = result["recommendation"]


            # --------------------------------------------------
            # Risk Result
            # --------------------------------------------------

            st.subheader("Assessed Risk Level")

            if risk == "HIGH":

                st.error(f"🚨 {risk}")

            elif risk == "MEDIUM":

                st.warning(f"⚠️ {risk}")

            else:

                st.success(f"✅ {risk}")


            # --------------------------------------------------
            # Confidence
            # --------------------------------------------------

            st.subheader("Model Confidence")

            st.write(f"{confidence}%")


            # --------------------------------------------------
            # Key Indicators
            # --------------------------------------------------

            st.subheader("Key Indicators")

            if indicators:

                for indicator in indicators:

                    st.write(f"• {indicator}")

            else:

                st.write("• No specific indicators detected")


            # --------------------------------------------------
            # Recommended Action
            # --------------------------------------------------

            st.subheader("Recommended Action")

            if risk == "HIGH":

                st.error(recommendation)

            elif risk == "MEDIUM":

                st.warning(recommendation)

            else:

                st.success(recommendation)