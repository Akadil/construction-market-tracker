from pdfminer.high_level import extract_text
import re
import os
import requests
import urllib3

urllib3.disable_warnings()


def extract_text_from_pdf(pdf_path):
    try:
        text = extract_text(pdf_path)
        return text
    except Exception as e:
        return None


def get_technicality(text: str):
    characteristics = {}

    if len(re.findall("первый[\s\S]{0,5}повышенный", text)) > 1:
        characteristics["level"] = (1, "Первый")
    elif len(re.findall("второй[\s\S]{0,5}нормальный", text)) > 1:
        characteristics["level"] = (2, "Второй")
    else:
        characteristics["level"] = (3, "другое")

    if "не" not in re.findall("здания[\s\S]{0,3}и[\s\S]{0,3}сооружения,[\s\S]{0,6}относящиеся[\s\S]{0,3}"
                              "к[\s\S]{0,3}технически[\s\S]{0,3}сложным[\s\S]{0,3}объектам", text)[-1]:
        characteristics["tech_diff"] = (1, "сложный")
    else:
        characteristics["tech_diff"] = (2, "не сложный")

    if len(re.findall("новое[\s\S]{0,5}строительство", text)) > 1:
        characteristics["type"] = (1, "новое строительство")
    elif len(re.findall("реставрация[\s\S]{0,5}и[\s\S]{0,5}капитальный[\s\S]{0,5}ремонт[\s\S]{0,5}существующих[\s\S]{0,5}объектов", text)) > 1:
        characteristics["type"] = (3, "капитальный ремонт")
    elif len(re.findall("реконструкция", text)) > 1:
        characteristics["type"] = (2, "реконструкция")
    else:
        characteristics["type"] = (4, "другое")

    if len(re.findall("прочие[\s\S]{0,5}сооружения", text)) > 1:
        characteristics["goal"] = (2, "прочие сооружения")
    elif len(re.findall("объекты[\s\S]{0,5}жилищно", text)) > 1:
        characteristics["goal"] = (1, "объекты жилищно-гражданского назначения")
    else:
        characteristics["goal"] = (3, "другое")

    return characteristics    


def parseFile(name, url):
    # Iterate through different pdf files


    pdf_file_path = f'fileCache/{name}'
    os.makedirs(os.path.dirname(pdf_file_path), exist_ok=True)
    response = requests.get(url, verify=False)

    # Check the request and save the file
    if response.status_code == 200:            
        with open(pdf_file_path, 'wb') as file:
            file.write(response.content)
    
    else:
        return  {"status_code": response.status_code, 
                    "message": "Failed to download the file.",
                    "characteristics": None}

    # extract text from the pdf file and get the characteristics
    result_text = extract_text_from_pdf(pdf_file_path)
    if (result_text is None):
        return {"status_code": 407, 
                "message": "No text found in the pdf file",
                "characteristics": None}
        
    response = {"status_code": 200, 
                "message": "Success",
                "characteristics": get_technicality(result_text)}
    
    # clean up
    file.close()
    os.remove(pdf_file_path)

    return response


if __name__ == "__main__":
    url = "https://ows.goszakup.gov.kz/download/trd_buy_lots_list/fc827be523eea833df73bf9c271d59b0"
    name = "appendix_5_2022_11541287.pdf"
    parseFile(name, url)
