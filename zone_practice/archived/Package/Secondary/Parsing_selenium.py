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


def retrieve_technicality(driver):
    # Parsing appendix
    driver.find_elements_by_xpath('.//button[@class="btn btn-primary btn-sm"][contains(., "Перейти")]')[3].click()
    time.sleep(1)
    filename_tech_difficulty = driver.find_element_by_xpath('.//a[contains(., "appendix")]').text
    driver.find_element_by_xpath('.//a[contains(., "appendix")]').click()
    driver.find_element_by_xpath('.//button[contains(., "Закрыть")]').click()
    time.sleep(1)
    print("I downloaded ", filename_tech_difficulty)

    return filename_tech_difficulty


def retrieve_terms_time(driver):
    # Parsing techspec
    driver.find_elements_by_xpath('.//button[@class="btn btn-primary btn-sm"][contains(., "Перейти")]')[4].click()
    time.sleep(1)
    filename_time_given = driver.find_element_by_xpath('.//a[contains(., "techspec")]').text
    driver.find_element_by_xpath('.//a[contains(., "techspec")]').click()
    driver.find_element_by_xpath('.//button[contains(., "Закрыть")]').click()
    time.sleep(1)
    print("I downloaded ", filename_time_given)

    return filename_time_given


def retrieve_project_designer(driver):
    # Parsing project designer
    driver.find_elements_by_xpath('.//button[@class="btn btn-primary btn-sm"][contains(., "Перейти")]')[-1].click()
    time.sleep(1)
    filename_project_designer = driver.find_elements_by_xpath('.//a[contains(., ".pdf")]')[-1].text
    driver.find_elements_by_xpath('.//a[contains(., ".pdf")]')[-1].click()
    time.sleep(1)
    print("I downloaded ", filename_project_designer)

    return filename_project_designer


def parsing_technicality_file(filename):
    # Parsing technical difficulty
    inFile = open(filename, 'rb')
    resMgr = PDFResourceManager()
    retData = io.StringIO()
    TxtConverter = TextConverter(resMgr, retData, laparams=LAParams())
    interpreter = PDFPageInterpreter(resMgr, TxtConverter)

    generator_container = []
    for page in PDFPage.get_pages(inFile):
        generator_container.append(page)

    interpreter.process_page(generator_container[-2])
    interpreter.process_page(generator_container[-1])

    text = retData.getvalue()
    # print(text)

    if len(re.findall("первый[\s\S]{0,5}повышенный", text)) > 1:
        level = "Первый"
    elif len(re.findall("второй[\s\S]{0,5}нормальный", text)) > 1:
        level = "Второй"
    else:
        level = "(Не смог опознать)"

    if "не" not in re.findall("здания[\s\S]{0,3}и[\s\S]{0,3}сооружения,[\s\S]{0,6}относящиеся[\s\S]{0,3}"
                              "к[\s\S]{0,3}технически[\s\S]{0,3}сложным[\s\S]{0,3}объектам", text)[-1]:
        tech_diff = "сложный"
    else:
        tech_diff = "не сложный"

    # print("Тех сложность объекта", level, ", ", tech_diff)

    return tech_diff, level


def parsing_term_file(filename):
    # ---------------
    # Parsing time given
    inFile = open(filename, 'rb')

    resMgr = PDFResourceManager()
    retData = io.StringIO()
    TxtConverter = TextConverter(resMgr, retData, laparams=LAParams())
    interpreter = PDFPageInterpreter(resMgr, TxtConverter)

    generator_container = []
    # Work through all pages
    for page in PDFPage.get_pages(inFile):
        # interpreter.process_page(page)
        generator_container.append(page)

    interpreter.process_page(generator_container[-1])
    interpreter.process_page(generator_container[-2])

    text = retData.getvalue()
    # print(text)

    time_given = re.findall("(\d+|\d+\.\d+) месяц", text)[0]
    # print("Срок объекта ", time_given)

    return time_given


