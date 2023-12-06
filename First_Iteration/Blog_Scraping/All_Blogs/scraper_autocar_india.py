from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
import re
import sqlite3

driver = webdriver.Firefox()

# Navigate to AutoCar India website
driver.get("https://www.autocarindia.com/car-news")
driver.maximize_window()

# Wait for the page to load (you might need to adjust the sleep time)
time.sleep(2)


def scroll_down(scroll_height=1000, scroll_pause_time=2):
    # Scroll down by the specified height\
    blog_elements = driver.find_elements(By.CLASS_NAME, "new-section")
    while len(blog_elements) <= 100:
        blog_elements = driver.find_elements(By.CLASS_NAME, "new-section")
        driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight + {scroll_height});")
        print("Blogs Found:", len(blog_elements))
        time.sleep(scroll_pause_time)
    driver.execute_script(f"window.scrollTo(0, 2000);")

scroll_down()

def scrape_blogs():
    blog_details = []
    time.sleep(1)
    blog_elements = driver.find_elements(By.CLASS_NAME, "new-section")  # Adjust the class name accordingly

    for blog_element in blog_elements:
        image_url = blog_element.find_element(By.TAG_NAME, "img").get_attribute("src")
        blog_url = blog_element.find_element(By.TAG_NAME, "a").get_attribute("href")
        title = blog_element.find_element(By.CSS_SELECTOR, "div.new-sec-det").find_element(By.TAG_NAME,"a").text
        description = blog_element.find_element(By.CSS_SELECTOR, "div.new-sec-det").find_element(By.CSS_SELECTOR,"p.new-pare-p").text
        published_date = blog_element.find_element(By.CSS_SELECTOR, "div.new-sec-det").find_element(By.CSS_SELECTOR,"p.pub-date-p").text

        # Extract date from the published_date
        input_string = published_date
        # Define the regex pattern to match the date part
        date_pattern = re.compile(r'(\w{3} \d{1,2}, \d{4})')
        # Use findall to extract the date part
        matches = date_pattern.findall(input_string)
        if matches:
            # print(matches[0])
            published_date = matches[0]
    
        blog_details.append({
            'image_url': image_url,
            'blog_url': blog_url,
            'title': title,
            'description': description,
            'published_date': published_date
        })
    print(len(blog_details))
    print("Inserting Data")
    connection = sqlite3.connect("autocar_india.db")
    cursor = connection.cursor()
    # Print the scraped data
    for blog in blog_details:
        # print("Image URL:", blog['image_url'])
        # print("Blog URL:", blog['blog_url'])
        # print("Title:", blog['title'])
        # print("Description:", blog['description'])
        # print("Published Date:", blog['published_date'])
        # print("\n")

        cursor.execute('''
            INSERT INTO all_car_blogs (Title, Description, PublishedDate, ImageURL, BlogURL)
            VALUES (?, ?, ?, ?, ?)
        ''', (blog['title'], blog['description'], blog['published_date'], blog['blog_url'], blog['image_url']))
    print("Data Inserted Successfully")
    connection.commit()
    connection.close()

scrape_blogs()


# Close the browser
# driver.quit()
