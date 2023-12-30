import sqlite3

def create_fts_table():
    conn = sqlite3.connect('all_cars24_car_listings_copy.db')
    cursor = conn.cursor()

    # Create the FTS virtual table
    cursor.execute('''
        CREATE VIRTUAL TABLE IF NOT EXISTS cars24_mumbai_fts1
        USING fts5(CarName, tokenize = "unicode61 remove_diacritics 2");
    ''')

    # Copy data from the original table to the FTS virtual table
    cursor.execute('''
        INSERT INTO cars24_mumbai_fts (CarName)
        SELECT CarName FROM cars24_mumbai;
    ''')

    conn.commit()
    conn.close()

# Create the FTS table (run this only once)
create_fts_table()
