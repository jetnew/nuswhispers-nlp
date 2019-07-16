from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup

driver = webdriver.Chrome()

url = "https://nuswhispers.com/tag/65313"
driver.get(url)


def is_content_present(driver):
    """
    The text 'No confessions to display.' is always present, but is visible only when post content is absent.
    Hence, if this element does not contain class name 'ng-hide', it means that post content is present.
    """
    element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'No confessions to display.')]"))
    )
    classes = element.get_attribute('class')
    return 'ng-hide' in classes

def wait_load_post(driver):
    """
    Waits at most 5 seconds for post content to load.
    """
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'post-text')]")))
        return True
    except:
        return False

# Get post content element if present
element = None
content_present = is_content_present(driver)
if content_present:
    # Wait for post to load
    if wait_load_post(driver):
        # Get post element
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@id, 'post-list')]")))

# Get post attributes if post is present
if element:
    html = element.get_attribute('innerHTML')
    soup = BeautifulSoup(html, 'html.parser')
    # print(soup.prettify())
    text = soup.find('span', class_='post-text')
    print(text.get_text())