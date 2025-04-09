import pandas as pd

# File paths
file1 = "C:\Python\Visualization Assignment\FieldDataAcquisition\ModelReadyFiles\model_ready_steps_sleep.csv"
file2 = "C:\Python\Visualization Assignment\FieldDataAcquisition\ModelReadyFiles\model_ready_steps_sleep_sander.csv.xls"

# Read the CSVs (they have .xls extensions but are actually CSV)
df1 = pd.read_csv(file1)
df2 = pd.read_csv(file2)

# Merge the dataframes
merged_df = pd.concat([df1, df2], ignore_index=True)

# Drop exact duplicate rows
merged_df = merged_df.drop_duplicates()

# Save the cleaned merged data
merged_df.to_csv("merged_steps_sleep_clean.csv", index=False)

print("Merged file saved as merged_steps_sleep_clean.csv")
