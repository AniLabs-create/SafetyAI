import joblib


# --------------------------------------------------
# Check whether the input is safety-related
# --------------------------------------------------

def is_safety_report(report):

    safety_keywords = [
        # General safety
        "safety",
        "hazard",
        "hazardous",
        "risk",
        "incident",
        "accident",
        "danger",
        "unsafe",
        "injury",
        "injured",

        # Workplace
        "worker",
        "workers",
        "employee",
        "employees",
        "workplace",
        "factory",
        "production",
        "site",
        "area",

        # Equipment / machinery
        "machine",
        "machinery",
        "equipment",
        "motor",
        "pump",
        "valve",
        "pressure",
        "vibration",
        "leak",
        "leaking",

        # Electrical
        "electrical",
        "electric",
        "wire",
        "wiring",
        "voltage",
        "current",
        "circuit",
        "panel",
        "spark",

        # Fire / emergency
        "fire",
        "smoke",
        "flame",
        "alarm",
        "emergency",
        "evacuation",
        "evacuate",

        # Chemicals
        "chemical",
        "toxic",
        "gas",
        "fume",
        "spill",
        "acid",

        # PPE
        "ppe",
        "helmet",
        "gloves",
        "goggles",
        "mask",
        "protective",

        # Maintenance
        "maintenance",
        "repair",
        "inspection",
        "inspect",
        "damaged",
        "damage",
        "broken",
        "failure",

        # Workplace hazards
        "slip",
        "fall",
        "trip",
        "exposed",
        "exposure",
        "blocked",
        "obstruction"
    ]

    report_lower = report.lower()

    for keyword in safety_keywords:

        if keyword in report_lower:
            return True

    return False


# --------------------------------------------------
# Find important safety indicators
# --------------------------------------------------

def find_indicators(report):

    indicators = []

    keywords = {
        "warning": "Warning ignored",
        "ignored": "Warning ignored",
        "maintenance delayed": "Maintenance delayed",
        "maintenance has been delayed": "Maintenance delayed",
        "abnormal vibration": "Abnormal vibration",
        "severe vibration": "Severe vibration",
        "pressure": "Abnormal pressure",
        "leak": "Leak detected",
        "workers remain": "Workers remain in hazardous area",
        "exposed": "Worker exposure detected",
        "fire": "Fire hazard",
        "smoke": "Smoke detected",
        "chemical": "Chemical hazard"
    }

    report_lower = report.lower()

    for keyword, indicator in keywords.items():

        if keyword in report_lower and indicator not in indicators:
            indicators.append(indicator)

    return indicators


# --------------------------------------------------
# Generate recommendation
# --------------------------------------------------

def get_recommendation(risk):

    recommendations = {

        "LOW":
        "Continue monitoring and address during routine maintenance.",

        "MEDIUM":
        "Schedule prompt inspection and corrective action.",

        "HIGH":
        "Immediate inspection and escalation required."
    }

    return recommendations.get(
        risk,
        "Further safety assessment is recommended."
    )


# --------------------------------------------------
# Load trained model and TF-IDF vectorizer
# --------------------------------------------------

model = joblib.load(
    "model/risk_model.pkl"
)

vectorizer = joblib.load(
    "model/tfidf_vectorizer.pkl"
)


# --------------------------------------------------
# Main analysis function
# --------------------------------------------------

def analyze_report(report):

    # ----------------------------------------------
    # Step 1: Safety relevance check
    # ----------------------------------------------

    if not is_safety_report(report):

        return {
            "is_safety_report": False,
            "risk": None,
            "confidence": 0,
            "indicators": [],
            "recommendation":
                "This does not appear to be a safety-related report. "
                "Please enter an operational safety report."
        }


    # ----------------------------------------------
    # Step 2: Convert report into TF-IDF
    # ----------------------------------------------

    report_tfidf = vectorizer.transform([report])


    # ----------------------------------------------
    # Step 3: Predict risk
    # ----------------------------------------------

    prediction = model.predict(report_tfidf)[0]


    # ----------------------------------------------
    # Step 4: Get probabilities
    # ----------------------------------------------

    probabilities = model.predict_proba(report_tfidf)[0]

    confidence = max(probabilities) * 100


    # ----------------------------------------------
    # Step 5: Find safety indicators
    # ----------------------------------------------

    indicators = find_indicators(report)


    # ----------------------------------------------
    # Step 6: Generate recommendation
    # ----------------------------------------------

    recommendation = get_recommendation(prediction)


    # ----------------------------------------------
    # Step 7: Return result
    # ----------------------------------------------

    result = {

        "is_safety_report": True,

        "risk": prediction,

        "confidence": round(confidence, 2),

        "indicators": indicators,

        "recommendation": recommendation
    }

    return result


# --------------------------------------------------
# Test backend directly
# --------------------------------------------------

if __name__ == "__main__":

    report = input("\nEnter a safety report: ")

    result = analyze_report(report)

    print("\nResult:")

    print(result)