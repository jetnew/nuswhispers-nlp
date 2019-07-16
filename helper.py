from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def is_content_present(driver):
    """
    The text 'No confessions to display.' is always present, but is visible only when post content is absent.
    Hence, if this element does not contain class name 'ng-hide', it means that post content is present.
    """
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'No confessions to display.')]"))
        )
        classes = element.get_attribute('class')
        return 'ng-hide' in classes
    except:
        return False

def wait_load_post(driver):
    """
    Waits at most 5 seconds for post content to load.
    """
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'post-text')]")))
        return True
    except:
        return False