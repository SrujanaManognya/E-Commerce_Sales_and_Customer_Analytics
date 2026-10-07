# 🛒 E-Commerce Sales & Customer Analytics

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?logo=pandas)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-SQL-336791?logo=postgresql)
![Power BI](https://img.shields.io/badge/Power%20BI-Dashboard-F2C811?logo=powerbi)
![CSV](https://img.shields.io/badge/CSV-Data%20Source-6C757D)
![DAX](https://img.shields.io/badge/DAX-Data%20Modeling-0078D4)
![GitHub](https://img.shields.io/badge/GitHub-Portfolio-181717?logo=github)

## 📌 Project Overview

**E-Commerce Sales & Customer Analytics** is an end-to-end data analytics project built using the **Brazilian E-Commerce Public Dataset by Olist**.

The project analyzes approximately **100,000 e-commerce orders from 2016–2018**, combining order, customer, product, payment, freight, seller and review information to understand sales performance, customer behavior, product performance and delivery experience.

The project follows a complete analytics workflow:

**Raw Data → Data Cleaning → Feature Engineering → EDA → SQL Analysis → Customer Segmentation → Power BI**

---

## 🎯 Business Problem

Management wants to understand:

- How sales revenue changes over time
- Which product categories generate the most revenue
- Who the highest-value customers are
- How many customers make repeat purchases
- Where customers are geographically concentrated
- How delivery delays affect customer experience
- Which product categories have stronger customer ratings
- Which customers are Champions, Loyal Customers, Potential Loyalists, At Risk or Lost Customers

The objective is to transform raw transactional data into actionable business insights that can support **revenue growth, customer retention, product strategy and delivery improvement**.

---

# 🗂️ Dataset

The project uses the **Brazilian E-Commerce Public Dataset by Olist** available through Kaggle.

The dataset contains approximately 100,000 orders from 2016–2018 and includes information related to orders, products, customers, payments, freight, sellers and reviews.

### Main tables

```text
olist_orders_dataset.csv
olist_order_items_dataset.csv
olist_order_payments_dataset.csv
olist_order_reviews_dataset.csv
olist_products_dataset.csv
olist_customers_dataset.csv
olist_sellers_dataset.csv
olist_product_category_name_translation.csv
```

The project report documents these source tables and the analytical workflow.

---

# 🛠️ Tools & Technologies

| Technology | Purpose |
|---|---|
| **Python** | Data cleaning, transformation and analysis |
| **Pandas** | Data manipulation |
| **PostgreSQL** | SQL analytics |
| **Excel** | Supporting analysis |
| **Power BI** | Interactive dashboard |
| **DAX** | Measures and business calculations |
| **GitHub** | Version control and portfolio |

The project report specifically identifies SQL, Python, Pandas, Excel, Power BI and DAX as project tools.

---

# 🔄 Project Workflow

```text
                    ┌─────────────────────┐
                    │    Olist Dataset    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Data Cleaning     │
                    │  Missing Values     │
                    │  Duplicate Checks   │
                    │  Data Types         │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Feature Engineering │
                    │ Delivery Metrics    │
                    │ Revenue Metrics     │
                    │ Review Metrics      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Analytical Dataset  │
                    │ Order-Level Table    │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
        ┌──────────┐     ┌──────────┐     ┌───────────┐
        │  Python  │     │   SQL    │     │   RFM     │
        │   EDA    │     │ Analysis │     │Segment.   │
        └────┬─────┘     └────┬─────┘     └─────┬─────┘
             │                │                 │
             └────────────────┼─────────────────┘
                              ▼
                    ┌─────────────────────┐
                    │   BI Visualization  │
                    │      Power BI       │
                    └─────────────────────┘
```

---

# 🧹 Data Preparation

The Python workflow includes:

- Inspecting dataset shape and data types
- Identifying primary and foreign keys
- Checking duplicate IDs
- Checking missing values
- Converting timestamps
- Calculating delivery metrics
- Comparing delivery time with review score
- Comparing delivery delay with order value
- Translating product categories
- Identifying cancelled and unavailable orders
- Creating an analytical order-level dataset
- Exporting cleaned data

These preparation tasks are documented in the project report.

---

# ⚙️ Feature Engineering

The analytical dataset contains several derived business metrics:

```text
delivery_days
estimated_delivery_days
delivery_delay_days
order_revenue
freight_cost
total_order_value
review_score
```

These derived fields form the foundation for the SQL and BI analysis.

---

# 🐍 Python Analysis

Python and Pandas were used to transform the raw Olist tables into an analytical order-level dataset.

### Main Python tasks

```text
Data Inspection
      ↓
Data Quality Checks
      ↓
Timestamp Conversion
      ↓
Feature Engineering
      ↓
Delivery Analysis
      ↓
Category Translation
      ↓
Order-Level Dataset
      ↓
Export CSV
```

### Key analytical questions

- What are the major sales trends?
- Which categories generate the most revenue?
- Are there unusual delivery patterns?
- How does delivery performance relate to customer reviews?
- Which orders are cancelled or unavailable?

---

# 🐘 PostgreSQL Analysis

The cleaned analytical dataset was loaded into PostgreSQL for SQL-based business analysis.

### SQL analyses include

### 1. Monthly Revenue

```sql
SELECT
    DATE_TRUNC('month', order_purchase_timestamp::timestamp) AS month,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(order_revenue)::numeric, 2) AS monthly_revenue
FROM analytical_order_level
WHERE order_status = 'delivered'
GROUP BY DATE_TRUNC('month', order_purchase_timestamp::timestamp)
ORDER BY month;
```

### 2. Top Product Categories

```sql
SELECT
    COUNT(*) AS total_delivered_orders,

    COUNT(*) FILTER (
        WHERE delivery_status = 'Late'
    ) AS late_orders,

    COUNT(*) FILTER (
        WHERE delivery_status = 'Early'
    ) AS early_orders,

    COUNT(*) FILTER (
        WHERE delivery_status = 'On Time'
    ) AS on_time_orders,

    ROUND(
        100.0 * COUNT(*) FILTER (
            WHERE delivery_status = 'Late'
        ) / NULLIF(COUNT(*), 0),
        2
    ) AS late_delivery_percentage

FROM analytical_order_level
WHERE is_delivered = TRUE;
```

### 3. Average Order Value

```sql
SELECT
    DATE_TRUNC('month', order_purchase_timestamp::timestamp) AS month,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(total_order_value)::numeric, 2) AS total_revenue,
    ROUND(AVG(total_order_value)::numeric, 2) AS average_order_value
FROM analytical_order_level
WHERE order_status = 'delivered'
GROUP BY DATE_TRUNC('month', order_purchase_timestamp::timestamp)
ORDER BY month;
```

### 4. Late Delivery Analysis

```sql
SELECT
    DATE_TRUNC('month', order_purchase_timestamp::timestamp) AS month,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(order_revenue)::numeric, 2) AS monthly_revenue
FROM analytical_order_level
WHERE order_status = 'delivered'
GROUP BY DATE_TRUNC('month', order_purchase_timestamp::timestamp)
ORDER BY month;
```

### 5. Customer Revenue Ranking

```sql
SELECT
    customer_unique_id,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(total_order_value)::numeric, 2) AS total_revenue,

    RANK() OVER (
        ORDER BY SUM(total_order_value) DESC
    ) AS revenue_rank

FROM analytical_order_level
WHERE order_status = 'delivered'
GROUP BY customer_unique_id
ORDER BY revenue_rank
LIMIT 20;
```

### 6. Repeat Customers

```sql
SELECT
    COUNT(*) AS repeat_customers
FROM (
    SELECT
        customer_unique_id
    FROM analytical_order_level
    WHERE order_status = 'delivered'
    GROUP BY customer_unique_id
    HAVING COUNT(DISTINCT order_id) > 1
) AS customers;
```

---

# 👥 Customer Analytics & RFM Segmentation

Customer behavior was analyzed using **RFM segmentation**.

## RFM Framework

| Metric | Meaning |
|---|---|
| **Recency** | How recently the customer purchased |
| **Frequency** | How frequently the customer purchased |
| **Monetary** | How much the customer spent |

Customers were segmented into:

```text
🏆 Champions
💎 Loyal Customers
🌱 Potential Loyalists
⚠️ At Risk
❌ Lost Customers
```

The project report explicitly defines these five RFM segments.

### Business use

RFM segmentation can help businesses:

- Identify high-value customers
- Improve customer retention
- Target inactive customers
- Develop loyalty campaigns
- Identify customers with growth potential
- Prioritize personalized marketing

---

# 📊 Power BI Dashboard

The Power BI solution contains **three interactive dashboard pages**.

The dashboard output reports approximately:

```text
Total Revenue       → 15.42M
Total Orders        → 96K
Total Customers     → 93K
Average Order Value → 159.83
Average Review      → 4.09
```

These values are visible in the generated Power BI dashboard.

---

# 📄 Page 1 — Executive Overview

### KPIs

- Total Revenue
- Total Orders
- Total Customers
- Average Order Value
- Average Review Score
- On-Time Delivery %

### Visualizations

- Monthly Revenue Trend
- Revenue by Product Category
- Revenue by Customer State
- Orders by Status

The dashboard provides a management-level view of sales, customer and delivery performance.

### Dashboard Preview

> <img width="1377" height="784" alt="1" src="https://github.com/user-attachments/assets/96f57d87-6f36-401e-b63b-7a6a8d72ffdf" />


```text
![Executive Overview](images/powerbi-executive-overview.png)
```

---

# 📄 Page 2 — Customer Analytics

### Visualizations

- One-Time vs Repeat Customers
- Revenue by Customer Segment
- Average Order Value
- Customer Distribution by State
- Top 10 Customers
- RFM Customer Segmentation

The Power BI output shows approximately **90.56K one-time customers and 2.8K repeat customers** in the displayed analysis.

### RFM Segments

```text
Champions
Loyal Customers
Potential Loyalists
At Risk
Lost Customers
```

### Dashboard Preview

> <img width="1374" height="789" alt="2" src="https://github.com/user-attachments/assets/5f38b383-0c6b-4628-928b-8bbe190994f8" />


```text
![Customer Analytics](images/powerbi-customer-analytics.png)
```

---

# 📄 Page 3 — Delivery & Product Performance

### Visualizations

- Average Delivery Time
- Late Delivery %
- Delivery Delay Distribution
- Review Score vs Delivery Delay
- Category-wise Average Review Score
- Top Product Categories
- Bottom Product Categories

The dashboard includes delivery delay buckets ranging from early delivery through severe late delivery and compares review scores with delivery delays.

### Dashboard Preview

> <img width="1377" height="776" alt="3" src="https://github.com/user-attachments/assets/f8e1b5e3-b361-4d96-abe2-5809c75e0377" />


```text
![Delivery and Product Performance](images/powerbi-delivery-product-performance.png)
```

---

# 📈 Key Dashboard Metrics

Based on the generated Power BI dashboard:

| KPI | Value |
|---|---:|
| Total Revenue | **15.42M** |
| Total Orders | **96K** |
| Total Customers | **93K** |
| Average Order Value | **159.83** |
| Average Review Score | **4.09** |

The dashboard also shows **delivered orders as the dominant order status**, accounting for approximately 97% of displayed orders.

---

# 📊 Product Category Analysis

The Power BI dashboard identifies leading categories including:

- Health & Beauty
- Watches & Gifts
- Bed Bath Table
- Sports & Leisure
- Computers & Accessories
- Furniture & Decor
- Housewares
- Cool Stuff
- Auto
- Garden Tools

The dashboard's revenue-by-category visual shows **health_beauty** as the leading displayed category.

---

# 🚚 Delivery Performance

Delivery analysis focuses on:

```text
Delivery Days
Estimated Delivery Days
Delivery Delay Days
Delivery Status
Review Score
```

### Delivery analysis questions

- How long do customers typically wait?
- What percentage of orders are late?
- Which orders experience significant delays?
- Does delivery delay affect review scores?
- Which categories receive stronger reviews?

---

# 📦 Product Performance

Product performance is evaluated using:

```text
Revenue
Order Count
Average Review Score
Product Category
```

The dashboard provides both **top and bottom product category** views, allowing management to identify high-performing and weaker categories.

---

# 🗃️ Project Structure

```text
E-Commerce-Sales-and-Customer-Analytics/
│
├── Data/
│   ├── raw/
│   │   ├── olist_orders_dataset.csv
│   │   ├── olist_order_items_dataset.csv
│   │   ├── olist_order_payments_dataset.csv
│   │   ├── olist_order_reviews_dataset.csv
│   │   ├── olist_products_dataset.csv
│   │   ├── olist_customers_dataset.csv
│   │   ├── olist_sellers_dataset.csv
│   │   └── olist_product_category_name_translation.csv
│   │
│   └── processed/
│       └── analytical_order_level.csv
│
├── Python/
│   ├── data_cleaning.py
│   ├── feature_engineering.py
│   ├── eda.py
|   ├── delivery_analysis.py
│   └── loader.py
│
├── SQL/
│   └── analytical_order_level.sql
│
├── PowerBI/
|   ├── E-Commerce Sales & Analytics.pbix
|   ├── E-Commerce Sales & Analytics.pdf
|   ├── 1.png
|   ├── 2.png
│   └── 3.png
│
├── Project_Report.pdf│
│
└── README.md
```

---

# 🔍 Skills Demonstrated

### Data Analytics

- Exploratory Data Analysis
- Data Cleaning
- Data Transformation
- Feature Engineering
- Business Analytics
- Customer Analytics
- Delivery Analytics

### Python

- Python
- Pandas
- Data manipulation
- Data quality analysis
- Feature engineering

### SQL

- PostgreSQL
- Aggregations
- GROUP BY
- CASE statements
- CTEs
- Window functions
- RANK()
- Customer segmentation
- Business-oriented SQL analysis

### Power BI

- Data modeling
- DAX
- KPI cards
- Interactive dashboards
- Slicers
- Maps
- Time-series analysis
- Customer segmentation
- RFM analysis

---

# 💡 Business Insights Generated

The project enables management to answer important questions such as:

### Sales

> Which months and categories generate the most revenue?

### Customers

> Who are the highest-value customers?

### Retention

> How many customers return and purchase again?

### RFM

> Which customers should receive retention or loyalty campaigns?

### Delivery

> Where are delivery delays occurring?

### Customer Satisfaction

> Does delivery performance appear to influence review scores?

### Products

> Which categories generate high revenue and strong reviews?

---

# 🚀 Future Improvements

Potential extensions include:

- Customer Lifetime Value (CLV)
- Churn prediction
- Sales forecasting
- Delivery-delay prediction
- Customer propensity modeling
- Product recommendation system
- Cohort analysis
- Geographic delivery analysis
- Automated Power BI refresh
- Advanced Tableau dashboards
- Machine learning for customer segmentation

---

# 📌 Portfolio Highlights

This project demonstrates an end-to-end ability to:

```text
Collect
  ↓
Clean
  ↓
Transform
  ↓
Analyze
  ↓
Query
  ↓
Segment
  ↓
Visualize
  ↓
Communicate Insights
```

It combines **Python + Pandas + PostgreSQL + Power BI + DAX** into one business-focused analytics workflow.

---

**Srujana Manognya D**

Aspiring Data Analyst | Python | SQL | Power BI | Tableau | Excel

### Connect

- GitHub: (https://github.com/SrujanaManognya)
- Email: srujanadunna@gmail.com
