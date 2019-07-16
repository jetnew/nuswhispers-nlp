from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd
from bs4 import BeautifulSoup
from helper import *
import os


class Post:
    """
    # Create sample post
    post = Post(64236)
    post.get_text(driver)
    print(post.text)
    """
    def __init__(self, tag):
        self.url = "https://nuswhispers.com/tag/" + str(tag)
        self.tag = tag
        self.text = None
        self.post_element = None

    def get_tag(self):
        return self.tag

    def get_post_element(self, driver=None):
        if self.post_element:
            return self.post_element
        else:
            driver.get(self.url)
            element = None
            content_present = is_content_present(driver)
            if content_present:
                if wait_load_post(driver):
                    try:
                        element = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, "//div[contains(@id, 'post-list')]"))
                        )
                    except:
                        element = None
            self.post_element = element
            return self.post_element

    def get_text(self, driver=None):
        """Get post text, given driver."""
        if self.text:
            return self.text
        else:
            post_element = self.get_post_element(driver=driver)
            if post_element:
                html = post_element.get_attribute('innerHTML')
                soup = BeautifulSoup(html, 'html.parser')
                text = soup.find('span', class_='post-text')
                self.text = text.get_text()
                return self.text

    def has_text(self):
        return "Present" if self.text else "Absent"

class Collection:
    """
    # Create collection
    collection = Collection()
    for tag in range(64236, 64300):
        post = Post(tag)
        post.get_text(driver)
        collection.insert(post)
    """
    def __init__(self):
        self.posts = []
        self.df = pd.DataFrame({})

    def insert(self, post):
        """Insert Post into post list"""
        assert type(post) == Post
        if post.text:
            self.posts.append(post)

    def is_empty(self):
        """True if post list is empty"""
        return len(self.posts) == 0

    def is_updated(self):
        """True if size of DataFrame equals post list"""
        return len(self.df) == len(self.posts)

    def to_df(self):
        """Update DataFrame if not updated with post list"""
        assert not self.is_empty()

        if self.is_updated():
            return self.df
        else:
            df = pd.DataFrame({})
            tags = [post.get_tag() for post in self.posts]
            texts = [post.get_text() for post in self.posts]
            df['tag'] = tags
            df['text'] = texts
            self.df = df
            return self.df

    def to_csv(self, path):
        """Create .csv file"""
        assert not self.is_empty()
        if 'data/' not in path:
            path = 'data/' + path

        if not self.is_updated():
            self.to_df()
        self.df.to_csv(path, index=False)
        print("Saved to:", path)

    def to_excel(self, path):
        """Create .xlsx file"""
        assert not self.is_empty()
        if 'data/' not in path:
            path = 'data/' + path

        if not self.is_updated():
            self.to_df()
        self.df.to_excel(path, index=False, engine='xlsxwriter')
        print("Saved to:", path)
