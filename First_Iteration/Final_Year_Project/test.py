import sqlite3
import os
import csv

# Connect to the SQLite database
conn = sqlite3.connect('all_car_listings.db')

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Execute a sample query to fetch data
cursor.execute("SELECT CarName FROM spinny_mumbai LIMIT 500")

# Fetch all the rows from the query result
rows = cursor.fetchall()

# Extract company and model from each row
car_info_list = [entry[0].split(' ', 1) for entry in rows]
car_companies, car_models = zip(*car_info_list)

# Print the extracted information

new_conn = sqlite3.connect('spinny_seperated.db')

# Create a cursor object to execute SQL queries
new_cursor = new_conn.cursor()

# Create a new table named 'car_info'
new_cursor.execute('''
    CREATE TABLE IF NOT EXISTS spinny_mumbai (
        company TEXT,
        model TEXT
    )
''')

csv_file = open('spinny_separated.csv', 'w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['company','model'])

for company, model in zip(car_companies, car_models):
    print(f"Company: {company}, Model: {model}")
    new_cursor.execute("INSERT INTO spinny_mumbai VALUES(?,?)",(company,company+' '+model))
    csv_writer.writerow([company,company+' '+model])



# Extracted car information

# Insert the data into the 'car_info' table


# Commit the changes and close the new connection
new_conn.commit()
new_conn.close()

# Close the cursor and connection
cursor.close()
conn.close()
csv_file.close()
