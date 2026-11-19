import pandas as pd

file_path = "dataset/sales_data.csv"
data = pd.read_csv(file_path)

data["Order_Date"] = pd.to_datetime(data["Order_Date"])

print("First five rows:")
print(data.head())

print("\nDataset size:")
print(f"{data.shape[0]} rows and {data.shape[1]} columns")

print("\nMissing values in each column:")
print(data.isnull().sum())
