import pandas as pd

# === Load all data ===
sleep_df = pd.read_csv("Data/sleep_processed.csv", parse_dates=["bedtime"])
steps_df = pd.read_csv("Data/steps_cleaned.csv", parse_dates=["date"])
screen_df = pd.read_csv("Data/screen_cleaned_with_ratios.csv", parse_dates=["date"])

# --- Extract date from bedtime for merging ---
sleep_df["date"] = pd.to_datetime(sleep_df["bedtime"].dt.date)

# === Merge sleep + steps ===
merged_steps = pd.merge(sleep_df, steps_df, on="date", how="left")

# === Keep only relevant columns for step-only model ===
step_features = [
    "date",
    "total_steps",
    "steps_2h_before_sleep",
    "took_nap",
    "sleep_quality",
    "sleep_score"
]
model_steps_sleep = merged_steps[step_features].dropna(subset=["sleep_quality"])
model_steps_sleep.to_csv("model_ready_steps_sleep.csv", index=False)

# === Merge with screen data as well ===
merged_all = pd.merge(model_steps_sleep, screen_df, on="date", how="left")

# === Final features for full model ===
screen_features = step_features + [
    "total_screen_time",
    "unlock_count",
    "Instagram",
    "YouTube",
    "X",
    "TikTok",
    "Snapchat",
    "8 Ball Pool",
    "Brawl Stars",
    "Clash of Clans",
    "Squad Busters",
    "social_media_ratio",
    "game_ratio"
]
model_full = merged_all[screen_features].dropna(subset=["total_screen_time"])
model_full.to_csv("ModelReadyFiles/model_ready_all.csv", index=False)

print(" Saved: model_ready_steps_sleep.csv and model_ready_all.csv")