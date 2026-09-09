# SafetyAI

A lightweight machine learning project for analyzing operational safety reports and classifying them into Low, Medium, or High risk.

## Overview

This project uses a synthetic safety report dataset, TF-IDF text vectorization, and a logistic regression classifier to detect potential safety issues. It includes:

- a Streamlit web app for interactive risk analysis
- a training script to train the model
- a prediction script for direct backend testing
- a dataset generator and dataset inspection script

## Project Structure

- `app.py` – Streamlit front end for entering a safety report and viewing the risk result
- `train.py` – trains the classifier and saves the model artifacts
- `predict.py` – loads the trained model and exposes the `analyze_report()` function
- `generate_dataset.py` – generates the synthetic dataset used for training
- `check_dataset.py` – prints dataset statistics and validation details
- `data/safety_reports.csv` – labeled synthetic safety reports
- `model/risk_model.pkl` – trained classifier
- `model/tfidf_vectorizer.pkl` – TF-IDF vectorizer used at inference time

## Dataset

The project uses a synthetic dataset stored in `data/safety_reports.csv` with the following columns:

- `report_text` – safety report text
- `category` – report category
- `risk_label` – label (`LOW`, `MEDIUM`, `HIGH`)

## Setup

1. Open a terminal in the project folder.
2. Activate the virtual environment:

   PowerShell:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

3. Install the required packages if needed:

   ```powershell
   pip install streamlit pandas scikit-learn joblib
   ```

## Usage

### Train the model

```powershell
python train.py
```

### Run the Streamlit app

```powershell
streamlit run app.py
```

### Inspect the dataset

```powershell
python check_dataset.py
```

### Regenerate the dataset

```powershell
python generate_dataset.py
```

### Run prediction directly

```powershell
python predict.py
```

## Model Details

The pipeline uses:

- `TfidfVectorizer` for text processing
- `LogisticRegression` for risk classification
- `joblib` for saving and loading model artifacts

## Example

Enter a report such as:

> During the night shift, a hydraulic hose near the packaging line began leaking fluid and workers were instructed to evacuate the area.

The app will classify the report and return:

- risk level
- confidence score
- detected safety indicators
- recommended action

## Notes

- The model is trained on synthetic data and is intended for demonstration and experimentation.
- The existing model artifacts in `model/` are already included in this repository snapshot.
