
import pandas as pd
patients = pd.read_csv("data/patients.csv")
print("shape: ", patients.shape)
print(patients.head())
print(patients.dtypes)
