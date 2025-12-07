import pandas as pd
import numpy as np

from scipy.stats import (
    ttest_ind,
    f_oneway,
    mannwhitneyu,
    wilcoxon,
    chi2_contingency,
    fisher_exact
)

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import os


def analyze_any_data(df):
    return {
        "basic_info": get_basic_info(df),
        "statistical_tests": run_statistics(df),
        "correlations": calculate_correlations(df),
        "plots": create_plots(df),
        "data_preview": df.head(10).to_dict("records")
    }


def get_basic_info(df):
    numeric_cols = list(df.select_dtypes(include=[np.number]).columns)
    categorical_cols = list(df.select_dtypes(exclude=[np.number]).columns)

    return {
        "rows": len(df),
        "columns": len(df.columns),
        "numeric_cols": numeric_cols,
        "categorical_cols": categorical_cols,
        "missing_values": df.isnull().sum().to_dict()
    }



def run_statistics(df):
    results = {}

    numeric = list(df.select_dtypes(include=[np.number]).columns)
    categorical = list(df.select_dtypes(exclude=[np.number]).columns)

 
    if len(numeric) >= 2:
        a = df[numeric[0]].dropna()
        b = df[numeric[1]].dropna()

        
        t, p = ttest_ind(a, b)
        results["t_test"] = make_test("T-Test (Independent)", numeric[0], numeric[1], t, p)

        u, p = mannwhitneyu(a, b)
        results["mann_whitney"] = make_test("Mann-Whitney U", numeric[0], numeric[1], u, p)

        
        size = min(len(a), len(b))
        w, p = wilcoxon(a[:size], b[:size])
        results["wilcoxon"] = make_test("Wilcoxon Signed Rank", numeric[0], numeric[1], w, p)


    if len(numeric) >= 1 and len(categorical) >= 1:
        num_col = numeric[0]
        cat_col = categorical[0]

        groups = [df[df[cat_col] == val][num_col].dropna() for val in df[cat_col].dropna().unique()]

        if len(groups) >= 2:
            f, p = f_oneway(*groups)
            results["anova"] = make_test(
                "ANOVA",
                f"{num_col} grouped by {cat_col}",
                "",
                f,
                p
            )

  
    if len(categorical) >= 2:
        col1, col2 = categorical[0], categorical[1]
        table = pd.crosstab(df[col1], df[col2])

        
        table = table.loc[(table != 0).any(axis=1), (table != 0).any(axis=0)]

        if table.shape[0] > 1 and table.shape[1] > 1:
            chi, p, _, _ = chi2_contingency(table)
            results["chi_square"] = make_test("Chi-Square", col1, col2, chi, p)

      
        if table.shape == (2, 2):
            odds, p = fisher_exact(table)
            results["fisher"] = make_test("Fisher Exact Test", col1, col2, odds, p)

    return results



def make_test(name, var1, var2, stat, p):
    return {
        "test": name,
        "variables": f"{var1} vs {var2}" if var2 else var1,
        "statistic": round(stat, 4),
        "p_value": round(p, 4),
        "significant": p < 0.05
    }



def calculate_correlations(df):
    numeric = df.select_dtypes(include=[np.number]).columns

    if len(numeric) < 2:
        return {}

    pearson = df[numeric].corr("pearson")
    spearman = df[numeric].corr("spearman")

    return {
        "pearson": {"top_pairs": pick_top_correlations(pearson)},
        "spearman": {"top_pairs": pick_top_correlations(spearman)}
    }


def pick_top_correlations(corr_matrix):
    pairs = []
    cols = corr_matrix.columns

    for i in range(len(cols)):
        for j in range(i + 1, len(cols)):
            val = corr_matrix.iloc[i, j]
            pairs.append({
                "var1": cols[i],
                "var2": cols[j],
                "correlation": round(val, 4),
                "abs_corr": abs(round(val, 4))
            })

    
    return sorted(pairs, key=lambda x: x["abs_corr"], reverse=True)[:10]


def create_plots(df):
    os.makedirs("static/plots", exist_ok=True)
    plots = []

    numeric = df.select_dtypes(include=[np.number]).columns


    for col in numeric[:6]:  
        plt.figure(figsize=(10, 6))
        df[col].hist(bins=20, color="skyblue", edgecolor="black")
        plt.title(f"Distribution of {col}")
        path = f"static/plots/dist_{col}.png"
        plt.savefig(path, dpi=100, bbox_inches="tight")
        plt.close()
        plots.append(f"plots/dist_{col}.png")

    
    if len(numeric) > 1:
        plt.figure(figsize=(12, 9))
        sns.heatmap(df[numeric].corr(), annot=True, cmap="coolwarm")
        path = "static/plots/correlation_heatmap.png"
        plt.savefig(path, dpi=100, bbox_inches="tight")
        plt.close()
        plots.append("plots/correlation_heatmap.png")

    return plots
