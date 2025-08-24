import os
import pandas as pd
import matplotlib.pyplot as plt

#Paths
Base_dir = os.path.dirname(os.path.dirname(__file__))
Fact_path = os.path.join(Base_dir, "data", "Fact_LeadGeneration.csv")
Dim_path = os.path.join(Base_dir, "data", "Dim_Associate.csv")
Plot_path = os.path.join(Base_dir, "plots", "Leads_Performance_Comparison.png")

#Loading the datasets
fact_df = pd.read_csv(Fact_path)
dim_df = pd.read_csv(Dim_path)

#Merging datasets
df = fact_df.merge(dim_df, left_on="Employee ID", right_on="Employee ID")

#Grouping by Associate and Review
review_perf = df.groupby(["Employee ID", "Employee Name", "Review"]).agg( AvgLeads=("Leads", "mean")).reset_index()

#Pivot for comparison b/w Attended and Missed
review_pivot = review_perf.pivot(index=["Employee ID", "Employee Name"], columns="Review", values="AvgLeads").reset_index()

#Renaming the columns
review_pivot = review_pivot.rename(columns={"Attended": "Attended_AvgLeads", "Missed": "Missed_AvgLeads"})

#Calculating percentage difference
review_pivot["% Difference"] = ((review_pivot["Attended_AvgLeads"] - review_pivot["Missed_AvgLeads"]) / review_pivot["Missed_AvgLeads"]) * 100

#Changing the column type to object to store both int and str
review_pivot["% Difference"] = review_pivot["% Difference"].astype("object")

for idx, row in review_pivot.iterrows():
    if pd.isna(row["Attended_AvgLeads"]) and row["% Difference"] < 0:
        review_pivot.loc[idx, "% Difference"] = "Always Missed"
    elif pd.isna(row["Missed_AvgLeads"]):
        review_pivot.loc[idx, "% Difference"] = "Perfect Attendance"

print("Review Attendance Performance")
print(review_pivot)

#Grouped Plot
pivot_df = review_perf.pivot(index="Employee Name", columns="Review", values="AvgLeads").fillna(0)
pivot_df.plot(kind="bar", figsize=(8,6))
plt.title("Average Leads: Attended vs Missed Daily Team Reviews")
plt.ylabel("Average Leads")
plt.xlabel("Associates")
plt.xticks(rotation=0)
plt.legend(title="Review Status")
plt.tight_layout()
plt.savefig(Plot_path)
plt.close()