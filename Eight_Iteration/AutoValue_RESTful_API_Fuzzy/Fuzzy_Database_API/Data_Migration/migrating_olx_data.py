import sqlite3
import csv

# Connect to SQLite database
conn = sqlite3.connect('all_olx_car_listings_fuzzy.db')
cursor = conn.cursor()

# Execute a SELECT query to retrieve data from the table
# cursor.execute('SELECT * FROM spinny_mumbai')
cursor.execute('SELECT * FROM olx_hyderabad')

# Fetch all rows from the result set
rows = cursor.fetchall()

# Specify the path for the CSV file
csv_file_path = 'olx_csvs/olx_hyderabad.csv'

# Write data to the CSV file
with open(csv_file_path, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    # Write header row with column names
    csv_writer.writerow([description[0] for description in cursor.description])
    # Write data rows
    csv_writer.writerows(rows)

# Close database connection
conn.close()
