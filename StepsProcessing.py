import pandas as pd

# Load steps and processed sleep data
import pandas as pd

steps_df = pd.read_csv(r"Data/steps.csv")
sleep_df = pd.read_csv(r"Data/sleep_processed.csv")  # Or "sleep_processed.csv" if that's the actual name



# Convert time columns to datetime
steps_df['Time'] = pd.to_datetime(steps_df['Time'])
sleep_df['bedtime'] = pd.to_datetime(sleep_df['bedtime'])
sleep_df['wake_up_time'] = pd.to_datetime(sleep_df['wake_up_time'])

# Initialize an empty list to hold cleaned daily summaries
daily_steps_summary = []

# Iterate through each sleep session
for _, row in sleep_df.iterrows():
    sleep_date = row['bedtime'].date()
    uid = row['Uid']
    sid = row['Sid']
    bedtime = row['bedtime']
    wake_up = row['wake_up_time']
    two_hours_before_bed = bedtime - pd.Timedelta(hours=2)

    # Filter steps for this user and session's date
    mask = (
        (steps_df['Time'].dt.date == sleep_date) &
        (steps_df['Uid'] == uid) &
        (steps_df['Sid'] == sid)
    )
    steps_day = steps_df[mask].copy()

    # Filter out steps taken during sleep
    steps_awake = steps_day[
        (steps_day['Time'] < bedtime) | (steps_day['Time'] > wake_up)
    ]

    # Total steps (excluding sleep)
    total_steps = steps_awake['steps'].sum()

    # Steps in the 2h window before sleep
    steps_2h_before_sleep = steps_awake[
        (steps_awake['Time'] >= two_hours_before_bed) & (steps_awake['Time'] < bedtime)
    ]['steps'].sum()

    # Save summary
    daily_steps_summary.append({
        'date': sleep_date,
        'Uid': uid,
        'Sid': sid,
        'total_steps': total_steps,
        'steps_2h_before_sleep': steps_2h_before_sleep
    })

# Create dataframe from summaries
steps_summary_df = pd.DataFrame(daily_steps_summary)

# Save cleaned and aggregated steps data
steps_summary_df.to_csv("Data\steps_cleaned.csv", index=False)
print("Saved to 'steps_cleaned.csv'")