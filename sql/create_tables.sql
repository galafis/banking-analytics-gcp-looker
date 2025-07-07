-- Banking Analytics - BigQuery Table Definitions
-- Advanced GCP/Looker Integration for Financial Services

-- Create dataset
CREATE SCHEMA IF NOT EXISTS `banking_analytics`
OPTIONS(
  description="Banking analytics data for financial services dashboard",
  location="us-central1"
);

-- Customers table
CREATE OR REPLACE TABLE `banking_analytics.customers` (
  customer_id STRING NOT NULL,
  age FLOAT64,
  income FLOAT64,
  segment STRING,
  city STRING,
  account_opening_date TIMESTAMP,
  is_active BOOLEAN,
  credit_score FLOAT64,
  num_products INTEGER,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
)
PARTITION BY DATE(account_opening_date)
CLUSTER BY segment, city
OPTIONS(
  description="Customer master data with demographics and account information"
);

-- Transactions table
CREATE OR REPLACE TABLE `banking_analytics.transactions` (
  transaction_id STRING NOT NULL,
  customer_id STRING NOT NULL,
  transaction_date TIMESTAMP NOT NULL,
  transaction_type STRING,
  amount FLOAT64,
  is_fraud BOOLEAN,
  channel STRING,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
)
PARTITION BY DATE(transaction_date)
CLUSTER BY customer_id, transaction_type
OPTIONS(
  description="Transaction data with fraud detection flags"
);

-- Products table
CREATE OR REPLACE TABLE `banking_analytics.products` (
  customer_id STRING NOT NULL,
  product_type STRING NOT NULL,
  balance FLOAT64,
  opening_date TIMESTAMP,
  is_active BOOLEAN,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
)
PARTITION BY DATE(opening_date)
CLUSTER BY product_type, customer_id
OPTIONS(
  description="Customer product holdings and balances"
);

-- Create views for analytics

-- Daily transaction summary view
CREATE OR REPLACE VIEW `banking_analytics.daily_transaction_summary` AS
SELECT 
  DATE(transaction_date) as transaction_date,
  COUNT(*) as transaction_count,
  SUM(amount) as total_volume,
  AVG(amount) as avg_amount,
  SUM(CASE WHEN is_fraud THEN 1 ELSE 0 END) as fraud_count,
  SUM(CASE WHEN is_fraud THEN amount ELSE 0 END) as fraud_amount,
  COUNT(DISTINCT customer_id) as active_customers
FROM `banking_analytics.transactions`
GROUP BY DATE(transaction_date)
ORDER BY transaction_date DESC;

-- Customer 360 view
CREATE OR REPLACE VIEW `banking_analytics.customer_360` AS
SELECT 
  c.customer_id,
  c.age,
  c.income,
  c.segment,
  c.city,
  c.credit_score,
  c.account_opening_date,
  c.is_active,
  COUNT(p.product_type) as product_count,
  SUM(p.balance) as total_balance,
  COUNT(t.transaction_id) as transaction_count,
  SUM(t.amount) as total_transaction_volume,
  SUM(CASE WHEN t.is_fraud THEN 1 ELSE 0 END) as fraud_count,
  DATE_DIFF(CURRENT_DATE(), DATE(c.account_opening_date), DAY) as customer_tenure_days
FROM `banking_analytics.customers` c
LEFT JOIN `banking_analytics.products` p ON c.customer_id = p.customer_id
LEFT JOIN `banking_analytics.transactions` t ON c.customer_id = t.customer_id
GROUP BY 
  c.customer_id, c.age, c.income, c.segment, c.city, 
  c.credit_score, c.account_opening_date, c.is_active;

-- Product performance view
CREATE OR REPLACE VIEW `banking_analytics.product_performance` AS
SELECT 
  product_type,
  COUNT(DISTINCT customer_id) as customer_count,
  SUM(balance) as total_balance,
  AVG(balance) as avg_balance,
  MIN(balance) as min_balance,
  MAX(balance) as max_balance,
  STDDEV(balance) as balance_stddev
FROM `banking_analytics.products`
WHERE is_active = TRUE
GROUP BY product_type
ORDER BY total_balance DESC;

