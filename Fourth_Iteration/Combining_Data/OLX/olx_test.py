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
url = 'https://www.olx.in/mumbai_g4058997/cars_c84'
driver.get(url)


element = wait.until(
    EC.visibility_of_element_located((By.CLASS_NAME, '_3V_Ww')))
driver.maximize_window()


# Wait for the page to load (you may need to adjust the time depending on your internet speed)
time.sleep(3)

# Create a CSV file to store the data
csv_file = open('olx_mumbai.csv', 'w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['CarName', 'Price', 'Year',
                    'KilometersDriven', 'Fuel Type', 'Location'])

# Create an SQLite database and table to store the data
conn = sqlite3.connect('all_olx_car_listings.db')
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS olx_mumbai (ListingID INTEGER PRIMARY KEY AUTOINCREMENT, CarName TEXT, Price TEXT, Year TEXT, KilometersDriven TEXT, FuelType TEXT, Location TEXT, ListingURL TEXT, ImageURL TEXT)')


def scroll_to_element(element_to_scroll):
    # Use JavaScript to scroll to the element
    # driver.execute_script("arguments[0].scrollIntoView(true);", element)

    element_y_offset = element_to_scroll.location['y']

    # Calculate the scroll position to place the element slightly below the top of the viewport
    # Adjust the value (100 in this example)
    scroll_position = element_y_offset - 100

    # Scroll to the calculated position
    driver.execute_script(f"window.scrollTo(0, {scroll_position});")
    # element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, '_3V_Ww')))

# Replace this with your own locator and value

# Scroll down to load more listings


while True:
    previous_listing_count = len(driver.find_elements(By.CLASS_NAME, '_3V_Ww'))

    # Scroll down to load more listings
    element_to_scroll_to = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'button.rui-apowA')))
    # element_to_scroll_to = driver.find_element(
    #         By.CSS_SELECTOR, 'button.rui-apowA')
    
    load_btns = driver.find_elements(By.CSS_SELECTOR, 'button.rui-apowA')
    load_btn = load_btns[-1]  # Choose the last "Load more" button
    scroll_to_element(load_btn)

    if load_btn.is_displayed():
        load_btn.click()
        time.sleep(4)  # Wait for the listings to load
        current_listing_count = len(driver.find_elements(By.CLASS_NAME, '_1HlM1'))
    else:
        # No more listings to load, break out of the loop
        break


# Function to scrape and store the data
element = wait.until(EC.presence_of_all_elements_located(
    (By.CSS_SELECTOR, "img._3vnjf, img._2hBzJ")))
count = 0


def scrape_and_store_data():
    global count
    element = wait.until(
        EC.visibility_of_element_located((By.CLASS_NAME, '_1HlM1')))
    car_listings = driver.find_elements(By.CLASS_NAME, '_3V_Ww')

    for car in car_listings:

        try:

            car_info = car.find_element(
                By.CLASS_NAME, '_2Gr10').get_attribute("title")

            # Split the input string by commas
            parts = car_info.split(',')

            # Extract the car name, year, and fuel type
            car_name = parts[0].strip()
            car_name = re.match(r"(.+?)(?=\d|$)", car_name).group(0)

            # print("Car Name:", car_name)
            car_year = parts[1].strip()
            fuel_type = parts[2].strip()

            price = car.find_element(By.CLASS_NAME, '_1zgtX').text
            year_kilometers_driven = car.find_element(
                By.CLASS_NAME, '_21gnE').text

            parts = year_kilometers_driven.split('-')
            kilometers_driven = parts[1].strip()

            location_date = car.find_element(By.CLASS_NAME, "_3VRSm").text
            parts = location_date.split("\n")
            location = parts[0].strip()

            listing_url = car.find_element(
                By.TAG_NAME, "a").get_attribute("href")
            # image_url = car.find_element(By.TAG_NAME,"a").find_element(By.XPATH,"//div[@class='_1HlM1']").find_element(By.XPATH,"//figure[@class='_3UrC5']").find_element(By.TAG_NAME,"img")

            # time.sleep(0.7)
            image_url = car.find_element(By.CSS_SELECTOR, "div._1HlM1").find_element(
                By.XPATH, ".//img[contains(@class, '_3vnjf') or contains(@class, '_2hBzJ')]")

            # Print data to the console
            print(f'Car Year Name: {car_info}')
            print(f'Car Name: {car_name}')
            # print(f'Price: {price}')
            # print(f'Year: {car_year}')

            # print(f'Kilometers Driven: {kilometers_driven}')
            # print(f'Fuel Type: {fuel_type}')
            # print(f'Location: {location}')
            print(f'Listing URL: {listing_url}')
            print(f'Image URL: {image_url.get_attribute("src")}')
            print()
            count += 1

            # Write data to the CSV file
            # csv_writer.writerow([car_name, price, car_year, kilometers_driven, fuel_type, location])

            # # # Insert data into the SQLite database
            # cursor.execute('INSERT INTO spinny_mumbai (CarName, Price, Year, KilometersDriven, FuelType, Location, ListingURL, ImageURL) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
            #             (car_name, price, car_year, kilometers_driven, fuel_type, location,listing_url,image_url))
        except Exception as e:
            print(e)
        finally:
            conn.commit()
    conn.commit()
    print(len(car_listings))
    print(count)


# Loop through all pages and scrape data

scrape_and_store_data()

# Close the CSV file and database connection
csv_file.close()
conn.close()

# Close the web driver
# driver.quit()
