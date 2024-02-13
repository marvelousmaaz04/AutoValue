import pandas as pd

# Read the CSV file into a DataFrame
file_path = 'separated_csvs/combined_unique_entries.csv'  # Replace with the actual path to your CSV file
df = pd.read_csv(file_path)

# Get unique company names
unique_companies = df['Company'].unique()

# Get the total count of unique company names
total_unique_count = len(unique_companies)

# Print the unique company names and total count
print("Unique Company Names:", unique_companies)
print("Total Unique Company Names Count:", total_unique_count)

company_counts = df['Company'].value_counts()

# Print the company counts
print("Company Counts:")
print(company_counts)
