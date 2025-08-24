import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.model_selection import train_test_split
import numpy as np

#Paths
Base_dir = os.path.dirname(os.path.dirname(__file__))
Fact_dir = os.path.join(Base_dir, "data", "Fact_LeadGeneration.csv")
Dim_dir = os.path.join(Base_dir, "data", "Dim_Associate.csv")
Plot_path = os.path.join(Base_dir, "plots", "P10.png")

#Loading the datasets
fact_df = pd.read_csv(Fact_dir)
dim_df = pd.read_csv(Dim_dir)

#Merging the two tables
df = fact_df.merge(dim_df, left_on = "Employee ID", right_on = "Employee ID")

X = df[["TimeMins"]].values
y = df["Leads"].values

#Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#Linear Regression Model
model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

#Model Performance
mse = mean_squared_error(y_test, y_pred).__round__(2)
r2 = r2_score(y_test, y_pred).__round__(2)

print("Model Performance:")
print(f"Mean Squared Error: {mse}")
print(f"R² Score: {r2}")

#Sctter Plots
fig, axes = plt.subplots(2, 1, figsize=(8, 12))

sns.scatterplot(x=X_test.flatten(), y=y_test, label="Actual", ax=axes[0])
sns.lineplot(x=X_test.flatten(), y=y_pred, color="red", label="Predicted", ax=axes[0])
axes[0].set_title("Time Spent vs Leads (Regression Line)")
axes[0].set_xlabel("Time Spent (minutes)")
axes[0].set_ylabel("Leads")

sns.scatterplot(x=y_test, y=y_pred, ax=axes[1])
axes[1].set_title("Actual vs Predicted Leads")
axes[1].set_xlabel("Actual Leads")
axes[1].set_ylabel("Predicted Leads")
plt.tight_layout()
plt.savefig(Plot_path)
plt.show()
plt.close()