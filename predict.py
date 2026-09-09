import joblib


# --------------------------------------------------
# Check whether the input is safety-related
# --------------------------------------------------

def is_safety_report(report):

    safety_keywords = [
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

        "worker",
        "workers",
        "employee",
        "employees",
        "workplace",
        "factory",
        "production",
        "site",

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

        "electrical",
        "electric",
        "wire",
        "wiring",
        "voltage",
        "current",
        "circuit",
        "panel",
        "spark",

        "fire",
        "smoke",
        "flame",
        "alarm",
        "emergency",
        "evacuation",
        "evacuate",

        "chemical",
        "toxic",
        "gas",
        "fume",
        "spill",
        "acid",

        "ppe",
        "helmet",
        "gloves",
        "goggles",
        "mask",
        "protective",

        "maintenance",
        "repair",
        "inspection",
        "inspect",
        "damaged",
        "damage",
        "broken",
        "failure",

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
# Check whether enough information is provided
# --------------------------------------------------

def has_enough_information(report):

    information_keywords = [
        "machine",
        "machinery",
        "equipment",
        "worker",
        "workers",
        "employee",
        "employees",
        "factory",
        "production",
        "plant",
        "area",
        "site",
        "room",
        "pipe",
        "valve",
        "tank",
        "panel",
        "wire",
        "electrical",
        "chemical",
        "fire",
        "smoke",
        "leak",
        "pressure",
        "vibration",
        "maintenance",
        "inspection",
        "damage",
        "damaged",
        "broken",
        "alarm",
        "spill",
        "exposed",
        "exposure",
        "ppe",
        "injury",
        "injured",
        "hazard"
    ]

    report_lower = report.lower()

    matches = 0

    for keyword in information_keywords:

        if keyword in report_lower:
            matches += 1

    # We want at least two meaningful safety details
    return matches >= 2


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
# Load trained model and vectorizer
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
    # Step 1: Check safety relevance
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
    # Step 2: Check information quality
    # ----------------------------------------------

    if not has_enough_information(report):

        return {
            "is_safety_report": True,
            "insufficient_information": True,
            "risk": None,
            "confidence": 0,
            "indicators": [],
            "recommendation":
                "The report appears to be safety-related, "
                "but there is not enough information to determine "
                "the risk level. Please provide more details about "
                "the hazard, equipment, workers, or current conditions."
        }


    # ----------------------------------------------
    # Step 3: Convert report to TF-IDF
    # ----------------------------------------------

    report_tfidf = vectorizer.transform([report])


    # ----------------------------------------------
    # Step 4: Predict risk
    # ----------------------------------------------

    prediction = model.predict(report_tfidf)[0]


    # ----------------------------------------------
    # Step 5: Get probabilities
    # ----------------------------------------------

    probabilities = model.predict_proba(report_tfidf)[0]

    confidence = max(probabilities) * 100


    # ----------------------------------------------
    # Step 6: Find indicators
    # ----------------------------------------------

    indicators = find_indicators(report)


    # ----------------------------------------------
    # Step 7: Generate recommendation
    # ----------------------------------------------

    recommendation = get_recommendation(prediction)


    # ----------------------------------------------
    # Step 8: Return result
    # ----------------------------------------------

    return {
        "is_safety_report": True,
        "insufficient_information": False,
        "risk": prediction,
        "confidence": round(confidence, 2),
        "indicators": indicators,
        "recommendation": recommendation
    }


# --------------------------------------------------
# Test backend directly
# --------------------------------------------------

if __name__ == "__main__":

    report = input("\nEnter a safety report: ")

    result = analyze_report(report)

    print("\nResult:")

    print(result)