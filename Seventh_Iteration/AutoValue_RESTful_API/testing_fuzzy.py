import sqlite3

def fuzzy_search(query1):
    conn = sqlite3.connect('all_cars24_car_listings_copy.db')
    cursor = conn.cursor()

    # Use a parameterized query without additional quoting
    cursor.execute("""SELECT CarName FROM cars24_mumbai_fts WHERE CarName MATCH "cross";""")

    results = cursor.fetchall()
    conn.close()
    return results

# Example usage
query = "Maruti Suzuki S-Cross1"
results = fuzzy_search(query)
print("Fuzzy Search Results:", results)
