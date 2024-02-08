import csv
import sqlite3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

# Assuming you have initialized the driver (e.g., ChromeDriver)
firefox_profile = webdriver.FirefoxProfile()
firefox_profile.set_preference("dom.popup_maximum", 0)
driver = webdriver.Firefox()
url = 'https://www.olx.in/mumbai_g4058997/cars_c84'

# driver.get(url)
driver.execute_script("window.open('','_blank');")

# Switch to the new tab
driver.switch_to.window(driver.window_handles[1])
driver.get(url)
wait = WebDriverWait(driver, 5)

element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, '_3V_Ww')))
driver.maximize_window()

def scroll_to_element(element_to_scroll):
    # Use JavaScript to scroll to the element
    # driver.execute_script("arguments[0].scrollIntoView(true);", element)

    element_y_offset = element_to_scroll.location['y']

    # Calculate the scroll position to place the element slightly below the top of the viewport
    scroll_position = element_y_offset - 100  # Adjust the value (100 in this example)

    # Scroll to the calculated position
    driver.execute_script(f"window.scrollTo(0, {scroll_position});")
    element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, '_3V_Ww')))

# Replace this with your own locator and value
# element_to_scroll_to = driver.find_element(By.CSS_SELECTOR, '._38O09 > button:nth-child(1)')

# element_to_scroll_to = driver.find_element(By.PARTIAL_LINK_TEXT, 'load more')
  # Replace with the actual button text


# Scroll to the element
# scroll_to_element(load_btn)

while True:
    element_to_scroll_to = driver.find_elements(By.CSS_SELECTOR, 'button.rui-apowA')
    print(len(element_to_scroll_to))
    load_btn = element_to_scroll_to[-1]
    scroll_to_element(load_btn)
    print(load_btn.text)
    load_btn.click()
    element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, '_1HlM1')))
    time.sleep(2)
