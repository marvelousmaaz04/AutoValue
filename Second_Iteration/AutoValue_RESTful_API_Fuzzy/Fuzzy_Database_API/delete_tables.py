import sqlite3

def delete_fts_table():
    conn = sqlite3.connect('all_car_listings_fuzzy.db')
    cursor = conn.cursor()

    # Create the FTS virtual table
    cursor.execute('''
     DROP TABLE IF EXISTS spinny_mumbai_fts;
    ''')


    conn.commit()
    conn.close()

# Create the FTS table (run this only once)
delete_fts_table()
