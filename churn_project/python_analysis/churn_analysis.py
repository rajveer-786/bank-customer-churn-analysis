

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("../data/bank_customer_data.csv")

print("STEP 1 DONE: Data Loaded")
print("Number of rows:", len(df))
print("Columns:", list(df.columns))
print()


missing_values = df.isnull().sum()
print("STEP 2: Checking for missing values")
print(missing_values)
print()


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
