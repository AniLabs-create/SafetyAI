import pandas as pd

from sklearn.model_selection import train_test_split

from sklearn.linear_model import LogisticRegression

from sklearn.metrics import accuracy_score, classification_report

import joblib


dataframe = pd.read_csv("data/safety_reports.csv")


X = dataframe["report_text"]
Y = dataframe["risk_label"]


X_train, X_test, Y_train, Y_test = train_test_split(
    X,
    Y,
    test_size = 0.2,
    random_state = 42,
    stratify=Y
)

from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer()

X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

model = LogisticRegression(max_iter = 1000)
model.fit(X_train_tfidf, Y_train)
print("\n Model training complete!")

Y_predict = model.predict(X_test_tfidf)
print("\nPredictions: ")
print(Y_predict[:10])

accuracy = accuracy_score(Y_test, Y_predict)
print("\n Accuracy: ", accuracy)
print(f"Accuracy percentage: { accuracy * 100} % " )

print("\nClassification Report: ")
print(classification_report(Y_test, Y_predict))

probabilities = model.predict_proba(X_test_tfidf)
print("\nFirst prediction probabilities:")
print(probabilities[0])

print("\nClasses:")
print(model.classes_)

print("\n Training TF-IDf shape: ")
print(X_train_tfidf.shape)

print("\n Testing TF-IDF shape: ")
print(X_test_tfidf.shape)

print("\nNumber of features: ", len(vectorizer.get_feature_names_out()))
print("\nFirst 20 features: ")
print(vectorizer.get_feature_names_out()[:20])

print("Total Reports: ", len(dataframe))
print("Training Reports: ", len(X_train))
print("Testing Reports: ", len(X_test))


print("\nTraining Distributions: ")
print(Y_train.value_counts())


print("\nTesting Distributions: ")
print(Y_test.value_counts())

joblib.dump(model, "model/risk_model.pkl")
joblib.dump(vectorizer, "model/tfidf_vectorizer.pkl")
print("\n Model and Vectorizer are Saved")