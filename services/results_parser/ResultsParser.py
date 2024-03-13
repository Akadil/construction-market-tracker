from bs4 import BeautifulSoup
import logging
import requests
import re
import yaml
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

try:
    from market_tracker.settings import API_TOKEN
except Exception as e:
    from .tests.test_resultParser import API_TOKEN

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
            logger.info(f"File content downloaded successfully!")

        except Exception as e:
            logger.error(f"Error in parsing the content: {e}")

            return self.returner(False, "Couldn't parse the file", None)


        """ Retrieve all information about participants """
        logger.info(f"Starting to parse the content of the file")

        # try:
            # Check the content of the tables
        tables = soup.find_all('table')
        tables = tables[int(len(tables) / 2) :]  # Remove the kaz version of the tables
        lots = self.sort_tables(tables)

        for lot in lots:

            logger.info(f"Starting to parse {lot['lot_number']} lot")

            lot["participants"] = self.get_participants(lot["table_participants"])
            dict_participants = self.formulate_participants(lot["participants"])

            headers = self.get_headers(lot["table_score_calculation"], lot["table_results"])

            # parse the participants info from score calculation table
            for row in lot["table_score_calculation"].find_all('tr')[4:]:
                row_data = row.find_all('td')
                
                participant = dict_participants[row_data[headers["b_id"]].get_text(strip=True)]
                participant["experience_level"] = row_data[headers["experience_level"]].get_text(strip=True)
                participant["tax_score"] = row_data[headers["tax_score"]].get_text(strip=True)
                participant["location_score"] = row_data[headers["location_score"]].get_text(strip=True)
                participant["negative_score"] = row_data[headers["negative_score"]].get_text(strip=True)
                participant["score"] = row_data[headers["score"]].get_text(strip=True)

            # parse the participants info from results table
            for row in lot["table_results"].find_all('tr')[2:]:
                row_data = row.find_all('td')

                participant = dict_participants[row_data[headers["b_id"]].get_text(strip=True)]
                participant["bid"] = row_data[headers["bid"]].get_text(strip=True)
                participant["score_bid"] = row_data[headers["score_bid"]].get_text(strip=True)
                participant["financial_stability"] = row_data[headers["fin_stability"]].get_text(strip=True)
                participant["applied_time"] = row_data[headers["applied_time"]].get_text(strip=True)

            lot.pop("table_participants")
            lot.pop("table_score_calculation")
            lot.pop("table_results")

        # except Exception as e:
        #     logger.error(f"Error in parsing the content: {e}")
        #     return self.returner(False, "Error in parsing the content", None)

        return self.returner(True, "Success", lots)


    def download_file(self, link):
        """
            Downloads the file from the link

            Args:
                - link:     The link to the file

            Returns:
                - fileContent:   The content of the file
        """
        logger.info(f"Downloading file")

        # headers = {'Authorization': f'Bearer {API_TOKEN}'}
        # response = requests.get(link, headers=headers, verify=True)
        response = requests.get(link, verify=False)

        if response.status_code == 200:
            logger.info(f"File downloaded successfully")
        else:
            raise Exception(f"Get request failed. Status code {response.status_code}")

        return response.content


    def sort_tables(self, tables):
        """
            Gets the tables from the soup

            1. Identify how many lots are there
            2. Sort the tables by the lots
        """

        logger.info(f"Starting to sort the tables")
        
        lot_table = self.get_table(tables, self.config["TABLENAME_LOTS"])
        tables.remove(lot_table)


        """ Identify how many lots are there """
        lots = []    # list of lot numbers (lot ids)
        lotNumber = self.config["COLNAME_LOTNUMBER"]  # col. name of the lot number
        myCol = self.get_column(lot_table.find('tr'), lotNumber)   # column of the lot number

        for lot in lot_table.find_all('tr')[1:]:
            lots.append(lot.find_all('td')[myCol].get_text(strip=True))

        # I assume that each lot has 3 tables: participants, score calculation and results
        if (len(lots) * 3 != len(tables)):
            logger.error(f"The amount of tables is not correct")
            raise Exception("The amount of tables is not correct")


        """ Sort the tables by the lots """
        sorted_tables = [] # list of dictionaries
        
        for i, lot in enumerate(lots):
            # Take the tables of the current lot. First 3 tables
            u_tables = tables[int(3 * i) : int(3 * (i + 1))]  # updated tables

            tn_participant = self.config["TABLENAME_PARTICIPANTS"]  # table name of participants
            tn_scores = self.config["TABLENAME_SCORE_CALCULATION"]  # table name of score calculation
            tn_results = self.config["TABLENAME_RESULTS"]  # table name of results

            lot_info = {
                "lot_number": lot,
                "table_participants": self.get_table(u_tables, tn_participant),
                "table_score_calculation": self.get_table(u_tables, tn_scores),
                "table_results": self.get_table(u_tables, tn_results)
            }

            sorted_tables.append(lot_info)

        return sorted_tables


    def get_column(self, tableRow, name, dataType = "td"):
        """
            Get the column of the table
        """

        i = 0
        # logger.debug(f"Getting the column of the table\n {tableRow}")
        for td in tableRow.find_all(dataType):
            if name in td.get_text(strip=True):
                return i
            i += 1
        
        raise Exception(f"Couldn't find the column: {name}")


    def get_table(self, tables, name):
        """
            Retrieve the table from tables with specific name
        """

        for table in tables:
            if name in table.caption.text:
                return table

        raise Exception(f"Couldn't find the table with name: {name}")


    def get_participants(self, myTable):
        """
            Gets the participants from the tables
        """

        logger.info(f"Getting the participants of the tender")

        # Identify the headers (columns) of the table
        name_name = self.config["COMPONENTS"]["name"]    # name of the participant
        name_b_id = self.config["COMPONENTS"]["b_id"]    # b_id of the participant
        col_name = self.get_column(myTable.find('tr'), name_name, "th")   # column of the name
        col_b_id = self.get_column(myTable.find('tr'), name_b_id, "th")   # column of the b_id

        # Get the participants
        participants = []

        for row in myTable.find_all('tr')[1:]:
            participants.append({
                    "name": row.find_all('td')[col_name].get_text(strip=True),
                    "b_id": row.find_all('td')[col_b_id].get_text(strip=True)
                }
            )

        return participants


    def formulate_participants(self, participants):
        """
            Formulate the participants in a dictionary
        """

        dict_participants = {}

        for participant in participants:
            dict_participants[participant["b_id"]] = participant

        return dict_participants


    def get_headers(self, table_experience, table_results):
        """
            Gets the headers of the table
        """

        name = self.config["COMPONENTS"]["name"]
        b_id = self.config["COMPONENTS"]["b_id"]
        experience_level = self.config["COMPONENTS"]["experience_level"]
        tax_score = self.config["COMPONENTS"]["tax_score"]
        location_score = self.config["COMPONENTS"]["location_score"]
        negative_score = self.config["COMPONENTS"]["negative_score"]
        score = self.config["COMPONENTS"]["score"]
        bid = self.config["COMPONENTS"]["bid"]
        score_bid = self.config["COMPONENTS"]["score_bid"]
        fin_stability = self.config["COMPONENTS"]["fin_stability"]
        applied_time = self.config["COMPONENTS"]["applied_time"]

        headers = {
            "name": self.get_column(table_experience.find('tr'), name, "th"),
            "b_id": self.get_column(table_experience.find('tr'), b_id, "th"),
            "experience_level": self.get_column(table_experience.find_all('tr')[1], experience_level, "th"),
            "tax_score": self.get_column(table_experience.find_all('tr')[1], tax_score, "th"),
            "location_score": self.get_column(table_experience.find_all('tr')[1], location_score, "th"),
            "negative_score": self.get_column(table_experience.find_all('tr')[1], negative_score, "th"),
            "score": self.get_column(table_experience.find_all('tr')[1], score, "th"),
            "bid": self.get_column(table_results.find('tr'), bid, "th"),
            "score_bid": self.get_column(table_results.find('tr'), score_bid, "th"),
            "fin_stability": self.get_column(table_results.find('tr'), fin_stability, "th"),
            "applied_time": self.get_column(table_results.find('tr'), applied_time, "th")
        }

        return headers


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