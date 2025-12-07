
Universal Data Analyzer - Project Documentation

Overview
The Universal Data Analyzer is a Python + Flask based web application that automatically analyzes any dataset uploaded by the user. It performs statistical tests, correlation analysis, visualizations, and generates a clean dashboard — without requiring the user to write any code.

Objectives
1. Upload any CSV or Excel dataset
2. Automatically detect numeric and categorical columns
3. Perform statistical tests:
   - Independent T-Test
   - Mann–Whitney U Test
   - Wilcoxon Signed-Rank Test
   - One-Way ANOVA
   - Chi-Square Test
   - Fisher’s Exact Test
4. Compute correlations:
   - Pearson
   - Spearman
5. Generate visualizations:
   - Histograms
   - Correlation heatmap
6. Display all results in a single dashboard

Workflow
1. User uploads CSV/Excel file
2. Flask receives and saves file
3. pandas loads file into DataFrame
4. System detects numeric & categorical columns
5. Performs statistical tests
6. Computes correlations
7. Generates histograms + heatmap
8. Combines everything into a result dictionary
9. Dashboard displays full analysis

Tools & Technologies
Backend: Python, Flask
Libraries: pandas, NumPy, SciPy, Matplotlib, Seaborn
Frontend: HTML, CSS, Jinja2 templates

Dataset Compatibility
Works with all dataset types:
- Numeric-only
- Categorical-only
- Mixed datasets
- Missing values
- Small or large datasets

Statistical Tests
T-Test, Mann–Whitney U, Wilcoxon, One-Way ANOVA, Chi-Square, Fisher’s Exact Test

Correlation Analysis
Pearson & Spearman correlations with top 10 strongest results.

Visualizations
Histograms (first 6 numeric columns)
Correlation Heatmap

How to Run
1. pip install flask pandas numpy scipy matplotlib seaborn
2. python app.py
3. Open http://127.0.0.1:5000
4. Upload any CSV/Excel file

