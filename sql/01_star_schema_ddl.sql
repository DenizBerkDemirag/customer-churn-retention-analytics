-- Drop existing tables to allow clean recreation
DROP TABLE IF EXISTS fact_churn CASCADE;
DROP TABLE IF EXISTS dim_subscription CASCADE;
DROP TABLE IF EXISTS dim_customer CASCADE;
DROP TABLE IF EXISTS dim_location CASCADE;

-- 1. DIMENSION: Customer Demographics (household_size calculated dynamically)
CREATE TABLE dim_customer AS
SELECT DISTINCT
    customer_id,
    gender,
    age,
    age_group,
    married,
    number_of_dependents,
    (1 + CASE WHEN married = 'Yes' THEN 1 ELSE 0 END + number_of_dependents) AS household_size
FROM stg_telecom_churn;

ALTER TABLE dim_customer ADD PRIMARY KEY (customer_id);

-- 2. DIMENSION: Location Details
CREATE TABLE dim_location AS
SELECT DISTINCT
    zip_code,
    city,
    latitude,
    longitude,
    population
FROM stg_telecom_churn;

ALTER TABLE dim_location ADD PRIMARY KEY (zip_code);

-- 3. DIMENSION: Subscription & Value-Added Services
CREATE TABLE dim_subscription AS
SELECT DISTINCT
    customer_id,
    offer,
    contract,
    payment_method,
    paperless_billing,
    phone_service,
    multiple_lines,
    internet_service,
    internet_type,
    online_security,
    online_backup,
    device_protection_plan,
    premium_tech_support,
    streaming_tv,
    streaming_movies,
    streaming_music,
    unlimited_data,
    total_addon_services
FROM stg_telecom_churn;

ALTER TABLE dim_subscription ADD PRIMARY KEY (customer_id);

-- 4. FACT TABLE: Financial Metrics and Churn Status
CREATE TABLE fact_churn AS
SELECT
    customer_id,
    zip_code,
    tenure_in_months,
    tenure_group,
    number_of_referrals,
    referral_group,
    monthly_charge,
    monthly_arpu,
    total_charges,
    total_refunds,
    total_extra_data_charges,
    total_long_distance_charges,
    total_revenue,
    customer_status,
    churn_category,
    churn_reason,
    is_churned
FROM stg_telecom_churn;

-- Key Constraints (Primary Key & Foreign Keys)
ALTER TABLE fact_churn ADD PRIMARY KEY (customer_id);
ALTER TABLE fact_churn ADD CONSTRAINT fk_fact_customer FOREIGN KEY (customer_id) REFERENCES dim_customer(customer_id);
ALTER TABLE fact_churn ADD CONSTRAINT fk_fact_location FOREIGN KEY (zip_code) REFERENCES dim_location(zip_code);