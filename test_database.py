import streamlit as st
from database import supabase

st.title("Supabase Connection Test")

test_data = {
    "report_text": "Test safety report from Safety Risk Analyzer",
    "risk": "MEDIUM",
    "confidence": 87.5,
    "indicators": [
        "Test indicator",
        "Maintenance check required"
    ],
    "recommendation": "Schedule prompt inspection."
}

try:
    response = (
        supabase
        .table("safety_reports")
        .insert(test_data)
        .execute()
    )

    st.success("✅ Database connection successful!")

    st.write("Data saved:")
    st.json(response.data)

except Exception as e:
    st.error("❌ Database connection failed")
    st.exception(e)