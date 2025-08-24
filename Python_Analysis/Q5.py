import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np

#Paths
Base_dir = os.path.dirname(os.path.dirname(__file__))
Fact_path = os.path.join(Base_dir, "data", "Fact_LeadGeneration.csv")
Dim_path = os.path.join(Base_dir, "data", "Dim_Associate.csv")
Plot_path = os.path.join(Base_dir, "plots", "P5.png")

#Loading the datasets
fact_df = pd.read_csv(Fact_path)
dim_df = pd.read_csv(Dim_path)

#Merging datasets
df = fact_df.merge(dim_df, left_on="Employee ID", right_on="Employee ID")

#Converting Date column
df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')

#Grouping by Employee and Date for incomplete leads
df_incomplete = df.groupby(["Employee Name", "Date"])["IncompleteLeads"].sum().reset_index()
results = []

associates = df_incomplete["Employee Name"].unique()
fig, axes = plt.subplots(len(associates), 1, figsize=(10, 12), sharex=True)

for i, associate in enumerate(associates):
    temp = df_incomplete[df_incomplete["Employee Name"] == associate].copy()
    temp = temp.sort_values("Date")

    #Preparing regression variables
    X = np.arange(len(temp)).reshape(-1, 1)  # time index
    y = temp["IncompleteLeads"].values

    #Fitting linear regression
    model = LinearRegression()
    model.fit(X, y)
    slope = model.coef_[0]

    #Storing the result
    status = "Improvement" if slope < 0 else "Deterioration" if slope > 0 else "No Change"
    results.append({"Employee Name": associate, "Slope": slope, "Trend": status})

    #Ploting subplot
    axes[i].plot(temp["Date"], y, marker="o", label=f"{associate} (Actual)")
    axes[i].plot(temp["Date"], model.predict(X), linestyle="--", label=f"{associate} Trend")
    axes[i].set_title(f"Incomplete Leads Trend - {associate} ({status})")
    axes[i].set_ylabel("Incomplete Leads")
    axes[i].legend()

#Shared x-axis
plt.xlabel("Date")
plt.tight_layout()
plt.savefig(Plot_path)

results_df = pd.DataFrame(results)
print(results_df)