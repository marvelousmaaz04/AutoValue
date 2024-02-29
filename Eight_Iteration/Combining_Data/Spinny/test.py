import sqlite3

# Connect to the SQLite database (replace 'your_database.db' with your database file)
conn = sqlite3.connect('all_car_listings.db')
cursor = conn.cursor()

# Specify the table name you want to delete
table_name = 'spinny_delhi'

# Check if the table exists
cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
if cursor.fetchone() is not None:
    # The table exists; delete it
    cursor.execute(f"DROP TABLE {table_name}")
    print(f"Table '{table_name}' has been deleted.")
else:
    print(f"Table '{table_name}' does not exist.")

# Commit the changes and close the connection
conn.commit()
conn.close()
