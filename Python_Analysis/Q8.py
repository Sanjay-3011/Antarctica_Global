import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

#Paths
Base_dir = os.path.dirname(os.path.dirname(__file__))
Fact_dir = os.path.join(Base_dir, "data", "Fact_LeadGeneration.csv")
Dim_dir = os.path.join(Base_dir, "data", "Dim_Associate.csv")
Plot_path = os.path.join(Base_dir, "plots", "P8.png")

#Loading the datasets
fact_df = pd.read_csv(Fact_dir)
dim_df = pd.read_csv(Dim_dir)

#Merging the two tables
df = fact_df.merge(dim_df, left_on="Employee ID", right_on = "Employee ID")
df['Date'] = pd.to_datetime(df['Date'], format = "%d-%m-%Y")

#Grouping TimeMins into Bins
bin_size = 30  #minutes
df['TimeBin'] = (df['TimeMins'] // bin_size) * bin_size

#Calculating AvgLeads per bin
bin_summary = df.groupby('TimeBin')['Leads'].mean().reset_index().round(2)

#Simple Regression to find trend
X = bin_summary[['TimeBin']]
y = bin_summary['Leads']
model = LinearRegression().fit(X, y)
bin_summary['PredictedLeads'] = model.predict(X).round(2)

#Identifying Optimal Time
optimal_bin = bin_summary.loc[bin_summary['Leads'].idxmax(), 'TimeBin']

print("Time Bin Analysis (minutes):")
print(bin_summary)
print(f"\n✅ Optimal Time Spent for Max Leads ≈ {optimal_bin}-{optimal_bin+bin_size} minutes")

#Plot
plt.figure(figsize=(8,6))
plt.scatter(df['TimeMins'], df['Leads'], alpha=0.3, label="Daily Data")
plt.plot(bin_summary['TimeBin'], bin_summary['Leads'], marker='o', color='red', label="Avg Leads per Bin")
plt.plot(bin_summary['TimeBin'], bin_summary['PredictedLeads'], linestyle='--', color='blue', label="Trend Line")
plt.axvline(optimal_bin, color="green", linestyle="--", label=f"Optimal Time ≈ {optimal_bin} mins")
plt.xlabel("Time Spent on Lead Generation (mins)")
plt.ylabel("Avg Leads Generated")
plt.title("Impact of Time Spent on Leads Generated")
plt.legend()
plt.show()
plt.savefig(Plot_path)
plt.close()
