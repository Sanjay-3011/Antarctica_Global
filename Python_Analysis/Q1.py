import os
import pandas as pd
import matplotlib.pyplot as plt

#Paths
Base_dir = os.path.dirname(os.path.dirname(__file__))
Fact_path = os.path.join(Base_dir, "data", "Fact_LeadGeneration.csv")
Dim_path = os.path.join(Base_dir, "data", "Dim_Associate.csv")
Plot_path = os.path.join(Base_dir, "plots", "P1.png")

#Loading the datasets
fact_df = pd.read_csv(Fact_path)
dim_df = pd.read_csv(Dim_path)

#Merging two tables
df = fact_df.merge(dim_df, left_on="Employee ID", right_on="Employee ID")

#Grouping by employee and Aggregating
efficiency = df.groupby(["Employee ID", "Employee Name"]).agg(TotalLeads=("Leads", "sum"), TotalTimeSpent=("TimeMins", "sum")).reset_index()

#Efficiency calculation
efficiency["Efficiency"] = (efficiency["TotalLeads"] / efficiency["TotalTimeSpent"]).round(2)

#Sorting to find the top performer
efficiency = efficiency.sort_values(by="Efficiency", ascending=False)

print("Lead Generation Efficiency")
print(efficiency)

#Bar Plot
plt.figure(figsize=(8, 5))
plt.bar(efficiency["Employee Name"], efficiency["Efficiency"], color="#4CAF50")
plt.xticks(rotation=45, ha="right")
plt.title("Lead Generation Efficiency")
plt.ylabel("Efficiency (Leads per Time Unit)")
plt.xlabel("Associate")
plt.tight_layout()
plt.savefig(Plot_path)
plt.show()
plt.close()