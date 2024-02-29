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

# Navigate to AutoX India website
driver.get("https://www.autox.com/news/car-news/")
driver.maximize_window()

# Wait for the page to load (you might need to adjust the sleep time)
time.sleep(2)


def scrape_blogs():
    blog_details = []
    time.sleep(1)
    page = 1
    while True:

        blog_elements = driver.find_elements(By.CLASS_NAME, "post-item")  # The ul has all the li tags which are blogs
        print("At Page:",page)
        for blog_element in blog_elements:
            print("Actual Blogs Found:",len(blog_details))
            
            
            blog_url = blog_element.find_element(By.CSS_SELECTOR, "span.had-thumb").get_attribute("data-link")
            
            title = blog_element.find_element(By.CSS_SELECTOR, "span.had-thumb").get_attribute("title")

            image_element = blog_element.find_element(By.CSS_SELECTOR, "span.had-thumb").find_element(By.TAG_NAME,"img")
            image_url = image_element.get_attribute("src")
            # if "no-image.jpg" in image_url.split("/"):
            #     continue

            description = blog_element.find_element(By.CSS_SELECTOR, "div.post-right").find_element(By.TAG_NAME,"p").text
            published_date = blog_element.find_element(By.CSS_SELECTOR, "div.post-excerpt").find_element(By.XPATH,".//span[@title][last()]").get_attribute("title")
            published_date = published_date.strip('"').strip(" ")
            # print(published_date)
            # # Extract date from the published_date
            date_string = published_date

            # Parse the date string
            parsed_date = datetime.strptime(date_string, "%B %d, %Y %I:%M %p")

            # Format the date in the desired format
            published_date = parsed_date.strftime("%b %d, %Y")

            # print(published_date)

            # print("Image URL:", image_url)
            # print("Blog URL:", blog_url)
            # print("Title:", title)
            # print("Description:", description)
            # print("Published Date:", published_date)
            # print("\n")
                
            blog_details.append({
                'image_url': image_url,
                'blog_url': blog_url,
                'title': title,
                'description': description,
                'published_date': published_date
            })
        if len(blog_details) >= 100:
            break
        next_page = driver.find_element(By.CLASS_NAME,"st-pagination").find_elements(By.TAG_NAME,"li")[-2]
        next_page.click()
        page = page + 1
        print("Going to next page:",page)
        time.sleep(2)
        
    print(len(blog_details))
    print("Inserting Data")
    connection = sqlite3.connect("all_blogs.db")
    cursor = connection.cursor()
    # Print the scraped data
    for blog in blog_details:
        cursor.execute('''
            INSERT INTO autox_blogs (Title, Description, PublishedDate, ImageURL, BlogURL)
            VALUES (?, ?, ?, ?, ?)
        ''', (blog['title'], blog['description'], blog['published_date'], blog['blog_url'], blog['image_url']))
    print("Data Inserted Successfully")
    connection.commit()
    connection.close()

scrape_blogs()


# Close the browser
# driver.quit()
