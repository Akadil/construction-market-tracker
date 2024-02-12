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
