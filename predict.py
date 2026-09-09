import joblib


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
# Load trained AI model and TF-IDF vectorizer
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

    # Convert report into TF-IDF numbers
    report_tfidf = vectorizer.transform([report])

    # Predict risk level
    prediction = model.predict(report_tfidf)[0]

    # Get probabilities
    probabilities = model.predict_proba(report_tfidf)[0]

    # Highest probability = confidence
    confidence = max(probabilities) * 100

    # Find safety indicators
    indicators = find_indicators(report)

    # Generate recommendation
    recommendation = get_recommendation(prediction)

    # Final result
    result = {
        "risk": prediction,
        "confidence": round(confidence, 2),
        "indicators": indicators,
        "recommendation": recommendation
    }

    return result


# --------------------------------------------------
# Test the backend directly
# --------------------------------------------------

if __name__ == "__main__":

    report = input("\nEnter a safety report: ")

    result = analyze_report(report)

    print("\nResult:")
    print(result)