import csv
import sqlite3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re



# Initialize the web driver (provide the path to your ChromeDriver executable)
driver = webdriver.Firefox()
wait = WebDriverWait(driver, 5)
# Open the website
url = 'https://www.cars24.com/buy-used-car?sort=bestmatch&serveWarrantyCount=true&listingSource=ViewAllCars&storeCityId=2&pinId=110001'
driver.get(url)


element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, '_2kfVy')))
driver.maximize_window()


# Wait for the page to load (you may need to adjust the time depending on your internet speed)
time.sleep(3)

# Create a CSV file to store the data
csv_file = open('cars24_newdelhi.csv', 'w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['CarName', 'Price', 'Year', 'KilometersDriven', 'Fuel Type', 'Location'])

# Create an SQLite database and table to store the data
conn = sqlite3.connect('all_cars24_car_listings.db')
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS cars24_newdelhi (ListingID INTEGER PRIMARY KEY AUTOINCREMENT, CarName TEXT, Price TEXT, Year TEXT, KilometersDriven TEXT, FuelType TEXT, Location TEXT, ListingURL TEXT, ImageURL TEXT)')

# Define a function to scroll down the page
middle_of_page = driver.execute_script("return window.innerHeight + window.scrollY")

# Define a function to scroll to the middle of the page
def scroll_to_bottom(amount):
    script = f"window.scrollTo(0, {amount})"
    driver.execute_script(script)
    time.sleep(3)  # Adjust the time based on your website's loading speed

# Scroll down to load more listings
i = 500
while True:
    
    previous_listing_count = len(driver.find_elements(By.CLASS_NAME, '_2kfVy'))
    scroll_to_bottom(i)
    # time.sleep(2)  # Adjust the time based on your website's loading speed
    element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, '_2kfVy')))
    current_listing_count = len(driver.find_elements(By.CLASS_NAME, '_2kfVy'))
    print(current_listing_count)
    if current_listing_count >= 650:
        time.sleep(5)
        print("Total listings found:",current_listing_count)
        break
        
    i = i + 1500
    


# Function to scrape and store the data

def scrape_and_store_data():
    car_listings = driver.find_elements(By.CLASS_NAME, '_2kfVy')
    
    for car in car_listings:

        try:

            car_year_name = car.find_element(By.CLASS_NAME, '_2lmIw').text
            

            text = car_year_name
            pattern = r'(\d{4}) (.+)'
            match = re.match(pattern, text)

            if match:
                car_year = match.group(1)
                car_name = match.group(2)
                
            else:
                print("Pattern not found in the text.")

            
            price = car.find_element(By.CLASS_NAME, '_18ToE').find_element(By.TAG_NAME,"span").text
            price = price.replace("₹","").strip()
            # year = car.find_element(By.CLASS_NAME, 'car-year').text

            other_info = car.find_element(By.CLASS_NAME, "_13yb6")
            info = other_info.find_elements(By.TAG_NAME,"li")

            kilometers_driven = info[0].text
            fuel_type = info[2].text
            location = car.find_element(By.CLASS_NAME,"_351jJ").text

            listing_url = car.get_attribute("href")
            image_url = car.find_element(By.CSS_SELECTOR,"img._4x0mJ").get_attribute("src")
            
            

            # Print data to the console
            # print(f'Car Year Name: {car_year_name}')
            # print(f'Car Name: {car_name}')
            # print(f'Price: {price}')
            # print(f'Year: {car_year}')
            
            # print(f'Kilometers Driven: {kilometers_driven}')
            # print(f'Fuel Type: {fuel_type}')
            # print(f'Location: {location}')
            # print(f'Listing URL: {listing_url}')
            # print(f'Image URL: {image_url}')
            print()
            
            

            # Write data to the CSV file
            csv_writer.writerow([car_name, price, car_year, kilometers_driven, fuel_type, location])

            # Insert data into the SQLite database
            cursor.execute('INSERT INTO cars24_newdelhi (CarName, Price, Year, KilometersDriven, FuelType, Location, ListingURL, ImageURL) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',(car_name, price, car_year, kilometers_driven, fuel_type, location,listing_url,image_url))
        except Exception as e:
            print(e)
        
    conn.commit()
    print(len(car_listings))
    

# Loop through all pages and scrape data
scrape_and_store_data()
    

# Close the CSV file and database connection
csv_file.close()
conn.close()

# Close the web driver
# driver.quit()