-- Fraud detection view
CREATE OR REPLACE VIEW `banking_analytics.fraud_analysis` AS
SELECT 
  customer_id,
  COUNT(*) as total_transactions,
  SUM(CASE WHEN is_fraud THEN 1 ELSE 0 END) as fraud_transactions,
  SAFE_DIVIDE(SUM(CASE WHEN is_fraud THEN 1 ELSE 0 END), COUNT(*)) as fraud_rate,
  SUM(amount) as total_amount,
  SUM(CASE WHEN is_fraud THEN amount ELSE 0 END) as fraud_amount,
  AVG(amount) as avg_transaction_amount,
  STDDEV(amount) as amount_stddev,
  MAX(transaction_date) as last_transaction_date
FROM `banking_analytics.transactions`
GROUP BY customer_id
HAVING COUNT(*) >= 5  -- Only customers with at least 5 transactions
ORDER BY fraud_rate DESC, fraud_amount DESC;

-- Monthly trends view
CREATE OR REPLACE VIEW `banking_analytics.monthly_trends` AS
SELECT 
  EXTRACT(YEAR FROM transaction_date) as year,
  EXTRACT(MONTH FROM transaction_date) as month,
  DATE_TRUNC(DATE(transaction_date), MONTH) as month_date,
  COUNT(*) as transaction_count,
  SUM(amount) as total_volume,
  AVG(amount) as avg_amount,
  COUNT(DISTINCT customer_id) as active_customers,
  SUM(CASE WHEN is_fraud THEN 1 ELSE 0 END) as fraud_count,
  SAFE_DIVIDE(SUM(CASE WHEN is_fraud THEN 1 ELSE 0 END), COUNT(*)) as fraud_rate
FROM `banking_analytics.transactions`
GROUP BY 
  EXTRACT(YEAR FROM transaction_date),
  EXTRACT(MONTH FROM transaction_date),
  DATE_TRUNC(DATE(transaction_date), MONTH)
ORDER BY year DESC, month DESC;

-- Customer segmentation analysis
CREATE OR REPLACE VIEW `banking_analytics.segment_analysis` AS
SELECT 
  c.segment,
  COUNT(DISTINCT c.customer_id) as customer_count,
  AVG(c.age) as avg_age,
  AVG(c.income) as avg_income,
  AVG(c.credit_score) as avg_credit_score,
  SUM(p.balance) as total_balance,
  AVG(p.balance) as avg_balance,
  COUNT(t.transaction_id) as total_transactions,
  SUM(t.amount) as total_transaction_volume,
  SUM(CASE WHEN t.is_fraud THEN 1 ELSE 0 END) as fraud_count
FROM `banking_analytics.customers` c
LEFT JOIN `banking_analytics.products` p ON c.customer_id = p.customer_id
LEFT JOIN `banking_analytics.transactions` t ON c.customer_id = t.customer_id
WHERE c.is_active = TRUE
GROUP BY c.segment
ORDER BY total_balance DESC;

-- Create materialized views for better performance
CREATE MATERIALIZED VIEW `banking_analytics.daily_kpis`
PARTITION BY transaction_date
AS
SELECT 
  DATE(transaction_date) as transaction_date,
  COUNT(*) as daily_transactions,
  SUM(amount) as daily_volume,
  COUNT(DISTINCT customer_id) as daily_active_customers,
  SUM(CASE WHEN is_fraud THEN 1 ELSE 0 END) as daily_fraud_count,
  SAFE_DIVIDE(SUM(CASE WHEN is_fraud THEN 1 ELSE 0 END), COUNT(*)) as daily_fraud_rate
FROM `banking_analytics.transactions`
GROUP BY DATE(transaction_date);

-- Indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_customers_segment 
ON `banking_analytics.customers`(segment);

CREATE INDEX IF NOT EXISTS idx_transactions_customer_date 
ON `banking_analytics.transactions`(customer_id, transaction_date);

CREATE INDEX IF NOT EXISTS idx_products_customer_type 
ON `banking_analytics.products`(customer_id, product_type);

