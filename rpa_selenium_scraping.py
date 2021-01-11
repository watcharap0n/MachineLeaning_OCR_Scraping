import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time


class WebScraping:

    def __init__(self, webdriver):
        self.webdriver = webdriver

    def dynamic_scraping(self, uri, html, key, val, delay):
        driver = webdriver.Chrome(self.webdriver)
        driver.get(uri)
        driver.implicitly_wait(5)
        time.sleep(delay)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        content = soup.find_all(html, {key: val})
        driver.close()
        return content
