import pandas as pd
import numpy as py

# Input CSV file path
input_csv_path = 'COW_Trade_4.0\\Dyadic_COW_4.0.csv'

# Output CSV file path for filtered data
output_csv_path = 'select_years_raw_data.csv'

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(input_csv_path, delimiter=",",header=0)
print("test 1\n")
#columns_to_remove = ['IPEDSCOUNT1','IPEDSCOUNT2']

# filtered_df = df[df['EARN_MDN_1YR'] != "PrivacySuppressed"]
# filtered_df = filtered_df[df['EARN_MDN_4YR'] != "PrivacySuppressed"]
# columns_to_keep = [col for col in df.columns if 'BBRR' not in col]
# filtered_df = df[columns_to_keep]
values_to_filter = [1939,1940,1941,1942,1943,1944,1945]

# Apply your filtering logic, for example, let's say you want to filter rows where column 'A' is greater than 10
filtered_df = df[df['year'].isin(values_to_filter)]
print("test 2\n")
# filtered_df = df.drop(columns=columns_to_remove)
# filtered_df = filtered_df[df['IPEDSCOUNT1'].notnull()]
# filtered_df = filtered_df[df['IPEDSCOUNT2'].notnull()]
# filtered_df = df.groupby('CIPDESC').mean().reset_index()
# df['NUM_GRADUATES_2YR'] = df['IPEDSCOUNT1'] + df['IPEDSCOUNT2']
# filtered_df = df
# filtered_df = filtered_df.drop(columns=columns_to_remove)

# Assuming 'COLUMN_TO_SUM' is the column you want to sum
# and other columns are the ones you want to average
"""agg_dict = {
    'NUM_GRADUATES_2YR': 'sum',
    'EARN_MDN_1YR': 'mean',
    'EARN_MDN_4YR': 'mean',
    'CIPCODE': 'mean'
}"""

# filtered_df = filtered_df.groupby('CIPDESC').agg(agg_dict).reset_index()
# filtered_df['CIPDESC'] = filtered_df['CIPDESC'].str.rstrip('.')

# Save the filtered DataFrame to a new CSV file
filtered_df.to_csv(output_csv_path, index=False)

#print(f"Filtered data saved to {output_csv_path}")
