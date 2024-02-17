from _exceptions import CustomException
from _utils import *
import os

responseForm = {
    "status_code": int,
    "message": str,
    "char": dict | None
}

def parseFile(name: str, url: str)-> responseForm:
    """
        This function downloads a pdf file from the given url, extracts the 
        text from it and returns the characteristics of the object.

        Returns:
            dict:
                A dictionary containing the following keys:
                - 'status_code' (int): The HTTP status code of the response.
                - 'message' (str): A descriptive message regarding the response.
                - 'characteristics' (dict): The characteristics of the object.
    """

    # make a request to the url
    pdf_request = requests.get(url, verify=False)
    if (pdf_request.status_code != 200):
        return {
            "status_code": pdf_request.status_code, 
            "message": pdf_request.reason,
            "characteristics": None
        }
    
    # Create the file path
    pdf_file_path = utils.create_file_path(name)

    try:
        # Create the file and write the content
        os.makedirs(os.path.dirname(pdf_file_path), exist_ok=True)
        with open(pdf_file_path, 'wb') as file:
            file.write(pdf_request.content)
    
        try:
            # Extract the text from the pdf
            result_text = extract_text_from_pdf(pdf_file_path)

            response = {
                "status_code": 200, 
                "message": "Success",
                "characteristics": utils.parse_text(result_text)
            }

        except CustomException as ce:               # couldn't extract the text
            response = {                            # or config not there
                "status_code": 407,
                "message": f"Error: {str(ce)}",
                "characteristics": None
            }

    except Exception as e:                  # couldn't create the file
        response = {
            "status_code": 407,             
            "message": f"Error: {str(e)}",
            "characteristics": None
        }

    else:
        # clean up
        os.remove(pdf_file_path)

    return response
