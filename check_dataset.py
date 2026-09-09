import pandas as pd

dataframe = pd.read_csv("data/safety_reports.csv")
print(dataframe.head())
print(dataframe.shape)
print("coloumns: ", dataframe.columns.tolist())
print(dataframe["risk_label"].value_counts())
print("\n Missing Values: ")
print(dataframe.isnull().sum())