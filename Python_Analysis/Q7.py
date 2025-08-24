import os
import pandas as pd
import matplotlib.pyplot as plt

#Paths
Base_dir = os.path.dirname(os.path.dirname(__file__))
Fact_dir = os.path.join(Base_dir, "data", "Fact_LeadGeneration.csv")
Dim_dir = os.path.join(Base_dir, "data", "Dim_Associate.csv")
Plot_path = os.path.join(Base_dir, "plots", "P7.png")

#Loading the datasets
fact_df = pd.read_csv(Fact_dir)
dim_df = pd.read_csv(Dim_dir)

#Merging the two tables
df = fact_df.merge(dim_df, left_on="Employee ID", right_on = "Employee ID")

high_perf_results = []
for associate, group in df.groupby("Employee Name"):
    # 90th percentile cutoff
    cutoff = group["Leads"].quantile(0.9)
    
    #Selecting high-performance days
    high_perf_days = group[group["Leads"] >= cutoff]
    
    #Calculating Avgtime spent on those days
    avg_time = high_perf_days["TimeMins"].mean()
    
    high_perf_results.append({"Employee Name": associate, "Cutoff_Leads": cutoff, "AvgTime_HighPerfDays": avg_time,"HighPerf_DaysCount": len(high_perf_days)})

#Converting results into DataFrame
high_perf_df = pd.DataFrame(high_perf_results)

print("High-Performance Days Analysis:")
print(high_perf_df)

#Plot
plt.figure(figsize=(8,5))
plt.barh(high_perf_df["Employee Name"], high_perf_df["AvgTime_HighPerfDays"], color="skyblue")

plt.xlabel("Average Time Spent(mins)")
plt.ylabel("Associate")
plt.title("High-Performance Days")
plt.gca().invert_yaxis()  #Keeping the highes performance in the top
plt.savefig(Plot_path)
plt.show()
plt.close()