import pandas as pd
import re

# Load the Excel file
xls = pd.ExcelFile("Data\Screen_Data.xlsx")

# Load sheets
usage_time_df = xls.parse("Usage Time")
unlocks_df = xls.parse("Device Unlocks")

# === STEP 1: Clean usage_time_df ===

# Get device name from second column of first row
device_name = usage_time_df.iloc[0, 1]

# Drop last 3 rows (footer/system junk)
usage_time_df = usage_time_df[:-3]

# Rename column
usage_time_df.rename(columns={"Unnamed: 0": "app"}, inplace=True)

# --- Time parser function ---
def parse_time(t):
    if isinstance(t, str):
        hours = re.search(r"(\d+)h", t)
        minutes = re.search(r"(\d+)m", t)
        seconds = re.search(r"(\d+)s", t)
        total_seconds = 0
        if hours:
            total_seconds += int(hours.group(1)) * 3600
        if minutes:
            total_seconds += int(minutes.group(1)) * 60
        if seconds:
            total_seconds += int(seconds.group(1))
        return total_seconds / 60
    return 0

# === STEP 2: Total screen time from "Total Usage" ===
total_row = usage_time_df[usage_time_df["app"] == "Total Usage"].drop(columns=["app"])
date_columns = [pd.to_datetime(col, format="%B %d, %Y", errors="coerce") for col in total_row.columns]
total_times = total_row.iloc[0].apply(parse_time)
total_screen_time_df = pd.DataFrame({
    "date": date_columns,
    "total_screen_time": total_times.values
})

# === STEP 3: App-specific screen time ===
social_media_apps = ["Instagram", "YouTube", "X", "TikTok", "Snapchat"]
game_apps = ["Brawl Stars", "Clash of Clans", "8 Ball Pool", "Squad Busters"]

# Melt the dataframe and parse time
melted = usage_time_df.melt(id_vars=["app"], var_name="date", value_name="time")
melted["date"] = pd.to_datetime(melted["date"], format="%B %d, %Y", errors='coerce')
melted["time_minutes"] = melted["time"].apply(parse_time)

# Calculate social media usage
social_media_usage = melted[melted['app'].isin(social_media_apps)].pivot_table(
    index="date",
    columns="app",
    values="time_minutes",
    aggfunc="sum"
).fillna(0).reset_index()

# Calculate game usage
game_usage = melted[melted['app'].isin(game_apps)].pivot_table(
    index="date",
    columns="app",
    values="time_minutes",
    aggfunc="sum"
).fillna(0).reset_index()

# === STEP 4: Process Device Unlocks ===

# Remove footer rows (e.g., "Created by StayFree", etc.)
unlocks_df = unlocks_df.dropna(subset=["Unnamed: 0"])

# Extract unlock counts
unlock_row = unlocks_df.iloc[0].drop("Unnamed: 0")
unlock_dates = [pd.to_datetime(date, format="%B %d, %Y", errors='coerce') for date in unlock_row.index]
unlock_df = pd.DataFrame({
    "date": unlock_dates,
    "unlock_count": unlock_row.values
})

# === STEP 5: Merge everything ===
screen_summary = pd.merge(total_screen_time_df, social_media_usage, on="date", how="outer")
screen_summary = pd.merge(screen_summary, game_usage, on="date", how="outer")
screen_summary = pd.merge(screen_summary, unlock_df, on="date", how="outer")

# Add device info
screen_summary["device"] = device_name

# Fill missing app usage with 0
for app in social_media_apps + game_apps:
    if app not in screen_summary.columns:
        screen_summary[app] = 0.0

# === STEP 6: Calculate ratios ===

# Calculate social media time to total screen time ratio
screen_summary["social_media_time"] = screen_summary[social_media_apps].sum(axis=1)
screen_summary["social_media_ratio"] = screen_summary["social_media_time"] / screen_summary["total_screen_time"]

# Calculate game time to total screen time ratio
screen_summary["game_time"] = screen_summary[game_apps].sum(axis=1)
screen_summary["game_ratio"] = screen_summary["game_time"] / screen_summary["total_screen_time"]

# Final touches
screen_summary = screen_summary.sort_values("date")

# Save to CSV
screen_summary.to_csv("Data\screen_cleaned_with_ratios.csv", index=False)
print("Saved to 'screen_cleaned_with_ratios.csv'")