from bs4 import BeautifulSoup
import logging
import requests
import re

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class ResultsParser:
    """
        Class to parse the data from results file. I will receive the link for 
        html page, then I will parse it and return the result.
    """    
    
    config: dict = None     # config file

    def __init__(self):
        logger.info("Initiating the class")

        try :
            with open('./config.yml', 'r') as file:
                data = yaml.safe_load(file)

            self.config = data["RESULTS_PARSER"]

        except Exception as e:
            logger.error(f"Failed to init class: {e}")
            return 


    def parse(self, link):
        """
            Main function. Parses the html file and returns the result

            Args:
                - link:     The link to the file

            Returns:
                - result:   The result of the parsing
        """

        logger.info(f"Starting parsing file in link: {link}")

        # Download the file and get the data
        data = self.get_data(link)
        if data["status_code"] != 200:
            return self.returner(data["status_code"], data["message"], None)
        
        data = data["data"]

        # Check the content
        tables = data.find_all('table')
        if len(tables) == 0:
            return self.returner(404, "Wrong content", None)

        # Parse the data
        result_table = table[-1];

        parcipants_info = []
        header_table: list = self.get_headers(result_table)

        for row in result_table.find_all('tr')[2:]:
            row_data = [td.get_text(strip=True) for td in row.find_all('td')]
            participant_info = {}

            for col_name, value in zip(header_table, row_data):
                participant_info[col_name] = value

            participants_info.append(participant_info)

        return self.returner(200, "Success", participants_info)


    def get_headers(self, table):
        """
            Gets the headers of the table

            Args:
                - table:    The table to get the headers from

            Returns:
                - headers:  The headers of the table
        """

        logger.info(f"Getting the headers of the table")

        headers = []
        columns = self.config["COMPONENTS"]

        for th in table.find('tr').find_all('th'):
            text = th.get_text(strip=True)

            for column in columns:
                if re.search(column["regex"], text, flags=re.IGNORECASE):
                    headers.append(text)

        return headers


    def get_data(self, link):
        """
            Gets the data from the html file

            Args:
                - link:     The link to the file

            Returns:
                - data:     The data from the file
        """

        # Download the file
        fileContent = self.download_file(link)
        if fileContent is None:
            return self.returner(402, "Error: Couldn't download the file", None)

        # Parse the file (Get the soup)
        try:
            soup = BeautifulSoup(fileContent, 'html.parser')

        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            logger.debug(f"The file Content is \n{fileContent}")

            return self.returner(403, "Error: Couldn't soupify the content", None)

        return self.returner(200, "Success", soup)


    def download_file(self, link):
        """
            Downloads the file from the link

            Args:
                - link:     The link to the file

            Returns:
                - fileContent:   The content of the file
        """
        logger.info(f"Downloading file")

        try: 
            response = requests.get(link, verify=False)

            if response.status_code == 200:
                logger.info(f"File downloaded successfully")
            else:
                logger.error(f"Failed to download the file. {response.status_code}")
                return None

        except requests.exceptions.RequestException as re:
            logger.error(f"Failed to download the file: {re}")
            return None

        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            return None

        return response.content


    def returner(self, status_code, message, char):
        """
            Returns the result

            Args:
                - status_code:      The status code of the operation
                - message:          A message describing the status of the 
                                    operation
                - char:             The characteristics of the object

            Returns:
                - responseForm:     The result of the operation
        """

        return {
            "status_code": status_code,
            "message": message,
            "data": char
        }