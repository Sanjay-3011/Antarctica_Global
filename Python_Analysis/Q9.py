import os
import pandas as pd
import matplotlib.pyplot as plt

#Paths
Base_dir = os.path.dirname(os.path.dirname(__file__))
Fact_dir = os.path.join(Base_dir, "data", "Fact_LeadGeneration.csv")
Dim_dir = os.path.join(Base_dir, "data", "Dim_Associate.csv")
Plot_path = os.path.join(Base_dir, "plots", "P9.png")

#Loading the datasets
fact_df = pd.read_csv(Fact_dir)
dim_df = pd.read_csv(Dim_dir)

#Merging the two tables
df = fact_df.merge(dim_df, left_on = "Employee ID", right_on = "Employee ID")

# Convert Date column to datetime
df["Date"] = pd.to_datetime(df["Date"], format = "%d-%m-%Y")

# Weekday (Mon=0 … Sun=6)
df["DayOfWeek"] = df["Date"].dt.dayofweek

# Weekday vs Weekend
df["DayType"] = df["DayOfWeek"].apply(lambda x: "Weekend" if x >= 5 else "Weekday")

# Group & calculate averages
avg_leads = (
    df.groupby(["Employee Name", "DayType"])["Leads"]
    .mean()
    .reset_index()
)

print("Average Leads - Weekday vs Weekend:\n", avg_leads)

# Pivot for plotting
pivot_df = avg_leads.pivot(index="Employee Name", columns="DayType", values="Leads")

# Plot grouped bar chart
pivot_df.plot(kind="bar", figsize=(8, 6))
plt.title("Average Leads on Weekdays vs Weekends (per Associate)")
plt.ylabel("Average Leads")
plt.xlabel("Employee Name")
plt.xticks(rotation=0)
plt.legend(title="Day Type")
plt.tight_layout()
plt.show()
plt.savefig(Plot_path)
plt.close()