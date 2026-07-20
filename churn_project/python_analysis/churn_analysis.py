"""
churn_analysis.py
------------------
PROJECT: Bank Customer Churn Analysis
LEVEL: Beginner

WHAT THIS SCRIPT DOES:
1. Loads the bank customer data (bank_customer_data.csv)
2. Cleans it a little (checks for missing values)
3. Answers common business questions using pandas:
     - What is the overall churn rate?
     - Which country has the highest churn rate?
     - Does being an "active member" affect churn?
     - Does number of products affect churn?
     - How does age relate to churn?
4. Saves 5 charts (as .png images) into the "charts" folder
5. Prints a short summary to the screen

HOW TO RUN THIS:
1. Install the required libraries (only needed once):
     pip install pandas matplotlib
2. Open a terminal in this "python_analysis" folder
3. Run:
     python churn_analysis.py
4. Check the "charts" folder for the images it creates
"""

import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# STEP 1: LOAD THE DATA
# ---------------------------------------------------------
df = pd.read_csv("../data/bank_customer_data.csv")

print("STEP 1 DONE: Data Loaded")
print("Number of rows:", len(df))
print("Columns:", list(df.columns))
print()

# ---------------------------------------------------------
# STEP 2: BASIC DATA CLEANING / CHECKS
# ---------------------------------------------------------
missing_values = df.isnull().sum()
print("STEP 2: Checking for missing values")
print(missing_values)
print()

# ---------------------------------------------------------
# STEP 3: BUSINESS QUESTION 1 - Overall Churn Rate
# ---------------------------------------------------------
churn_counts = df["Exited"].value_counts()
churn_rate = round(churn_counts["Yes"] / len(df) * 100, 2)
print("STEP 3: Overall Churn Rate")
print(f"{churn_rate}% of customers have churned (left the bank)")
print()

plt.figure(figsize=(6, 6))
plt.pie(churn_counts, labels=churn_counts.index, autopct="%1.1f%%",
        colors=["#70AD47", "#C00000"], startangle=90)
plt.title("Overall Customer Churn Split")
plt.tight_layout()
plt.savefig("charts/1_overall_churn_rate.png")
plt.close()

# ---------------------------------------------------------
# STEP 4: BUSINESS QUESTION 2 - Churn Rate by Geography
# ---------------------------------------------------------
geo_churn = df.groupby("Geography")["Exited"].apply(
    lambda x: round((x == "Yes").sum() / len(x) * 100, 2)
).sort_values(ascending=False)
print("STEP 4: Churn Rate by Country (%)")
print(geo_churn)
print()

plt.figure(figsize=(7, 5))
geo_churn.plot(kind="bar", color="#C00000")
plt.title("Churn Rate by Country (%)")
plt.ylabel("Churn Rate (%)")
plt.xlabel("Country")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("charts/2_churn_by_geography.png")
plt.close()

# ---------------------------------------------------------
# STEP 5: BUSINESS QUESTION 3 - Active Member vs Churn
# ---------------------------------------------------------
active_churn = df.groupby("IsActiveMember")["Exited"].apply(
    lambda x: round((x == "Yes").sum() / len(x) * 100, 2)
)
print("STEP 5: Churn Rate by Active Membership Status (%)")
print(active_churn)
print()

plt.figure(figsize=(6, 5))
active_churn.plot(kind="bar", color="#ED7D31")
plt.title("Churn Rate: Active vs Inactive Members")
plt.ylabel("Churn Rate (%)")
plt.xlabel("Is Active Member")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("charts/3_churn_by_active_status.png")
plt.close()

# ---------------------------------------------------------
# STEP 6: BUSINESS QUESTION 4 - Number of Products vs Churn
# ---------------------------------------------------------
product_churn = df.groupby("NumOfProducts")["Exited"].apply(
    lambda x: round((x == "Yes").sum() / len(x) * 100, 2)
).sort_index()
print("STEP 6: Churn Rate by Number of Products Held")
print(product_churn)
print()

plt.figure(figsize=(7, 5))
product_churn.plot(kind="bar", color="#264478")
plt.title("Churn Rate by Number of Products Held")
plt.ylabel("Churn Rate (%)")
plt.xlabel("Number of Products")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("charts/4_churn_by_num_products.png")
plt.close()

# ---------------------------------------------------------
# STEP 7: BUSINESS QUESTION 5 - Age Distribution: Churned vs Stayed
# ---------------------------------------------------------
avg_age = df.groupby("Exited")["Age"].mean().round(2)
print("STEP 7: Average Age - Churned vs Stayed")
print(avg_age)
print()

plt.figure(figsize=(7, 5))
df.boxplot(column="Age", by="Exited", grid=False)
plt.title("Age Distribution: Churned vs Stayed")
plt.suptitle("")
plt.ylabel("Age")
plt.xlabel("Exited (Churned)")
plt.tight_layout()
plt.savefig("charts/5_age_vs_churn.png")
plt.close()

# ---------------------------------------------------------
# STEP 8: SAVE A CLEAN SUMMARY FILE (used later in Excel/Power BI)
# ---------------------------------------------------------
summary = pd.DataFrame({
    "Metric": [
        "Total Customers", "Customers Churned", "Overall Churn Rate (%)",
        "Highest Churn Country", "Avg Age (Churned)", "Avg Age (Stayed)"
    ],
    "Value": [
        len(df),
        int(churn_counts["Yes"]),
        churn_rate,
        geo_churn.idxmax(),
        avg_age.get("Yes", 0),
        avg_age.get("No", 0),
    ]
})
summary.to_csv("summary_metrics.csv", index=False)

print("ALL DONE! 5 charts saved in the 'charts' folder.")
print("A summary_metrics.csv file was also created.")
