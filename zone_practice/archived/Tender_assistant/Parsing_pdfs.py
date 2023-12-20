from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams

import io
import re
import os
import time


def parsing_technicality_file(filename):
    # Parsing technical difficulty
    inFile = ""
    while inFile == "":
        try:
            inFile = open(filename, 'rb')
        except FileNotFoundError:
            print("ooooooops")
            time.sleep(0.1)


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

    os.remove(filename) if os.path.exists(filename) else print("The file does not exist!")


    # print("Тех сложность объекта", level, ", ", tech_diff)

    return tech_diff, level


def parsing_term_file(filename):
    # ---------------
    # Parsing time given
    inFile = ""
    while inFile == "":
        try:
            inFile = open(filename, 'rb')
        except FileNotFoundError:
            pass

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


    os.remove(filename) if os.path.exists(filename) else print("The file does not exist!")


    # print("Срок объекта ", time_given)

    return time_given


def parsing_project_designer_file(filename):
    # Parsing the project designer

    inFile = ""
    while inFile == "":
        try:
            inFile = open(filename, 'rb')
        except FileNotFoundError:
            pass


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


    os.remove(filename) if os.path.exists(filename) else print("The file does not exist!")

    # print("Генпроектировщик ", project_designer, " ", project_designer_date)

    return project_designer, project_designer_date


# Delete unneeded files
def pvConverter(filename_input):
    # "buy_pv_0310_1648_6700383.pdf"

    # ----------- Part1 --------------
    # Parsing through pdf

    # Convert pdf to text(string)
    myDir = filename_input
    inFile = open(myDir, 'rb')
    resMgr = PDFResourceManager()
    retData = io.StringIO()
    TxtConverter = TextConverter(resMgr, retData, laparams=LAParams())
    interpreter = PDFPageInterpreter(resMgr, TxtConverter)

    # Work through all pages
    for page in PDFPage.get_pages(inFile):
        interpreter.process_page(page)

    # my main string where saved all data
    text = retData.getvalue()
    # print(text)

    # ----------- Part2 --------------
    # Extracting needed data

    # Extract general information like number of competitors, lot number, name of the tender, customer
    num_competitors = \
    re.findall("на участие в конкурсе представлены следующими потенциальными поставщиками: (\d+)", text)[0]
    lot = re.findall("Протокол вскрытия №(\d{7}-..\d)", text)
    name = re.findall("Название конкурса ((.+\n)*)Наименование организатора", text)[0][0].replace("\n", "")
    customer = re.findall("Заказчик ((.+\n)*)", text)[0][0].replace("\n", "")
    sum = re.findall("Перечень закупаемых товаров, работ, услуг на общую сумму: (\d+ тг)", text)

    # Extract info about competitor names and their bin
    myPattern = "(ТОО|Товарищество с ограниченной ответственностью)[ \n]*(\"[\wА-Яа-я-\n\.\" әіңғүұқөӘІҢҒҮҰҚӨ]*\") +(\d{12})"
    all_competitors_uncleaned = re.findall(myPattern, text)
    all_competitors_uncleaned = list(dict.fromkeys(all_competitors_uncleaned))

    # Cleaning and fixing the competitor data
    all_competitors = []
    pv_i = 0
    for item in all_competitors_uncleaned:
        pv_i += 1
        all_competitors.append((item[1], item[2]))

    # Checking is number of competitors satisfying extracted ones
    pass_score = 0
    if pv_i == int(num_competitors):
        pass_score = 1

    return all_competitors, pass_score
