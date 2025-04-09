import pandas as pd

# List of people
names = ['Boran', 'David', 'Sander']

# Initialize an empty DataFrame to store all the data
df_all = pd.DataFrame()

# Load and concatenate data for all people
for name in names:
    df = pd.read_csv(f'{name}/model_ready_all.csv')
    df_all = pd.concat([df_all, df], ignore_index=True)

# Save the concatenated data to a new CSV file
output_file = 'combined_model_ready_all.csv'
df_all.to_csv(output_file, index=False)

print(f"Successfully combined data from {len(names)} people into {output_file}")
print(f"Total number of samples: {len(df_all)}")