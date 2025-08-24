import pandas as pd
import matplotlib.pyplot as plt
import os

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
FACT_PATH = os.path.join(BASE_DIR, "data", "Fact_LeadGeneration.csv")
DIM_PATH = os.path.join(BASE_DIR, "data", "Dim_Associate.csv")
PLOT_PATH = os.path.join(BASE_DIR, "plots", "Lead_generation_eff.png")

# Loading the datasets
fact_df = pd.read_csv(FACT_PATH)
dim_df = pd.read_csv(DIM_PATH)

# Merging two tables
df = fact_df.merge(dim_df, left_on="Employee ID", right_on="Employee ID")

# Aggregate
efficiency = df.groupby(["Employee ID", "Employee Name"]).agg(TotalLeads=("Leads", "sum"), TotalTimeSpent=("TimeMins", "sum")).reset_index()

# Efficiency calculation
efficiency["Efficiency"] = (efficiency["TotalLeads"] / efficiency["TotalTimeSpent"]).round(2)

# Sorting to find the top performer
efficiency = efficiency.sort_values(by="Efficiency", ascending=False)
top_employee = efficiency.iloc[0]

print("Lead Generation Efficiency")
print(efficiency)
print(f"\n Highest efficiency: {top_employee['Employee Name']} ({top_employee['Efficiency']} leads per unit time)")

# Plot
plt.figure(figsize=(8, 5))
plt.bar(efficiency["Employee Name"], efficiency["Efficiency"], color="#4CAF50")
plt.xticks(rotation=45, ha="right")
plt.title("Lead Generation Efficiency per Associate")
plt.ylabel("Efficiency (Leads per Time Unit)")
plt.tight_layout()
plt.savefig(PLOT_PATH)
plt.close()
