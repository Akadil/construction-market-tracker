from datetime import datetime as dt
from _exceptions import CustomException
import urllib3
import yaml

urllib3.disable_warnings()

def create_file_path(name):
    if (name is None or name == ""):
        return "fileCache/" + str(dt.now().strftime("%Y%m%d_%H%M%S"))
    else:
        return "fileCache/" + name


def extract_text_from_pdf(pdf_path):

    try :
        from pdfminer.high_level import extract_text
        
        text = extract_text(pdf_path)
        if text is None:
            raise CustomException("Error: The text could not be extracted")
    
    except Exception as e:
        raise CustomException(f"Error: {str(e)}")

    return text


def get_technicality(text: str):
    characteristics = {}

    # Load the configuration file
    try:
        with open('config.yml', 'r') as file:
            config = yaml.safe_load(file)
            regex = config["REGEX"]
            
    except Exception as e:
        raise CustomException(f"Error: {str(e)}")       # handle this case

    # Get the level of responsibility
    if len(re.findall(regex["LEVELS"]["ONE"], text) > 1):
        characteristics["level"] = (1, "Первый")

    elif len(re.findall(regex["LEVELS"]["TWO"], text)) > 1:
        characteristics["level"] = (2, "Второй")
    else:
        characteristics["level"] = (3, "другое")

    # Get the technical difficulty
    if "не" not in re.findall(regex["TECHS"], text)[-1]:
        characteristics["tech_diff"] = (1, "сложный")
    else:
        characteristics["tech_diff"] = (2, "не сложный")

    # Get the type of the construction
    if len(re.findall(regex["TYPES"]["NEW"], text)) > 1:
        characteristics["type"] = (1, "новое строительство")
    
    elif len(re.findall(regex["TYPES"]["REPAIR"], text)) > 1:
        characteristics["type"] = (3, "капитальный ремонт")

    elif len(re.findall(regex["TYPES"]["RECON"], text)) > 1:
        characteristics["type"] = (2, "реконструкция")
    else:
        characteristics["type"] = (4, "другое")

    # Get the goal of the construction
    if len(re.findall(regex["GOALS"]["OTHER"], text)) > 1:
        characteristics["goal"] = (2, "прочие сооружения")

    elif len(re.findall(regex["GOALS"]["LIVING"], text)) > 1:
        characteristics["goal"] = (1, "объекты жилищно-гражданского назначения")
    else:
        characteristics["goal"] = (3, "другое")

    return characteristics    
