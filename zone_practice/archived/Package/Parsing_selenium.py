from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams

import io
import re
import os
import ssl
import time

from selenium import webdriver
from urllib.request import urlopen
from bs4 import BeautifulSoup

ssl._create_default_https_context = ssl._create_unverified_context


options = webdriver.ChromeOptions()
options.headless = True  # let's work on it background
driver = webdriver.Chrome(
    executable_path="/Users/akadilkalimoldayev/.wdm/drivers/chromedriver/mac64/101.0.4951.41/chromedriver",
    options=options)
driver.maximize_window()


def retrieve_technicality_file(id):
    # Parsing appendix

    driver.get(f'https://goszakup.gov.kz/ru/announce/index/{id}?tab=documents')
    driver.find_elements_by_xpath('.//button[@class="btn btn-primary btn-sm"][contains(., "Перейти")]')[3].click()
    time.sleep(1)

    filename_tech_difficulty = driver.find_element_by_xpath('.//a[contains(., "appendix")]').text
    driver.find_element_by_xpath('.//a[contains(., "appendix")]').click()
    driver.find_element_by_xpath('.//button[contains(., "Закрыть")]').click()
    time.sleep(1)

    # print("I downloaded ", filename_tech_difficulty)

    return filename_tech_difficulty


def retrieve_terms_file(id):
    # Parsing techspec

    driver.get(f'https://goszakup.gov.kz/ru/announce/index/{id}?tab=documents')
    driver.find_elements_by_xpath('.//button[@class="btn btn-primary btn-sm"][contains(., "Перейти")]')[4].click()
    time.sleep(1)

    filename_time_given = driver.find_element_by_xpath('.//a[contains(., "techspec")]').text
    driver.find_element_by_xpath('.//a[contains(., "techspec")]').click()
    driver.find_element_by_xpath('.//button[contains(., "Закрыть")]').click()
    time.sleep(1)

    # print("I downloaded ", filename_time_given)

    return filename_time_given


def retrieve_designer_file(id):
    # Parsing project designer

    driver.get(f'https://goszakup.gov.kz/ru/announce/index/{id}?tab=documents')
    driver.find_elements_by_xpath('.//button[@class="btn btn-primary btn-sm"][contains(., "Перейти")]')[-1].click()
    time.sleep(1)

    filename_project_designer = driver.find_elements_by_xpath('.//a[contains(., ".pdf")]')[-1].text
    driver.find_elements_by_xpath('.//a[contains(., ".pdf")]')[-1].click()
    time.sleep(1)

    # print("I downloaded ", filename_project_designer)

    return filename_project_designer


def retrieve_pv_file(id):

    driver.get(f'https://goszakup.gov.kz/ru/announce/index/{id}?tab=protocols')
    time.sleep(1)
    driver.find_element_by_xpath('.//a[@class="btn btn-primary"]').click()
    time.sleep(1)

    driver.close()

    myfile = ""

    for file in os.listdir():
        if "pv" and "pdf" in file:
            myfile = file

    for ind in range(len(myfile) - 1, -1, -1):
        if myfile[ind] == "/":
            break

    return myfile[ind:]



def parsing_client_name(id):
    # url = f'https://www.goszakup.gov.kz/ru/announce/index/{id}?tab=lots'
    # page = urlopen(url)
    # main_page_html = page.read()
    # main_page_soup = BeautifulSoup(main_page_html, 'lxml')
    # gov_costumer = main_page_soup.find_all('table')[-1].find_all('td')[2].text

    driver.get(f'https://www.goszakup.gov.kz/ru/announce/index/{id}?tab=lots')
    gov_costumer = driver.find_elements_by_tag_name("table")[-1].find_elements_by_tag_name("td")[2].text

    # print(gov_costumer)
    return gov_costumer


# my_dbms.add_to_db_full(["7589002"] + main("7589002"))
# parsing_client_website("7585675")
