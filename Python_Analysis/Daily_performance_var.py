import os
import pandas as pd
import matplotlib.pyplot as plt

# Paths
Base_dir = os.path.dirname(os.path.dirname(__file__))
Fact_path = os.path.join(Base_dir, "data", "Fact_LeadGeneration.csv")
Dim_path = os.path.join(Base_dir, "data", "Dim_Associate.csv")
Plot_path = os.path.join(Base_dir, "plots", "Daily_performance_var.png")

# Loading the datasets
fact_df = pd.read_csv(Fact_path)
dim_df = pd.read_csv(Dim_path)

# Merging two tables
df = fact_df.merge(dim_df, left_on="Employee ID", right_on="Employee ID")

# Grouping by employee and date
daily_leads = df.groupby(["Employee ID", "Employee Name", "Date"])["Leads"].sum().reset_index()

# Calculating std dev of daily leads per associate
variability = daily_leads.groupby(["Employee ID", "Employee Name"])["Leads"].std().reset_index().round(2)
variability = variability.rename(columns={"Leads": "StdDevLeads"})

# Sorting to find highest variability
variability = variability.sort_values(by="StdDevLeads", ascending=False)
top_var = variability.iloc[0]

print("Daily Performance Variability")
print(variability)
print(f"\n Highest variability: {top_var['Employee Name']} ({top_var['StdDevLeads']} std dev)")

# --- Plot ---
plt.figure(figsize=(8,5))
plt.bar(variability["Employee Name"], variability["StdDevLeads"], color="coral")
plt.xlabel("Employee")
plt.ylabel("Std Dev of Daily Leads")
plt.title("Daily Performance Variability")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(Plot_path)
plt.close()
