import pandas as pd
import json
from datetime import datetime


def epoch_to_datetime(epoch):
    return datetime.utcfromtimestamp(epoch).strftime('%Y-%m-%d %H:%M:%S')


def process_csv(file_path):
    # Load CSV file
    df = pd.read_csv(file_path)

    # Convert Time column from epoch format
    df['Time'] = df['Time'].apply(epoch_to_datetime)

    # Process the Value column
    expanded_data = []
    sleep_items_data = []
    sleepdata_id = 0
    for _, row in df.iterrows():
        value_dict = json.loads(row['Value'])  # Convert string to dictionary
        expanded_row = {
            'Uid': row['Uid'],
            'Sid': row['Sid'],
            'Key': row['Key'],
            'Time': row['Time']
        }

        for key, val in value_dict.items():
            if key in ['bedtime', 'device_wake_up_time', 'wake_up_time','device_bedtime']:
                expanded_row[key] = epoch_to_datetime(val)
            elif key == 'prontoTime':
                continue  # Drop prontoTime
            elif key == 'time':
                continue  # Drop duplicate time column
            elif key == 'items':
                for item in val:
                    item_row = item.copy()
                    item_row['sleepdata_id'] = sleepdata_id
                    item_row['Uid'] = row['Uid']
                    item_row['Sid'] = row['Sid']
                    sleep_items_data.append(item_row)
                expanded_row['sleepdata_id'] = sleepdata_id
                sleepdata_id += 1
            else:
                expanded_row[key] = val

        expanded_data.append(expanded_row)

    expanded_df = pd.DataFrame(expanded_data)

    # Create separate DataFrames
    keys = ['calories', 'heart_rate', 'sleep', 'steps', 'spo2']  # Added 'spo2'
    key_dfs = {}
    for key in keys:
        key_df = expanded_df[expanded_df['Key'] == key].copy()
        key_df.drop(columns=['Key'], inplace=True)
        key_df.reset_index(drop=True, inplace=True)
        key_df.dropna(axis=1, how='all', inplace=True)  # Drop empty columns
        key_dfs[key] = key_df

    # Create sleep items DataFrame
    sleep_items_df = pd.DataFrame(sleep_items_data)
    if not sleep_items_df.empty:
        sleep_items_df['start_time'] = sleep_items_df['start_time'].apply(epoch_to_datetime)
        sleep_items_df['end_time'] = sleep_items_df['end_time'].apply(epoch_to_datetime)

    return key_dfs, sleep_items_df



file_path = r'C:\Python\Visualization Assignment\FieldDataAcquisition\Data\20250321_8279399076_MiFitness_hlth_center_fitness_data.csv'  # Replace with your actual file
key_dataframes, sleep_items_df = process_csv(file_path)

# Saving to separate CSV files
for key, df in key_dataframes.items():
    df.to_csv(f'{key}.csv', index=False)


if not sleep_items_df.empty:
    sleep_items_df.to_csv('sleep_items.csv', index=False)