import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np

#Paths
Base_dir = os.path.dirname(os.path.dirname(__file__))
Fact_path = os.path.join(Base_dir, "data", "Fact_LeadGeneration.csv")
Dim_path = os.path.join(Base_dir, "data", "Dim_Associate.csv")
Plot_path = os.path.join(Base_dir, "plots", "P6.png")

#Loading the datasets
fact_df = pd.read_csv(Fact_path)
dim_df = pd.read_csv(Dim_path)

#Merging datasets
df = fact_df.merge(dim_df, left_on="Employee ID", right_on="Employee ID")

#Grouping by Employee
performance_consis = df.groupby(["Employee Name"]).agg(StdLeads = ("Leads", "std"), MeanLeads = ("Leads", "mean")).reset_index()

#Calculating Coefficient of Variation
performance_consis["CV"] = round(performance_consis["StdLeads"] / performance_consis["MeanLeads"], 2)
print(performance_consis)

#Plot
plt.figure(figsize=(6,4))
plt.plot(performance_consis["Employee Name"], performance_consis["CV"], marker="o", linestyle="-", color="blue")
for i, row in performance_consis.iterrows():
    plt.text(row["Employee Name"], row["CV"]+0.006, str(row["CV"]))
plt.title("Performance Consistency")
plt.xlabel("Associates")
plt.ylabel("Coefficient of Variation")
plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()
plt.gca().invert_yaxis()
plt.savefig(Plot_path)
plt.close()