import pandas as pd

def read_and_print_csv(file_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)

    # Print unique values from the "CarName" column
    unique_car_names = df['CarName'].unique()
    # print(unique_car_names)
    print(len(unique_car_names))

    df = pd.read_csv(file_path)

    # Extract the unique values from the "CarName" column
    unique_car_names = df['CarName'].unique()

    # Calculate word lengths for unique entries
    word_lengths = pd.Series([len(str(x).split()) for x in unique_car_names])

    # Find the highest, lowest, and average word lengths
    highest_word_length = word_lengths.max()
    lowest_word_length = word_lengths.min()
    average_word_length = word_lengths.mean()

    # Print the results
    print("Unique CarName Word Lengths:")
    print(word_lengths)
    print("\nHighest Word Length:", highest_word_length)
    print("Lowest Word Length:", lowest_word_length)
    print("Average Word Length:", average_word_length)

    # Print the count of each word length
    word_length_counts = word_lengths.value_counts().sort_index()
    print("\nWord Length Counts:")
    print(word_length_counts)

# Example usage:
csv_file_path = 'cars24_mumbai.csv'  # Replace with the actual path to your CSV file
read_and_print_csv(csv_file_path)



def process_and_write_to_new_file(input_file_path, output_file_path):
    ## Read only the "CarName" column from the CSV file into a DataFrame
    df = pd.read_csv(input_file_path, usecols=['CarName'])

    # Extract the company name (first word) and create a new "Company" column
    df['Company'] = df['CarName'].apply(lambda x: str(x).split()[0] if len(str(x).split()) >= 1 else '')

    # Process the "CarName" column
    df['CarName'] = df['CarName'].apply(lambda x: ' '.join(str(x).split()[:4]) if len(str(x).split()) >= 4 else x)

    # Reorder the columns
    df = df[['Company', 'CarName']]

    # Drop duplicate rows based on "Company" and "CarName"
    df = df.drop_duplicates()

    # Write the modified DataFrame to a new CSV file
    df.to_csv(output_file_path, index=False)

# Example usage:
input_file_path = 'cars24_mumbai.csv'  # Replace with the actual path to your input CSV file
output_file_path = 'separated_csvs/cars24_mumbai_separated.csv'  # Replace with the desired output file path

process_and_write_to_new_file(input_file_path, output_file_path)

