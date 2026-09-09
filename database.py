import streamlit as st
from supabase import create_client


@st.cache_resource
def get_supabase():

    return create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_PUBLISHABLE_KEY"]
    )


supabase = get_supabase()


def save_analysis(result, report):

    data = {
        "report_text": report,
        "risk": result["risk"],
        "confidence": result["confidence"],
        "indicators": result["indicators"],
        "recommendation": result["recommendation"]
    }

    response = (
        supabase
        .table("safety_reports")
        .insert(data)
        .execute()
    )

    return response


def get_history():

    response = (
        supabase
        .table("safety_reports")
        .select("*")
        .order("created_at", desc=True)
        .execute()
    )

    return response.data