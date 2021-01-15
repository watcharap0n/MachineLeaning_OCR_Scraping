import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd
import json
import requests
from PIL import Image
from io import BytesIO
from vision_machine_optical import VisionOCR


class WebScraping:

    def __init__(self, webdriver):
        self.webdriver = webdriver

    def dynamic_scraping(self, uri, html, key, val, delay):
        driver = webdriver.Edge(self.webdriver)
        driver.get(uri)
        driver.implicitly_wait(5)
        time.sleep(delay)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        content = soup.find_all(html, {key: val})
        driver.close()
        return content

    def table_index(self, tax_id, url):
        driver = webdriver.Edge(self.webdriver)
        driver.get(url)
        driver.implicitly_wait(5)
        time.sleep(1)
        element = driver.find_element_by_xpath('//*[@id="loginForm"]/div[1]/span')
        location = element.location
        size = element.size
        png = driver.get_screenshot_as_png()
        im = Image.open(BytesIO(png))
        left = location['x']
        top = location['y']
        right = location['x'] + size['width']
        bottom = location['y'] + size['height']
        im = im.crop((left, top, right, bottom))
        im.save('config/screenshot.png')
        ocr = VisionOCR('config/screenshot.png')
        ocr = ocr.document_spilt_text()
        hack = driver.find_element_by_id('captchaCode')
        hack.send_keys(ocr)
        summit = driver.find_element_by_id('signinBtn')
        summit.click()
        time.sleep(2)
        input_tax = driver.find_element_by_xpath('//*[@id="textStr"]')
        input_tax.send_keys(str(tax_id))
        time.sleep(2)
        enter_tax = driver.find_element_by_xpath('//*[@id="Capa_1"]')
        enter_tax.submit()
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        content = soup.find_all('table', {'id': 'fixTable'})
        return content