def parsing_project_designer_file(filename):
    # Parsing the project designer

    inFile = open(filename, 'rb')

    resMgr = PDFResourceManager()
    retData = io.StringIO()
    TxtConverter = TextConverter(resMgr, retData, laparams=LAParams())
    interpreter = PDFPageInterpreter(resMgr, TxtConverter)

    generator_container = []
    # Work through all pages
    for page in PDFPage.get_pages(inFile):
        # interpreter.process_page(page)
        generator_container.append(page)

    interpreter.process_page(generator_container[2])
    # interpreter.process_page(generator_container[3])

    text = retData.getvalue()
    # print(text)

    project_designer = re.findall("ГЕНПРОЕКТИРОВЩИК.{0,3}\n(.*)\n", text)[0]
    project_designer_date = re.findall("от (.+) г\.", text)[0]

    # print("Генпроектировщик ", project_designer, " ", project_designer_date)

    return project_designer, project_designer_date


def parsing_client_website(id):
    url = f'https://www.goszakup.gov.kz/ru/announce/index/{id}?tab=lots'
    page = urlopen(url)
    main_page_html = page.read()
    main_page_soup = BeautifulSoup(main_page_html, 'lxml')
    gov_costumer = main_page_soup.find_all('table')[-1].find_all('td')[2].text
    # print("Заказчик", gov_costumer)

    return gov_costumer


def parsing(id):
    options = webdriver.ChromeOptions()
    options.headless = True  # let's work on it background
    driver = webdriver.Chrome(
        executable_path="/Users/akadilkalimoldayev/.wdm/drivers/chromedriver/mac64/101.0.4951.41/chromedriver",
        options=options)
    driver.maximize_window()
    driver.get(f'https://goszakup.gov.kz/ru/announce/index/{id}?tab=protocols')
    time.sleep(2)
    driver.find_element_by_xpath('.//a[@class="btn btn-primary"]').click()
    time.sleep(2)

    driver.close()

    myfile = ""

    for file in os.listdir():
        if "pv" and "pdf" in file:
            myfile = file

    return myfile


# Connect to selenium in order to parse
def main(id):
    # Open chrome. "drive" is placeholder for virtual chrome
    options = webdriver.ChromeOptions()
    options.headless = True  # let's work on it background
    driver = webdriver.Chrome(
        executable_path="/Users/akadilkalimoldayev/.wdm/drivers/chromedriver/mac64/101.0.4951.41/chromedriver",
        options=options)
    driver.maximize_window()
    driver.get(f'https://goszakup.gov.kz/ru/announce/index/{id}?tab=documents')

    # Download needed pdf files
    filename_tech_difficulty = retrieve_technicality(driver)
    filename_time_given = retrieve_terms_time(driver)
    filename_project_designer = retrieve_project_designer(driver)

    # close the virtual chrome
    driver.close()

    # Parse pdf file to retrieve data
    tech_diff, level = parsing_technicality_file(filename_tech_difficulty)
    time_given = parsing_term_file(filename_time_given)
    project_designer, project_designer_date = parsing_project_designer_file(filename_project_designer)
    gov_costumer = parsing_client_website(id)

    # delete the parsed files afterward
    os.remove(filename_tech_difficulty) if os.path.exists(filename_tech_difficulty) \
        else print("The file does not exist!")
    os.remove(filename_time_given) if os.path.exists(filename_time_given) \
        else print("The file does not exist!")
    os.remove(filename_project_designer) if os.path.exists(filename_project_designer) \
        else print("The file does not exist!")

    return [gov_costumer, tech_diff, level, time_given, project_designer, project_designer_date]


# my_dbms.add_to_db_full(["7589002"] + main("7589002"))
parsing("7254774")


# class Parse_selenium:
#     def __init__(self):
#         # Open chrome. "drive" is placeholder for virtual chrome
#         options = webdriver.ChromeOptions()
#         options.headless = True  # let's work on it background
#
#         self.driver = webdriver.Chrome(
#                 executable_path="/Users/akadilkalimoldayev/.wdm/drivers/chromedriver/mac64/101.0.4951.41/chromedriver",
#                 options=options
#         )
#
#     def
