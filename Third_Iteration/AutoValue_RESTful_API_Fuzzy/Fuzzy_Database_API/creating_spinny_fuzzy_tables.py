import sqlite3

def create_fts_table():
    conn = sqlite3.connect('all_spinny_car_listings_fuzzy.db')
    cursor = conn.cursor()

    # Create the FTS virtual table
    cursor.execute('''
        CREATE VIRTUAL TABLE IF NOT EXISTS spinny_mumbai_fts
        USING fts5(ListingID, CarName, Price, Year, KilometersDriven, FuelType, Location, ListingURL, ImageURL, tokenize = "unicode61 remove_diacritics 2");
    ''')

    # Copy data from the original table to the FTS virtual table
    cursor.execute('''
        INSERT INTO spinny_mumbai_fts (ListingID, CarName, Price, Year, KilometersDriven, FuelType, Location, ListingURL, ImageURL)
        SELECT ListingID, CarName, Price, Year, KilometersDriven, FuelType, Location, ListingURL, ImageURL
        FROM spinny_mumbai;
    ''')
    cursor.execute('''
        CREATE VIRTUAL TABLE IF NOT EXISTS spinny_pune_fts
        USING fts5(ListingID, CarName, Price, Year, KilometersDriven, FuelType, Location, ListingURL, ImageURL, tokenize = "unicode61 remove_diacritics 2");
    ''')

    # Copy data from the original table to the FTS virtual table
    cursor.execute('''
        INSERT INTO spinny_pune_fts (ListingID, CarName, Price, Year, KilometersDriven, FuelType, Location, ListingURL, ImageURL)
        SELECT ListingID, CarName, Price, Year, KilometersDriven, FuelType, Location, ListingURL, ImageURL
        FROM spinny_pune;
    ''')
    cursor.execute('''
        CREATE VIRTUAL TABLE IF NOT EXISTS spinny_hyderabad_fts
        USING fts5(ListingID, CarName, Price, Year, KilometersDriven, FuelType, Location, ListingURL, ImageURL, tokenize = "unicode61 remove_diacritics 2");
    ''')

    # Copy data from the original table to the FTS virtual table
    cursor.execute('''
        INSERT INTO spinny_hyderabad_fts (ListingID, CarName, Price, Year, KilometersDriven, FuelType, Location, ListingURL, ImageURL)
        SELECT ListingID, CarName, Price, Year, KilometersDriven, FuelType, Location, ListingURL, ImageURL
        FROM spinny_hyderabad;
    ''')
    cursor.execute('''
        CREATE VIRTUAL TABLE IF NOT EXISTS spinny_bangalore_fts
        USING fts5(ListingID, CarName, Price, Year, KilometersDriven, FuelType, Location, ListingURL, ImageURL, tokenize = "unicode61 remove_diacritics 2");
    ''')

    # Copy data from the original table to the FTS virtual table
    cursor.execute('''
        INSERT INTO spinny_bangalore_fts (ListingID, CarName, Price, Year, KilometersDriven, FuelType, Location, ListingURL, ImageURL)
        SELECT ListingID, CarName, Price, Year, KilometersDriven, FuelType, Location, ListingURL, ImageURL
        FROM spinny_bangalore;
    ''')
    cursor.execute('''
        CREATE VIRTUAL TABLE IF NOT EXISTS spinny_delhi_fts
        USING fts5(ListingID, CarName, Price, Year, KilometersDriven, FuelType, Location, ListingURL, ImageURL, tokenize = "unicode61 remove_diacritics 2");
    ''')

    # Copy data from the original table to the FTS virtual table
    cursor.execute('''
        INSERT INTO spinny_delhi_fts (ListingID, CarName, Price, Year, KilometersDriven, FuelType, Location, ListingURL, ImageURL)
        SELECT ListingID, CarName, Price, Year, KilometersDriven, FuelType, Location, ListingURL, ImageURL
        FROM spinny_delhi;
    ''')

    conn.commit()
    conn.close()

# Create the FTS table (run this only once)
create_fts_table()
