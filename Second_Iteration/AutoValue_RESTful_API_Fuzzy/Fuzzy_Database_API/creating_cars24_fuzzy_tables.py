import sqlite3

def create_fts_table():
    conn = sqlite3.connect('all_cars24_car_listings_fuzzy.db')
    cursor = conn.cursor()

    # Create the FTS virtual table
    cursor.execute('''
        CREATE VIRTUAL TABLE IF NOT EXISTS cars24_mumbai_fts
        USING fts5(ListingID, CarName, Price, Year, KilometersDriven, FuelType, Location, ListingURL, ImageURL, tokenize = "unicode61 remove_diacritics 2");
    ''')

    # Copy data from the original table to the FTS virtual table
    cursor.execute(''' 
        INSERT INTO cars24_mumbai_fts (ListingID, CarName, Price, Year, KilometersDriven, FuelType, Location, ListingURL, ImageURL)
        SELECT ListingID, CarName, Price, Year, KilometersDriven, FuelType, Location, ListingURL, ImageURL
        FROM cars24_mumbai;
    ''')
    cursor.execute('''
        CREATE VIRTUAL TABLE IF NOT EXISTS cars24_pune_fts
        USING fts5(ListingID, CarName, Price, Year, KilometersDriven, FuelType, Location, ListingURL, ImageURL, tokenize = "unicode61 remove_diacritics 2");
    ''')

    # Copy data from the original table to the FTS virtual table
    cursor.execute('''
        INSERT INTO cars24_pune_fts (ListingID, CarName, Price, Year, KilometersDriven, FuelType, Location, ListingURL, ImageURL)
        SELECT ListingID, CarName, Price, Year, KilometersDriven, FuelType, Location, ListingURL, ImageURL
        FROM cars24_pune;
    ''')
    cursor.execute('''
    
        CREATE VIRTUAL TABLE IF NOT EXISTS cars24_hyderabad_fts
        USING fts5(ListingID, CarName, Price, Year, KilometersDriven, FuelType, Location, ListingURL, ImageURL, tokenize = "unicode61 remove_diacritics 2");
    ''')

    # Copy data from the original table to the FTS virtual table
    cursor.execute('''
        INSERT INTO cars24_hyderabad_fts (ListingID, CarName, Price, Year, KilometersDriven, FuelType, Location, ListingURL, ImageURL)
        SELECT ListingID, CarName, Price, Year, KilometersDriven, FuelType, Location, ListingURL, ImageURL
        FROM cars24_hyderabad;
    ''')
    cursor.execute('''
        
        CREATE VIRTUAL TABLE IF NOT EXISTS cars24_bangalore_fts
        USING fts5(ListingID, CarName, Price, Year, KilometersDriven, FuelType, Location, ListingURL, ImageURL, tokenize = "unicode61 remove_diacritics 2");
    ''')

    # Copy data from the original table to the FTS virtual table
    cursor.execute('''
        INSERT INTO cars24_bangalore_fts (ListingID, CarName, Price, Year, KilometersDriven, FuelType, Location, ListingURL, ImageURL)
        SELECT ListingID, CarName, Price, Year, KilometersDriven, FuelType, Location, ListingURL, ImageURL
        FROM cars24_bangalore;
    ''')
    cursor.execute('''
        CREATE VIRTUAL TABLE IF NOT EXISTS cars24_newdelhi_fts
        USING fts5(ListingID, CarName, Price, Year, KilometersDriven, FuelType, Location, ListingURL, ImageURL, tokenize = "unicode61 remove_diacritics 2");
    ''')

    # Copy data from the original table to the FTS virtual table
    cursor.execute('''
        INSERT INTO cars24_newdelhi_fts (ListingID, CarName, Price, Year, KilometersDriven, FuelType, Location, ListingURL, ImageURL)
        SELECT ListingID, CarName, Price, Year, KilometersDriven, FuelType, Location, ListingURL, ImageURL
        FROM cars24_newdelhi;
    ''')

    conn.commit()
    conn.close()

# Create the FTS table (run this only once)
create_fts_table()
