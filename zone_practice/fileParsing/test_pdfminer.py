from pdfminer.high_level import extract_text
import re

def main():
    """====================================================================="""
    """
        Test: Test the usage of pdfminer to parse pdf files
    """
    """====================================================================="""
    # Iterate through different pdf files
    for i in range(1, 10):
        print('==============================')
        print(f"{i} th pdf file")
        print("==============================")

        pdf_file_path = f'examples/appendix_{i}.pdf'
        result = extract_text_from_pdf(pdf_file_path)
        if (result is None):
            print("No text found in the pdf file")
        else:
            characteristics = get_technicality(result)
            print(characteristics)
        print()
        

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
    main()
