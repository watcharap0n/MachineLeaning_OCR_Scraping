import requests
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd
import json
import requests
from PIL import Image
from io import BytesIO
from vision_machine_optical import VisionOCR


def check_xpaht_dbd(driver):
    driver.implicitly_wait(5)
    driver.find_element_by_xpath('//*[@id="loginForm"]/div[1]/span/img').screenshot('config/screenshot.png')
    # element_image = driver.find_element_by_xpath('//*[@id="loginForm"]/div[1]/span')
    # location = element_image.location
    # size = element_image.size
    # png = driver.get_screenshot_as_png()
    # im = Image.open(BytesIO(png))
    # left = location['x']
    # top = location['y']
    # right = left + size['width']
    # bottom = top + size['height']
    # print(left, top)
    # print(right, bottom)
    # im = im.crop((int(left), int(top), int(right), int(bottom)))
    # im.save('config/screenshot.png')
    time.sleep(2)
    ocr = VisionOCR('config/screenshot.png')
    ocr = ocr.document_pandas()
    ocr = ocr.to_dict()
    texts = ocr['description']
    hack = driver.find_element_by_id('captchaCode')
    hack.send_keys(texts[1])
    summit = driver.find_element_by_id('signinBtn')
    summit.click()
    time.sleep(1)


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

    def dbd_tax(self, tax_id, url):
        driver = webdriver.Chrome('config/chromedriver')
        try:
            driver.get(url)
            check_xpaht_dbd(driver)
            input_tax = driver.find_element_by_xpath('//*[@id="textStr"]')
            input_tax.send_keys(str(tax_id))
            time.sleep(1)
            enter_tax = driver.find_element_by_xpath('//*[@id="Capa_1"]')
            enter_tax.submit()
            time.sleep(1)
            soup = BeautifulSoup(driver.page_source, 'lxml')
            content = soup.find_all('table', {'id': 'fixTable'})
            driver.close()
            return content
        except NoSuchElementException:
            while True:
                try:
                    driver.get(url)
                    check_xpaht_dbd(driver)
                    input_tax = driver.find_element_by_xpath('//*[@id="textStr"]')
                    input_tax.send_keys(str(tax_id))
                    time.sleep(1)
                    enter_tax = driver.find_element_by_xpath('//*[@id="Capa_1"]')
                    enter_tax.submit()
                    time.sleep(1)
                    soup = BeautifulSoup(driver.page_source, 'lxml')
                    content = soup.find_all('table', {'id': 'fixTable'})
                    driver.close()
                    return content
                except NoSuchElementException:
                    time.sleep(1)
                    driver.get(url)
                    check_xpaht_dbd(driver)
