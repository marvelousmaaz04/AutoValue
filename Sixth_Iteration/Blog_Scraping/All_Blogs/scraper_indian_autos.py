from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import sqlite3
from datetime import datetime

driver = webdriver.Firefox()

# Navigate to AutoCar India website
driver.get("https://indianautosblog.com/car-news")
driver.maximize_window()

# Wait for the page to load (you might need to adjust the sleep time)
time.sleep(2)


def scroll_down(scroll_height=2000, scroll_pause_time=2):
    # Scroll down by the specified height\
    blog_elements = driver.find_element(By.CLASS_NAME, "list-car-home").find_elements(By.TAG_NAME, "li")
    while len(blog_elements) <= 200:
        
        # driver.execute_script(f"window.scrollTo(0,{scroll_height});")
        
        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        load_more_btn = driver.find_element(By.CSS_SELECTOR,"div.text-center.mg-bottom-98.mg-bottom-58").find_element(By.TAG_NAME, "button")
        driver.execute_script("arguments[0].scrollIntoView(true);", load_more_btn)
        load_more_btn.click()
        print("Button clicked")
        driver.execute_script("window.scrollBy(0, -700);")
        time.sleep(scroll_pause_time)
        # image_element = WebDriverWait(driver, 10).until(
        #     EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "a.img-sp img"))
        # )
        blog_elements = driver.find_element(By.CLASS_NAME, "list-car-home").find_elements(By.TAG_NAME, "li")
        print("Blogs Found:", len(blog_elements))
        # scroll_height = scroll_height + 1800

    driver.execute_script(f"window.scrollTo(0, 500);")
    time.sleep(2)

scroll_down()

def scrape_blogs():
    blog_details = []
    time.sleep(1)
    blog_elements = driver.find_element(By.CLASS_NAME, "list-car-home").find_elements(By.TAG_NAME, "li")  # The ul has all the li tags which are blogs

    for blog_element in blog_elements:
        print("Actual Blogs Found:",len(blog_details))
        
        image_element = blog_element.find_element(By.CSS_SELECTOR, "a.img-sp img")
        image_url = image_element.get_attribute("src")
        if "no-image.jpg" in image_url.split("/"):
            continue
        blog_url = blog_element.find_element(By.CSS_SELECTOR, "a.img-sp").get_attribute("href")
        
        title = blog_element.find_element(By.CSS_SELECTOR, "div.info-car").find_element(By.TAG_NAME,"a").text
        description = blog_element.find_element(By.CSS_SELECTOR, "div.short-info").text
        published_date = blog_element.find_element(By.CSS_SELECTOR, "span.date-creat").text
        published_date = published_date.strip('"').strip(" ")
        # print(published_date)
        # # Extract date from the published_date
        date_string = published_date

        # Parse the date string
        parsed_date = datetime.strptime(date_string, "%d/%m/%Y - %H:%M")

        # Format the date in the desired format
        published_date = parsed_date.strftime("%b %d, %Y")

        # print(published_date)
            
        blog_details.append({
            'image_url': image_url,
            'blog_url': blog_url,
            'title': title,
            'description': description,
            'published_date': published_date
        })
    print(len(blog_details))
    if len(blog_details) < 80:
        print("Actual blogs are less than 80, return.")
        return
    print("Inserting Data")
    connection = sqlite3.connect("all_blogs.db")
    cursor = connection.cursor()
    # Print the scraped data
    for blog in blog_details:
        # print("Image URL:", blog['image_url'])
        # print("Blog URL:", blog['blog_url'])
        # print("Title:", blog['title'])
        # print("Description:", blog['description'])
        # print("Published Date:", blog['published_date'])
        print("\n")

        cursor.execute('''
            INSERT INTO indian_autos_blogs (Title, Description, PublishedDate, ImageURL, BlogURL)
            VALUES (?, ?, ?, ?, ?)
        ''', (blog['title'], blog['description'], blog['published_date'], blog['blog_url'], blog['image_url']))
    print("Data Inserted Successfully")
    connection.commit()
    connection.close()

scrape_blogs()


# Close the browser
# driver.quit()
