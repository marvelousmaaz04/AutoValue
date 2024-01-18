import pandas as pd
import os
print("Current Working Directory:", os.getcwd())
# List of file names
file_names = [ "separated_csvs/spinny_bangalore_separated.csv","separated_csvs/spinny_delhi_separated.csv", "separated_csvs/spinny_hyderabad_separated.csv", "separated_csvs/spinny_mumbai_separated.csv", "separated_csvs/spinny_pune_separated.csv"]

# Initialize an empty DataFrame to store all entries
all_entries_df = pd.DataFrame(columns=['Company', 'CarName'])

# Loop through each file
for file_name in file_names:
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_name)
    
    # Use regular expression to remove patterns like '1.5 VX', ' 1.2 S', '1.2L EX' and everything after
    df['CarName'] = df['CarName'].str.replace(r'\b\d+(\.\d+)?[^\w]*\w*\b.*$', '', regex=True).str.strip()
    
    # Concatenate the current DataFrame to the all_entries_df
    all_entries_df = pd.concat([all_entries_df, df], ignore_index=True)

# Drop duplicates from the combined DataFrame
unique_entries_df = all_entries_df.drop_duplicates()

# Write the unique entries to a new CSV file
unique_entries_df.to_csv("separated_csvs/combined_unique_entries.csv", index=False)
