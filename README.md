# 🎯 Video Game Market Analysis Dashboard
### Advanced Exploratory Data Analysis, SQL Pipeline & Feature Engineering Case Study

![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)
![Pandas](https://img.shields.io/badge/pandas-data%20analysis-orange)
![SQL](https://img.shields.io/badge/SQL-pandasql-lightgrey)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)

## 📖 Project Overview
This project is an end-to-end data analytics and business intelligence case study investigating regional consumer buying behaviors, historical market lifecycle shifts, and overarching industry metrics within the global video game industry. 

Using an curated historical dataset spanning over **16,000 game titles**, this project transcends basic data parsing syntax to deliver functional corporate market research, structured SQL pipelines, custom feature engineering, and an interactive business analytics dashboard.

---

## 🛠️ Tech Stack & Technical Competencies
*   **Core Languages:** Python, SQL (via `pandasql` engine)
*   **Data Manipulation:** Pandas, NumPy
*   **Data Visualization:** Matplotlib, Seaborn
*   **Deployment Interface:** Streamlit Engine
*   **Applied Data Architecture Matrix:**
    *   **Data Integrity Protocol:** Parsing null structural vectors (`Year`, `Publisher`), outlier math evaluation via Interquartile Range ($IQR$), and data type casting.
    *   **SQL Pipeline Ingestion:** Complex multi-aggregations, `HAVING` filters, conditional aggregations, and performance-centric queries.
    *   **Statistical Data Processing:** Identifying power-law (long-tail) distributions, multi-variable Pearson correlation matrices, and computing data skewness.
    *   **Feature Engineering Execution:** Era categorization bins, regional revenue concentration metrics (`Market_Strategy`), and character string structural impacts.

---

## 📈 Key Analytical Insights & Takeaways

1. **The Long-Tail Reality:** Global sales exhibit an extreme right-skewed Power Law distribution ($\text{Mean: } \$0.54\text{M} \gg \text{Median: } \$0.17\text{M}$). Budgeting protocols must align with median performance baselines rather than high-skew averages.
2. **Western Market Scalability:** The Western landscape (NA + EU) controls **76.44%** of aggregate global game software revenue. 
3. **Regional Strategic Anomalies:** Japan isolates as an explicit standalone vector, heavily prioritizing Role-Playing Games (RPGs) and handheld ecosystems relative to Western markets.
4. **Title Impact:** Title structural character length yields a near-zero correlation score ($-0.07$) relative to total global revenue.

---

## 🚀 Running the Streamlit App Locally

### 1. Prerequisites
Ensure you have Python 3.9 or higher installed.

### 2. Clone and Setup Environment
```bash
# Clone this repository
git clone [https://github.com/roshankshah2005-creator/video-game-market-analysis.git](https://github.com/your-username/video-game-market-analysis.git)
cd video-game-market-analysis

# Install dependencies
pip install pandas>=2.0.0 numpy>=1.24.0 matplotlib>=3.7.0 seaborn>=0.12.0
