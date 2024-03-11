from bs4 import BeautifulSoup
import logging
import requests
import re
import yaml

try:
    from market_tracker.settings import API_TOKEN
except Exception as e:
    from tests.test_resultParser import API_TOKEN

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

        """ Get the content """
        try:
            fileContent = self.download_file(link)
            soup = BeautifulSoup(fileContent, 'html.parser')

        except Exception as e:
            logger.error(f"Error in parsing the content: {e}")

            return self.returner(False, "Couldn't parse the file", None)


        """ Retrieve all information about participants """
        try:
            # Check the content of the tables
            tables = soup.find_all('table')
            participants = self.get_participants(tables)
            sorted_tables = self.sort_tables(tables)


            headers = self.get_headers(table[-2], table[-1])
            if headers.isSuccess == False:
                return self.returner(False, "Wrong format of the table", None)

            participants_info = []
            dict_participants = {}
            table_experience =  table[-2]
            table_result = table[-1];

            for row in table_experience.find_all('tr')[4:]:
                row_data = [td.get_text(strip=True) for td in row.find_all('td')]
                participant = {
                    "name": row_data[1],
                    "b_id": row_data[2],
                    "experience_level": row_data[3],
                    "tax_indicator": row_data[4],
                    "score_location": row_data[9],
                    "negative_score": row_data[10],
                    "score": row_data[11],
                }

                dict_participants[participant["b_id"]] = participant
                participants_info.append(participant)


            for row in table_results.find_all('tr')[2:]:
                row_data = [td.get_text(strip=True) for td in row.find_all('td')]
                
                participant_info = dict_participants[row_data[2]]

                participant_info["bid"] = row_data[4]
                participant_info["financial_stability"] = row_data[8]
                participant_info["applied_time"] = row_data[9]

        except Exception as e:
            logger.error(f"Error in parsing the participants info: {e}")
            return self.returner(False, "Error in parsing the participants info", None)

        return self.returner(True, "Success", participants_info)


    def sort_tables(self, tables):
        """
            Gets the tables from the soup
        """

        logger.info(f"Starting to sort the tables")

        sorted_tables = []

        # Identify the amount of lots in the tender
        number_of_lots = -1

        for table in tables:
            if self.config["TABLENAME_LOTS"] in table.caption.text:
                number_of_lots = len(table.find_all('tr')) - 1
                break
        
        if number_of_lots == -1:
            raise Exception("Couldn't find the number of lots in the tender")

        


        return sorted_tables


    def get_participants(self, tables):
        """
            Gets the participants from the tables
        """

        logger.info(f"Getting the participants of the tender")

        # Get the table with the participants
        myTable = None

        for table in tables:
            if self.config["TABLENAME_PARTICIPANTS"] in table.caption.text:
                myTable = table
                break

        if myTable == None:
            raise Exception(f"Couldn't find the table with the participants")

        # Identify the headers of the table
        col_name = -1
        col_b_id = -1

        for i, th in enumerate(myTable.find('tr').find_all('th')):
            if re.search(self.config["COMPONENTS"]["name"]["regex"], th.get_text(strip=True), flags=re.IGNORECASE):
                col_name = i
            elif re.search(self.config["COMPONENTS"]["b_id"]["regex"], th.get_text(strip=True), flags=re.IGNORECASE):
                col_b_id = i
            
        if col_name == -1 and col_b_id == -1:
            raise Exception(f"Couldn't find the headers of the table")
        

                
        
                for row in table.find_all('tr')[1:]:
                    row_data = [td.get_text(strip=True) for td in row.find_all('td')]

                    participant = {
                        "name": row_data[0],
                        "b_id": row_data[1],
                        "status": row_data[2],
                        "score": row_data[3]
                    }

                    participants.append(participant)

        return participants


    def get_headers(self, table_experience, table_results):
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


    def download_file(self, link):
        """
            Downloads the file from the link

            Args:
                - link:     The link to the file

            Returns:
                - fileContent:   The content of the file
        """
        logger.info(f"Downloading file")

        headers = {'Authorization': f'Bearer {API_TOKEN}'}
        response = requests.get(link, headers=headers, verify=True)

        if response.status_code == 200:
            logger.info(f"File downloaded successfully")
        else:
            raise Exception(f"Get request failed. Status code {response.status_code}")

        return response.content


    def returner(self, status_code, message, data):
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
            "is_success": status_code,
            "message": message,
            "data": data
        }