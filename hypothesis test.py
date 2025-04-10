import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import f_oneway
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import statsmodels.api as sm
from statsmodels.formula.api import ols

# Change font of plots
font = {'weight' : 'bold',
        'size'   : 22}
plt.rc('font', **font)

# Load data
df = pd.read_csv(r"C:\Users\schal\Downloads\combined_model_ready_all.csv")

# Drop rows with missing key data
df = df.dropna(subset=["sleep_quality", "total_steps", "total_screen_time"])

# Convert sleep_quality to numeric if necessary
sleep_map = {"Bad": 0, "Average": 1, "Good": 2}
if df["sleep_quality"].dtype == object:
    df["sleep_quality"] = df["sleep_quality"].map(sleep_map)

# Group data by sleep quality
grouped_steps = [group["total_steps"].dropna() for name, group in df.groupby("sleep_quality")]
grouped_screen = [group["total_screen_time"].dropna() for name, group in df.groupby("sleep_quality")]

# --- ANOVA Tests ---
print("\n--- ANOVA Results ---")

# Steps ANOVA
f_steps, p_steps = f_oneway(*grouped_steps)
print(f"Total Steps: F = {f_steps:.2f}, p = {p_steps:.4f}")

# Screen Time ANOVA
f_screen, p_screen = f_oneway(*grouped_screen)
print(f"Total Screen Time: F = {f_screen:.2f}, p = {p_screen:.4f}")

# --- Visualizations ---
plt.figure(figsize=(14, 6))

# Steps boxplot
sns.boxplot(x="sleep_quality", y="total_steps", data=df, palette="pastel")
plt.title("Total Steps by Sleep Quality")
plt.xlabel("Sleep Quality")
plt.ylabel("Total Steps")
plt.xticks([0, 1, 2], ["Bad", "Average", "Good"])
plt.show()

# Screen Time boxplot
sns.boxplot(x="sleep_quality", y="total_screen_time", data=df, palette="pastel")
plt.title("Screen Time by Sleep Quality")
plt.xlabel("Sleep Quality")
plt.ylabel("Screen Time (min)")
plt.xticks([0, 1, 2], ["Bad", "Average", "Good"])

plt.tight_layout()
plt.show()
