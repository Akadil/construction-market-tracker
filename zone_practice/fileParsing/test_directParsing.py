from pdfminer.high_level import extract_text
import re
import requests
import urllib3
import fitz

urllib3.disable_warnings()

def retrieve_speciality(file_link):
    """====================================================================="""
    """
        Test: Test the usage of pdfminer to parse pdf files
    """
    """====================================================================="""

    # Download the file
    text = retrieve_pdf_content_from_url(file_link)

    print(text)


def retrieve_pdf_content_from_url(pdf_url):
    final_text = ""
    pdf_document = None

    try:
        response = requests.get(pdf_url, stream=True, verify=False)
        response.raise_for_status()

        pdf_document = fitz.open(stream=response.content, filetype="pdf")
        
        # Iterate through pages and retrieve text
        for page_number in range(pdf_document.page_count):
            page = pdf_document[page_number]
            text = page.get_text()
            final_text += text
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if pdf_document:
            pdf_document.close()

    print(final_text)



def retrieve_pdf_content_from_url2(pdf_url):
    response = requests.get(pdf_url, verify=False)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
    
        # Create a file name based on the current timestamp and file extension
        file_name = f'downloaded_file.html'
        
        # Open the file in binary write mode ('wb')
        with open(file_name, 'wb') as file:
            # Write the content to the file
            file.write(response.content)
        
        print(f"File downloaded and saved as '{file_name}'")
    else:
        print(f"Failed to download the file. Status code: {response.status_code}")

        print("Putain! Something went wrong.")

    print(extract_text_from_pdf(file_name))


def extract_text_from_pdf(pdf_path):
    try:
        # Extract text from the PDF file
        text = extract_text(pdf_path)
        return text
    except Exception as e:
        print(f"Error: {e}")
        return None


def get_technicality(text: str):
    returner = {}

    if len(re.findall("первый[\s\S]{0,5}повышенный", text)) > 1:
        returner["level"] = "Первый"
    elif len(re.findall("второй[\s\S]{0,5}нормальный", text)) > 1:
        returner["level"] = "Второй"
    else:
        returner["level"] = "другое"

    if "не" not in re.findall("здания[\s\S]{0,3}и[\s\S]{0,3}сооружения,[\s\S]{0,6}относящиеся[\s\S]{0,3}"
                              "к[\s\S]{0,3}технически[\s\S]{0,3}сложным[\s\S]{0,3}объектам", text)[-1]:
        returner["tech_diff"] = "сложный"
    else:
        returner["tech_diff"] = "не сложный"

    if len(re.findall("новое[\s\S]{0,5}строительство", text)) > 1:
        returner["type"] = "новое строительство"
    elif len(re.findall("реставрация[\s\S]{0,5}и[\s\S]{0,5}капитальный[\s\S]{0,5}ремонт[\s\S]{0,5}существующих[\s\S]{0,5}объектов", text)) > 1:
        returner["type"] = "капитальный ремонт"
    elif len(re.findall("реконструкция", text)) > 1:
        returner["type"] = "реконструкция"
    else:
        returner["type"] = "другое"

    if len(re.findall("прочие[\s\S]{0,5}сооружения", text)) > 1:
        returner["goal"] = "прочие сооружения"
    elif len(re.findall("объекты[\s\S]{0,5}жилищно", text)) > 1:
        returner["goal"] = "объекты жилищно-гражданского назначения"
    else:
        returner["goal"] = "другое"

    return returner    

if __name__ == "__main__":
    file_link = "https://ows.goszakup.gov.kz/download/trd_buy_lots_list/fc827be523eea833df73bf9c271d59b0"
    retrieve_speciality(file_link)












