"""
generate_data.py
-----------------
Creates a fake (but realistic) bank customer dataset used for a
Customer Churn Analysis project. You don't need to run this yourself -
the CSV is already generated for you as bank_customer_data.csv. This file
is only here so you understand where the data came from.
"""
import pandas as pd
import numpy as np
import random

random.seed(21)
np.random.seed(21)

n_rows = 900

geographies = ["France", "Germany", "Spain"]
genders = ["Male", "Female"]

rows = []
for i in range(1, n_rows + 1):
    geography = random.choice(geographies)
    gender = random.choice(genders)
    age = int(np.clip(np.random.normal(39, 10), 18, 75))
    credit_score = int(np.clip(np.random.normal(650, 80), 350, 850))
    tenure = random.randint(0, 10)  # years as a customer
    balance = round(max(0, np.random.normal(76000, 45000)), 2)
    num_products = random.choices([1, 2, 3, 4], weights=[0.45, 0.40, 0.10, 0.05])[0]
    has_credit_card = random.choices(["Yes", "No"], weights=[0.7, 0.3])[0]
    is_active_member = random.choices(["Yes", "No"], weights=[0.55, 0.45])[0]
    estimated_salary = round(random.uniform(15000, 200000), 2)

    # Build churn probability based on realistic risk factors
    churn_score = 0.12  # base rate
    if is_active_member == "No":
        churn_score += 0.22
    if num_products == 1:
        churn_score += 0.10
    if num_products >= 3:
        churn_score += 0.15
    if age > 50:
        churn_score += 0.15
    if credit_score < 500:
        churn_score += 0.10
    if geography == "Germany":
        churn_score += 0.10
    if balance == 0:
        churn_score += 0.05

    exited = "Yes" if random.random() < min(churn_score, 0.9) else "No"

    rows.append({
        "CustomerID": f"CUST{i:05d}",
        "Age": age,
        "Gender": gender,
        "Geography": geography,
        "CreditScore": credit_score,
        "Tenure": tenure,
        "Balance": balance,
        "NumOfProducts": num_products,
        "HasCrCard": has_credit_card,
        "IsActiveMember": is_active_member,
        "EstimatedSalary": estimated_salary,
        "Exited": exited,
    })

df = pd.DataFrame(rows)
df.to_csv("/home/claude/churn_project/data/bank_customer_data.csv", index=False)
print("Generated", len(df), "rows")
print(df["Exited"].value_counts())
