import pandas as pd
import matplotlib.pyplot as plt

# File paths
files = {
    "calories": "calories.csv",
    "heart_rate": "heart_rate.csv",
    "spo2": "spo2.csv",
    "steps": "steps.csv",
    "sleep": "sleep.csv"
}


# Read and process data
def process_data(file_path):
    df = pd.read_csv(file_path)
    df['Time'] = pd.to_datetime(df['Time'], errors='coerce')
    df = df[df['Time'].dt.date == pd.to_datetime("2025-02-26").date()]
    return df


# Generate plots
def plot_graph(df, x_col, y_col, title, xlabel, ylabel):
    plt.figure(figsize=(10, 5))
    plt.plot(df[x_col], df[y_col], marker='o', linestyle='-', markersize=4)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
    plt.grid()
    plt.show()


# Process and plot each dataset
for name, file_path in files.items():
    df = process_data(file_path)
    if df.empty:
        print(f"No data available for {name} on 26-02-2025.")
        continue

    if name == "calories":
        plot_graph(df, 'Time', 'calories', 'Calories Burned Over Time', 'Time', 'Calories')
    elif name == "heart_rate":
        plot_graph(df, 'Time', 'bpm', 'Heart Rate Over Time', 'Time', 'BPM')
    elif name == "spo2":
        plot_graph(df, 'Time', 'spo2', 'SpO2 Levels Over Time', 'Time', 'SpO2 (%)')
    elif name == "steps":
        plot_graph(df, 'Time', 'steps', 'Steps Count Over Time', 'Time', 'Steps')
    elif name == "sleep":
        # Bar chart for sleep stages
        plt.figure(figsize=(8, 5))
        sleep_stages = ['sleep_deep_duration', 'sleep_light_duration', 'sleep_rem_duration', 'sleep_awake_duration']
        df_sleep_stages = df[sleep_stages].sum()

        # Plot the bar chart with proper labels
        df_sleep_stages.plot(kind='bar', color=['blue', 'orange', 'green', 'red'])
        plt.title('Sleep Stages Duration for 26-02-2025')
        plt.ylabel('Duration (minutes)')
        plt.xticks(ticks=range(len(df_sleep_stages)), labels=sleep_stages, rotation=0)  # Set the correct labels on x-axis
        plt.grid(axis='y')
        plt.show()

        # Line graph for heart rate during sleep
        if 'avg_hr' in df.columns:
            plot_graph(df, 'Time', 'avg_hr', 'Heart Rate During Sleep', 'Time', 'Avg BPM')
