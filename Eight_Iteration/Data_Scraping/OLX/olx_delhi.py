import csv
import sqlite3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re



driver = webdriver.Firefox()
wait = WebDriverWait(driver, 5)
# Open the website
url = 'https://www.olx.in/delhi_g4058659/cars_c84'
driver.get(url)


element = wait.until(
    EC.visibility_of_element_located((By.CLASS_NAME, '_3V_Ww')))
driver.maximize_window()



time.sleep(3)

# Create a CSV file to store the data
csv_file = open('olx_delhi.csv', 'w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['CarName', 'Price', 'Year',
                    'KilometersDriven', 'Fuel Type', 'Location'])

# Create an SQLite database and table to store the data
conn = sqlite3.connect('all_olx_car_listings.db')
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS olx_delhi (ListingID INTEGER PRIMARY KEY AUTOINCREMENT, CarName TEXT, Price TEXT, Year TEXT, KilometersDriven TEXT, FuelType TEXT, Location TEXT, ListingURL TEXT, ImageURL TEXT)')


def scroll_to_element(element_to_scroll):
    # Use JavaScript to scroll to the element
    # driver.execute_script("arguments[0].scrollIntoView(true);", element)

    element_y_offset = element_to_scroll.location['y']

    # Calculate the scroll position to place the element slightly below the top of the viewport
  
    scroll_position = element_y_offset - 100

    # Scroll to the calculated position
    driver.execute_script(f"window.scrollTo(0, {scroll_position});")
    # element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, '_3V_Ww')))


# Scroll down to load more listings


while True:
    previous_listing_count = len(driver.find_elements(By.CLASS_NAME, '_3V_Ww'))
    # element_to_scroll_to = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, '_3V_Ww')))
    # element_to_scroll_to = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/main/div/div/section/div/div[2]/div[5]/div[2]/div[1]/div[2]/ul/li[41]/div/button')))
    element = wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, 'button.rui-apowA')))
    element_to_scroll_to = driver.find_elements(
        By.CSS_SELECTOR, 'button.rui-apowA')
    # print(len(element_to_scroll_to))
    load_btn = element_to_scroll_to[-1]
    scroll_to_element(load_btn)
    # print(load_btn.text)
    load_btn.click()
    element = wait.until(
        EC.visibility_of_element_located((By.CLASS_NAME, '_1HlM1')))
    time.sleep(2)

    # Scroll to the element
 
    current_listing_count = len(driver.find_elements(By.CLASS_NAME, '_1HlM1'))
    print(current_listing_count)

    if current_listing_count == previous_listing_count or current_listing_count >= 600:
        time.sleep(2)
        element_to_scroll_to = driver.find_elements(
            By.CSS_SELECTOR, 'button.rui-apowA')
        # print(len(element_to_scroll_to))
        load_btn = element_to_scroll_to[-1]
        element_y_offset = load_btn.location['y']

        # Calculate the scroll position to place the element slightly below the top of the viewport
       
        scroll_position = element_y_offset - 500

        # Scroll to the calculated position
        driver.execute_script(f"window.scrollTo(0, {scroll_position});")
        element = wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, '_1HlM1')))
        time.sleep(5)
        break


# Function to scrape and store the data
# element = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "img._3vnjf, img._2hBzJ")))
count = 0


def scrape_and_store_data():
    global count
    element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, '_1HlM1')))
    car_listings = driver.find_elements(By.CLASS_NAME, '_3V_Ww')

    for car in car_listings:

        try:

            car_info = car.find_element(
                By.CLASS_NAME, '_2Gr10').get_attribute("title")

            # Split the input string by commas
            parts = car_info.split(',')

            # Extract the car name, year, and fuel type
            # car_name = parts[0].strip()
            # car_name = re.match(r"(.+?)(?=\d|$)", car_name).group(0)
            car_name = car.find_element(
                By.CLASS_NAME, '_2Gr10').text

            # print("Car Name:", car_name)
            car_year = parts[1].strip()
            fuel_type = parts[2].strip()

            price = car.find_element(By.CLASS_NAME, '_1zgtX').text
            # price = "₹ 11,85,000"
            price = price.replace('₹', '').strip()
            # print(price)
            year_kilometers_driven = car.find_element(
                By.CLASS_NAME, '_21gnE').text

            parts = year_kilometers_driven.split('-')
            kilometers_driven = parts[1].strip()

            # location_date = car.find_element(By.CLASS_NAME, "_3VRSm").text
            # parts = location_date.split("\n")
            # location = parts[0].strip()

            listing_url = car.find_element(
                By.TAG_NAME, "a").get_attribute("href")
            # image_url = car.find_element(By.TAG_NAME,"a").find_element(By.XPATH,"//div[@class='_1HlM1']").find_element(By.XPATH,"//figure[@class='_3UrC5']").find_element(By.TAG_NAME,"img")
            driver.execute_script("window.open('', '_blank');")
            driver.switch_to.window(driver.window_handles[1])
            driver.get(listing_url)
            # element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div._23Jeb")))
            time.sleep(2)
            # Perform scraping operations in the new tab
          
          
            # page_title = driver.title
            # print("Page Title:", page_title)
            image_url = driver.find_element(By.CSS_SELECTOR, "div._23Jeb").find_element(By.XPATH, ".//img[contains(@class, '_15xdg') or contains(@class, '_1Iq92')]").get_attribute("src")
            location = driver.find_elements(By.CSS_SELECTOR,'div._3VRXh')
            location = location[1].text
            # Close the new tab
            
            # time.sleep(0.7)
            # image_url = car.find_element(By.CSS_SELECTOR, "div._1HlM1").find_element(
            #     By.XPATH, ".//img[contains(@class, '_3vnjf') or contains(@class, '_2hBzJ')]") this is working only for some on the same page

            # Print data to the console
            print(f'Car Year Name: {car_info}')
            print(f'Car Name: {car_name}')
            print(f'Price: {price}')
            print(f'Year: {car_year}')

            print(f'Kilometers Driven: {kilometers_driven}')
            print(f'Fuel Type: {fuel_type}')
            print(f'Location: {location}')
            print(f'Listing URL: {listing_url}')
            print(f'Image URL: {image_url}')
            print()
            driver.close() # before using an element be sure to switch to that context
            count += 1
            driver.switch_to.window(driver.window_handles[0])

            # Write data to the CSV file
            csv_writer.writerow([car_name, price, car_year, kilometers_driven, fuel_type, location])

            # # Insert data into the SQLite database
            cursor.execute('INSERT INTO olx_delhi (CarName, Price, Year, KilometersDriven, FuelType, Location, ListingURL, ImageURL) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                        (car_name, price, car_year, kilometers_driven, fuel_type, location,listing_url,image_url))
            print(count)
        except Exception as e:
            print(e)
            driver.switch_to.window(driver.window_handles[0])
    
            # driver.switch_to.window(driver.window_handles[0])
        
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
