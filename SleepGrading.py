import pandas as pd

def calculate_sleep_scores(df):
    df.fillna(0, inplace=True)

    # Compute raw numeric sleep score
    df['raw_sleep_score'] = (
        0.5 * df['sleep_deep_duration'] +
        0.3 * df['sleep_rem_duration'] -
        0.2 * df['sleep_awake_duration'] +
        0.5 * df['duration']
    )

    # Calculate score thresholds
    thresholds = {
        'good': df['raw_sleep_score'].quantile(0.66),
        'average': df['raw_sleep_score'].quantile(0.33)
    }

    # Assign sleep quality labels
    def categorize_sleep(score):
        if score >= thresholds['good']:
            return "Good"
        elif score >= thresholds['average']:
            return "Average"
        else:
            return "Bad"

    df['sleep_quality'] = df['raw_sleep_score'].apply(categorize_sleep)
    df['sleep_score'] = df['raw_sleep_score'].round(2)  # For modeling

    return df

def add_nap_flag(df):
    df['bedtime'] = pd.to_datetime(df['bedtime'])
    df['wake_up_time'] = pd.to_datetime(df['wake_up_time'])
    df['date'] = df['bedtime'].dt.date

    nap_dates = set()

    for date, group in df.groupby('date'):
        has_nap = False
        for idx, row in group.iterrows():
            start = row['bedtime'].hour
            end = row['wake_up_time'].hour
            if 11 <= start <= 17 and 11 <= end <= 17:
                has_nap = True
                break
        if has_nap:
            nap_dates.add(date)

    df['took_nap'] = df['date'].isin(nap_dates)
    df['date'] = pd.to_datetime(df['date'])  # Ensure date is datetime
    return df


# === MAIN ===

# Load sleep data
sleep_df = pd.read_csv("Data\sleep.csv")

# Step 1: Score + label sleep quality
scored_sleep_df = calculate_sleep_scores(sleep_df)

# Step 2: Add took_nap flag
final_sleep_df = add_nap_flag(scored_sleep_df)

# Save processed file
final_sleep_df.to_csv("sleep_processed.csv", index=False)
print("Done! Saved to 'sleep_processed.csv'")