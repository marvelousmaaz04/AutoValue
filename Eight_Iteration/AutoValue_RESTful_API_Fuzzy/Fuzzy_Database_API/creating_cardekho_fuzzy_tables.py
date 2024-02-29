import sqlite3

def create_fts_table():
    conn = sqlite3.connect('all_cardekho_listings_fuzzy.db')
    cursor = conn.cursor()

    # Create the FTS virtual table
    cursor.execute('''
        CREATE VIRTUAL TABLE IF NOT EXISTS cardekho_mumbai_fts
        USING fts5(ListingID, CarName, Price, Year, KilometersDriven, FuelType, Location, ListingURL, ImageURL, tokenize = "unicode61 remove_diacritics 2");
    ''')

    # Copy data from the original table to the FTS virtual table
    cursor.execute('''
        INSERT INTO cardekho_mumbai_fts (ListingID, CarName, Price, Year, KilometersDriven, FuelType, Location, ListingURL, ImageURL)
        SELECT ListingID, CarName, Price, Year, KilometersDriven, FuelType, Location, ListingURL, ImageURL
        FROM cardekho_mumbai;
    ''')
    cursor.execute('''
        CREATE VIRTUAL TABLE IF NOT EXISTS cardekho_pune_fts
        USING fts5(ListingID, CarName, Price, Year, KilometersDriven, FuelType, Location, ListingURL, ImageURL, tokenize = "unicode61 remove_diacritics 2");
    ''')

    # Copy data from the original table to the FTS virtual table
    cursor.execute('''
        INSERT INTO cardekho_pune_fts (ListingID, CarName, Price, Year, KilometersDriven, FuelType, Location, ListingURL, ImageURL)
        SELECT ListingID, CarName, Price, Year, KilometersDriven, FuelType, Location, ListingURL, ImageURL
        FROM cardekho_pune;
    ''')
    cursor.execute('''
        CREATE VIRTUAL TABLE IF NOT EXISTS cardekho_hyderabad_fts
        USING fts5(ListingID, CarName, Price, Year, KilometersDriven, FuelType, Location, ListingURL, ImageURL, tokenize = "unicode61 remove_diacritics 2");
    ''')

    # Copy data from the original table to the FTS virtual table
    cursor.execute('''
        INSERT INTO cardekho_hyderabad_fts (ListingID, CarName, Price, Year, KilometersDriven, FuelType, Location, ListingURL, ImageURL)
        SELECT ListingID, CarName, Price, Year, KilometersDriven, FuelType, Location, ListingURL, ImageURL
        FROM cardekho_hyderabad;
    ''')
    cursor.execute('''
        CREATE VIRTUAL TABLE IF NOT EXISTS cardekho_bangalore_fts
        USING fts5(ListingID, CarName, Price, Year, KilometersDriven, FuelType, Location, ListingURL, ImageURL, tokenize = "unicode61 remove_diacritics 2");
    ''')

    # Copy data from the original table to the FTS virtual table
    cursor.execute('''
        INSERT INTO cardekho_bangalore_fts (ListingID, CarName, Price, Year, KilometersDriven, FuelType, Location, ListingURL, ImageURL)
        SELECT ListingID, CarName, Price, Year, KilometersDriven, FuelType, Location, ListingURL, ImageURL
        FROM cardekho_bangalore;
    ''')
    cursor.execute('''
        CREATE VIRTUAL TABLE IF NOT EXISTS cardekho_delhi_fts
        USING fts5(ListingID, CarName, Price, Year, KilometersDriven, FuelType, Location, ListingURL, ImageURL, tokenize = "unicode61 remove_diacritics 2");
    ''')

    # Copy data from the original table to the FTS virtual table
    cursor.execute('''
        INSERT INTO cardekho_delhi_fts (ListingID, CarName, Price, Year, KilometersDriven, FuelType, Location, ListingURL, ImageURL)
        SELECT ListingID, CarName, Price, Year, KilometersDriven, FuelType, Location, ListingURL, ImageURL
        FROM cardekho_delhi;
    ''')

    conn.commit()
    conn.close()

# Create the FTS table (run this only once)
create_fts_table()
