import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

#Paths
Base_dir = os.path.dirname(os.path.dirname(__file__))
Fact_path = os.path.join(Base_dir, "data", "Fact_LeadGeneration.csv")
Dim_path = os.path.join(Base_dir, "data", "Dim_Associate.csv")
Plot_path = os.path.join(Base_dir, "plots", "P3.png")

#Loading the datasets
fact_df = pd.read_csv(Fact_path)
dim_df = pd.read_csv(Dim_path)

#Merging two tables
df = fact_df.merge(dim_df, left_on="Employee ID", right_on="Employee ID")

# #Droping missing values to avoid invalid correlations
# time_efficiency = df.dropna(subset=["AvgMinsPerLead", "Leads"])

def corr_measure(corr):
    if corr > 0:
        return "Positive"
    elif corr < 0:
        return "Negative"
    else:
        return "Neutral"

#Overall correlation
corr, pval = pearsonr(df["AvgMinsPerLead"], df["Leads"])
corr, pval = corr.round(2), pval.round(3)
print(f"Overall correlation: {corr} ({corr_measure(corr)}) | p-value={pval}")

#Correlation per associate
for name, group in df.groupby("Employee Name"):
    if len(group) > 1:  # Pearson needs at least 2 points
        corr, pval = pearsonr(group["AvgMinsPerLead"], group["Leads"])
        corr, pval = corr.round(2), pval.round(3)
        print(f"{name}: {corr} ({corr_measure(corr)}) | p-value={pval}")

#Scatter plot with trendline
plt.figure(figsize=(8,6))
plt.scatter(df["AvgMinsPerLead"], df["Leads"], alpha=0.6)
m, b = np.polyfit(df["AvgMinsPerLead"], df["Leads"], 1)
plt.plot(df["AvgMinsPerLead"], m*df["AvgMinsPerLead"]+b, color="red", linewidth=2)
plt.title("Time Management Analysis")
plt.xlabel("Average Time per Lead (mins)")
plt.ylabel("Total Leads per Day")
plt.grid(True, linestyle="--", alpha=0.5)
plt.savefig(Plot_path)
plt.show()
plt.close()