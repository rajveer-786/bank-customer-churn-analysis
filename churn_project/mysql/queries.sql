-- =========================================================
-- PROJECT: Bank Customer Churn Analysis
-- FILE: queries.sql
-- TOOL: MySQL Workbench
-- =========================================================
-- HOW TO USE THIS FILE:
-- 1. Open MySQL Workbench
-- 2. Connect to your local MySQL server (localhost)
-- 3. Open this file: File > Open SQL Script > queries.sql
-- 4. Run the statements one section at a time (click the
--    lightning bolt icon, or select a section and press
--    Ctrl+Enter / Cmd+Enter)
-- =========================================================


-- ---------------------------------------------------------
-- SECTION 1: CREATE DATABASE AND TABLE
-- ---------------------------------------------------------
CREATE DATABASE IF NOT EXISTS bank_churn_db;
USE bank_churn_db;

CREATE TABLE IF NOT EXISTS customers (
    CustomerID       VARCHAR(20) PRIMARY KEY,
    Age              INT,
    Gender           VARCHAR(10),
    Geography        VARCHAR(30),
    CreditScore      INT,
    Tenure           INT,
    Balance          DECIMAL(12,2),
    NumOfProducts    INT,
    HasCrCard        VARCHAR(5),
    IsActiveMember   VARCHAR(5),
    EstimatedSalary  DECIMAL(12,2),
    Exited           VARCHAR(5)
);


-- ---------------------------------------------------------
-- SECTION 2: LOAD THE CSV DATA INTO THE TABLE
-- ---------------------------------------------------------
-- Easiest for beginners - use the MySQL Workbench
-- "Table Data Import Wizard":
--   1. In the left sidebar, right-click "Tables" under bank_churn_db
--   2. Choose "Table Data Import Wizard"
--   3. Select the file: data/bank_customer_data.csv
--   4. Choose "Use existing table" -> customers
--   5. Click Next through the steps and Finish


-- ---------------------------------------------------------
-- SECTION 3: BASIC CHECKS
-- ---------------------------------------------------------
SELECT * FROM customers LIMIT 10;

SELECT COUNT(*) AS total_customers FROM customers;


-- ---------------------------------------------------------
-- SECTION 4: BUSINESS QUESTIONS (the actual "analysis")
-- ---------------------------------------------------------

-- Q1. What is the overall churn rate?
SELECT
    Exited,
    COUNT(*) AS customer_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM customers), 2) AS percentage
FROM customers
GROUP BY Exited;


-- Q2. Which country has the highest churn rate?
SELECT
    Geography,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Exited = 'Yes' THEN 1 ELSE 0 END) AS customers_churned,
    ROUND(SUM(CASE WHEN Exited = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS churn_rate_pct
FROM customers
GROUP BY Geography
ORDER BY churn_rate_pct DESC;


-- Q3. Does being an active member affect churn?
SELECT
    IsActiveMember,
    ROUND(SUM(CASE WHEN Exited = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS churn_rate_pct
FROM customers
GROUP BY IsActiveMember;


-- Q4. Churn rate by number of products held
SELECT
    NumOfProducts,
    ROUND(SUM(CASE WHEN Exited = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS churn_rate_pct
FROM customers
GROUP BY NumOfProducts
ORDER BY NumOfProducts;


-- Q5. Average balance: churned vs stayed
SELECT
    Exited,
    ROUND(AVG(Balance), 2) AS avg_balance
FROM customers
GROUP BY Exited;


-- Q6. Average credit score: churned vs stayed
SELECT
    Exited,
    ROUND(AVG(CreditScore), 2) AS avg_credit_score
FROM customers
GROUP BY Exited;


-- Q7. Find high-value customers at risk of churning
-- (a nice one to mention in interviews - combines multiple conditions)
SELECT CustomerID, Geography, Balance, EstimatedSalary
FROM customers
WHERE Exited = 'No'
  AND IsActiveMember = 'No'
  AND Balance > 100000
ORDER BY Balance DESC
LIMIT 10;


-- Q8. Countries where average credit score is below the overall average
-- (this uses a subquery)
SELECT
    Geography,
    ROUND(AVG(CreditScore), 2) AS avg_credit_score
FROM customers
GROUP BY Geography
HAVING AVG(CreditScore) < (SELECT AVG(CreditScore) FROM customers)
ORDER BY avg_credit_score ASC;


-- Q9. Churn rate by age group
SELECT
    CASE
        WHEN Age < 30 THEN 'Under 30'
        WHEN Age BETWEEN 30 AND 45 THEN '30-45'
        WHEN Age BETWEEN 46 AND 60 THEN '46-60'
        ELSE '60+'
    END AS age_group,
    ROUND(SUM(CASE WHEN Exited = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS churn_rate_pct
FROM customers
GROUP BY age_group
ORDER BY churn_rate_pct DESC;


-- Q10. Does having a credit card affect churn?
SELECT
    HasCrCard,
    ROUND(SUM(CASE WHEN Exited = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS churn_rate_pct
FROM customers
GROUP BY HasCrCard;

-- =========================================================
-- END OF FILE
-- Tip for your resume/interview: be ready to explain what
-- GROUP BY, CASE WHEN, HAVING, and subqueries do in plain
-- English. That matters more than memorizing every query.
-- =========================================================
