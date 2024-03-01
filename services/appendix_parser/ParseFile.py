from Parsetext import Parsetext
from RetrieveText import RetrieveText
from datetime import datetime as dt
import logging
import requests
import yaml
import os


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


responseForm = {
    "status_code": int,
    "message": str,
    "char": dict | None
}

class ParseFile:
    """
        This class is responsible for parsing the text from the pdf file and 
        returning the characteristics of the object.

        Methods:
            - __init__:      Initiates the class
            - parseFile:     The main function. Downloads a pdf file from the 
                            given url, extracts the text from it and returns 
                            the characteristics of the object

        Helpers:
            - self.get_file:    Downloads the file from the given url

            - RetrieveText:     The class designed to receive a file path and
                                return the specific text from the file. The 
                                class uses pdfminer to extract the text

            - Parsetext:        This class is responsible for parsing the text.
                                It receives a string and returns a full 
                                characteristics of the tender

        version:
            - 0.0.0 First version
            - Untested
    """

    config: dict = None     # config file
    retrievetext: type(RetrieveText)
    parsetext: type(Parsetext)

    def __init__(self):
        """
            Initiates the class
        """
        logger.info("Initiating the class")

        try :
            with open('./config.yml', 'r') as file:
                self.config = yaml.safe_load(file)

        except Exception as e:
            logger.error(f"Failed to init: {e}")
            return 

        self.retrievetext = RetrieveText(self.config)
        self.parsetext = Parsetext(self.config)


    def parseFile(self, name: str, url: str)-> responseForm: 
        """
            This function downloads a pdf file from the given url, extracts the
            text from it and returns the characteristics of the object.

            Args:
                - name:     The name of the file
                - url:      The url of the file to be downloaded

            Returns:
                - status_code:      The status code of the operation
                - message:          A message describing the status of the 
                                    operation
                - char:             The characteristics of the object
            
            components:
                - get_file:         Downloads the file from the given url
                - retrievetext:     Extracts the text from the file
                - parsetext:        Parses the text and returns the 
                                    characteristics of the object
        """

        logger.info("Starting parsing the file / link")

        # Get the file
        result = self.get_file(name, url)
        filename = result["data"]["file_path"]
        if (result["status_code"] != 200):
            return self.returner(result["status_code"], result["message"], None)

        # Extract the text from the pdf
        result = self.retrievetext.retrieve(result["data"]["file_path"])
        if (result == None):
            return self.returner(403, "Error: Couldn't extract the text", None)

        # Parse the text
        result = self.parsetext.parse(name, result)
        if (result["success"] == False):
            return self.returner(404, result["message"], None)

        # delete the file
        os.remove(filename)

        return self.returner(200, "Success", result["data"])


    def get_file(self, name: str, url: str):
        """
            This function downloads a pdf file from the given url and returns the 
            file path
        """

        # make a request to the url
        logger.info("Downloading the file")
        pdf_request = requests.get(url, verify=False)
        if (pdf_request.status_code != 200):
            return self.returner(401, pdf_request.reason, None)

        
        # Get the file
        
        try:
            pdf_file_path = self.create_file_path(name)
            
            # Create the file and write the content
            logger.info(f"Writing the file to {pdf_file_path}")
            os.makedirs(os.path.dirname(pdf_file_path), exist_ok=True)
            with open(pdf_file_path, 'wb') as file:
                file.write(pdf_request.content)
        
        except Exception as e:
            return self.returner(402, f"Error: {str(e)}", None)

        return self.returner(200, "Success", {"file_path": pdf_file_path})


    def create_file_path(self, name: str):
        if (name is None or name == ""):
            return "fileCache/" + str(dt.now().strftime("%Y%m%d_%H%M%S"))
        else:
            return "fileCache/" + name


    def returner(self, status_code: int, message: str, characteristics: dict | None):
        return {
                "status_code": status_code,
                "data": characteristics,
                "message": message
            }
