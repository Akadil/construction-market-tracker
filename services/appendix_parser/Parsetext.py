from difflib import SequenceMatcher     # for similarity of strings
import logging
import yaml
import re

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)


class Parsetext:
    """
        This class is responsible for parsing the text. It receives a string
        and returns a full characteristics of the tender

        Methods:
            parse(filename, text) -> dict:
                main function of the class. It receives a filename and a text and
                returns the characteristics of the tender
            
            check_content(text) -> bool:
                checks if the text contains the necessary information

            format_text(text) -> list:
                reformats the text by removing redundancy and returns a list of 
                blocks of text

        returner:
            - success:      bool    - True or False
            - status_code:  int     - 200 or 400
            - data:         dict    - characteristics of the tender
            - message:      string  - message regarding the parsing

        @version    
            - Finished
            - Test file: test/test_Parsetext.py
            - 27.02 version
    """

    config: dict = None     # config file
    errorMsg: str = None    # error message

    def __init__(self, config = None):
        # Read the config file using yaml
        logger.info("Initiating the class")

        try:
            if (config != None):
                self.config = config
            else:
                with open('services/appendix_parser/config.yml', 'r') as file:
                    data = yaml.safe_load(file)
                    self.config = data['PARSETEXT']

        except Exception as e:
            logger.error(f"Failed to init: {e}")


    def parse(self, filename, text):
        """
            Main function of the class

            :param text: string
            :return: list
        """
        logger.info(f"The parsing of the {filename} has started")

        # Check if the config file is loaded
        if (self.config == None):
            logger.warning("The config file is not loaded")
            return self.returner(false, None, f"blah blah blah")
        
        # Check if the content contains the necessary information
        if (self.check_content(text) == False):
            logger.warning(f"{self.errorMsg}")
            return self.returner(False, None, f"blah blah blah")

        # Format the text by removing redundancy
        text_list = self.format_text(text)

        # Set the characteristics
        characteristics = self.set_characteristics()

        # traverse through characteristics and find it in text
        for key in characteristics:
            info = self.config["CHARACTERISTICS"][key.upper()]

            # Check if the category is in the data
            for category in info["CATEGORIES"]:

                if self.is_in(text_list, category, self.config["THRESHOLD"]):

                    # Set the category. Warn if there are multiple categories
                    if (characteristics[key] == None):
                        logger.info(f"In {filename} {key} category found: {category}")
                        characteristics[key] = category
                    else:
                        logger.warning(f"In {filename}, Multiple {key} categories found: {category} and {characteristics[key]}")
        
        # Check if all characteristics are retrieved
        for key in characteristics:
            if characteristics[key] == None:
                logger.warning(f"In {filename} No {key} characteristic found")

                return self.returner(False, None, f"blah blah blah")

        return self.returner(True, characteristics, "Success!")
    

    def check_content(self, text):
        """
            This function checks if the content is in the proper format

            :used parse()
            :param text: string
            :return: bool
        """

        for i_test, test in self.config['TEST'].items():
            
            if (re.search(test["test"], text) == None):

                test_passed = f" {i_test}/{len(self.config['TEST'])} passed"

                self.errorMsg = f"{test['name']} - {test['error']} {test_passed}"
                return False

        return True

    
    def format_text(self, text):
        """
            This function formats the text. 
            
            :description    Before the parsing, the text was just a retrieved 
                            string with unnecessary characters. This function
                            removes redundancy and leaves only the necessary.
                            Retruns a list of blocks of text

            :param text: string
            :return: list
        """

        # Split text into bunches based on double newline characters
        bunches = text.strip().split('\n\n')

        # Process each bunch
        data = []
        for bunch in bunches:
            # Split each bunch into lines
            lines = bunch.strip().split('\n')

            # Remove empty lines and any leading/trailing whitespace from each line
            lines = [line.strip() for line in lines if line.strip()]

            # if there is a minus sign at the end of the line, make sure to have
            # a space before it
            for i in range(len(lines)):
                if lines[i][-1] in {'-', '–', '—', '−', '‐', '‒'}:
                    minus_sign = lines[i][-1]
                    if (lines[i][-2] != ' '):
                        lines[i] = lines[i][:-1] + ' ' + minus_sign

            # Join the lines to form a single block of text
            block = ' '.join(lines)
            
            # Append the block to the list of blocks
            data.append(block)

        # Log the blocks
        for i in range(len(data)):
            logger.debug(f"Block {i+1}: {data[i]}")
        return data


    def set_characteristics(self):
        """
            This function sets the characteristics of the tender

            :description    All available characteristics are in the config file.

            :return: dict
        """
        # Initialize the characteristics
        myCharacteristics = dict()

        for name, value in self.config["CHARACTERISTICS"].items():
            myCharacteristics[value["NAME"]] = None

        logger.debug(f"Characteristics: {myCharacteristics}")
        return myCharacteristics


    def is_in(self, text_list, category, threshold):
        """
        Check the existences of the category by using similarity check by Difflib

        Args:
            threshold (float):  The threshold of similarity

        Returns:
            bool: similarity check result
        """

        for text in text_list:
            if SequenceMatcher(None, text, category).ratio() > threshold:
                return True

        return False


    def returner(self, isSuccess, data, message):

        if (isSuccess == False):
            return {
                "success": False,
                "status_code": 400,
                "data": None,
                "message": message
            }
        else:
            return {
                "success": True,
                "status_code": 200,
                "data": data,
                "message": message
            }
