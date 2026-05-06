# 🍬 Nassau Candy Distributor — Profitability Dashboard

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)

## 📌 Project Overview
The **Nassau Candy Profitability Dashboard** is an interactive, data-driven web application built with Python and Streamlit. It serves as a comprehensive business intelligence tool designed to analyze product line profitability, margin performance, supply chain logistics, and future sales forecasts. 

This dashboard features a heavily customized "Ocean Fresh" UI theme and transforms raw order data into actionable business insights.

## ✨ Key Features
The dashboard is separated into 7 core analytical modules:

- **📊 Product Overview:** View a product margin leaderboard, gross profit share (donut chart), and monthly sales/profit trend tracking.
- **🏭 Division Performance:** Deep dive into revenue and profit breakdowns across divisions (Chocolate, Sugar, Other) and regional distribution.
- **🔬 Cost Diagnostics:** Identify margin risks and pricing inefficiencies through cost vs. sales scatter plots and "Health Status" flags (🔴 / 🟡 / 🟢).
- **📈 Profit Concentration:** An 80/20 Pareto analysis highlighting the exact products driving the majority of revenue and profit, supplemented with an interactive Treemap.
- **📅 Year-over-Year (YoY):** Direct comparison of performance metrics across historical years (e.g., 2024 vs 2025) with variance tracking.
- **🔮 Forecasting:** Projects 6 months of future sales and profit utilizing a custom **Ordinary Least Squares (OLS) Linear Regression** model built from scratch. Includes 95% confidence intervals and $R^2$ scoring.
- **🚢 Shipping Routes:** An interactive geospatial map that visualizes logistics. Calculates distances using the Haversine formula and generates simulated delivery timelines from factory dispatch to final customer delivery.

## 🛠️ Technology Stack
- **Frontend & Backend Framework:** [Streamlit](https://streamlit.io/)
- **Data Manipulation & Math:** Pandas, NumPy
- **Interactive Visualizations:** Plotly Express, Plotly Graph Objects
- **Styling:** Custom injected CSS (Glassmorphism, gradients, custom fonts)

## 🚀 How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR-USERNAME/Product-Line-Profitability-Margin-Performance-Analysis-for-Nassau-Candy-Distributor
.git
   cd "Product-Line-Profitability-Margin-Performance-Analysis-for-Nassau-Candy-Distributor"
   ```

2. **Install the dependencies:**
   Make sure you have Python installed, then run:
   ```bash
   pip install -r requirements.txt
   ```
   *(Required packages include `streamlit`, `pandas`, `numpy`, `plotly`, and an Excel engine like `openpyxl` or `xlrd`)*

3. **Ensure Data is Present:**
   Place your dataset named `Nassau_Candy_Distributor.csv` or `Nassau_Candy_Distributor.xlsx` in the root directory.

4. **Launch the Dashboard:**
   ```bash
   python -m streamlit run app.py
   ```

## 📸 UI Theme ("Ocean Fresh")
The project bypasses standard Streamlit aesthetics by injecting raw CSS to achieve an "Ocean Fresh" theme. This includes:
- Deep navy/blue gradient backgrounds.
- Cyan and turquoise accents.
- Custom KPI cards with subtle borders.
- Styled DataFrame tables and metric badges.
