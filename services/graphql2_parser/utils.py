from services.appendix_parser import *


def update_characteristics(tender):
    """
        Check the technical characteristics of the tender and update the tender
        accordingly. 

        Args:
            tender: The tender to check

        Returns:
            bool: True if the tender is valid, False otherwise
    """
    

    for lot in tender["lots"]:
        fileName, filePath = get_file_link(lot["files"], "appendix_5")
        if (fileName == None):      # if the file is not there
            return False
        response = parseFile(filePath, fileName)

        if (response["status_code"] != 200):    # if the file could not be parsed
            return False
        if (response["char"]["level"][0] == 3):     # remove level 3 tenders
            return False
        if (response["char"]["type"][0] == 4):    # remove "unknown" tenders
            return False
        if (response["char"]["goal"][0] != 1):




# fileName, filePath = get_file_link(tender["lots"], "appendix_5")
# if (fileName == None):      # if the file is not there
#     return None
# response = parseFile(filePath, fileName)

# if (response["status_code"] != 200):    # if the file could not be parsed
#     return None
# if (response["char"]["level"][0] == 3):     # remove level 3 tenders
#     return None
# if (response["char"]["type"][0] == 4):    # remove "unknown" tenders
#     return None
# if (response["char"]["goal"][0] != 1):  # remove tenders 
#     return None

# return response["char"]

def add_characteristic(tender, characteristics) -> dict:
    """
        Add the characteristics of the tender

        Args:
            tender: The tender to add the characteristics to

        Returns:
            dict: The tender with the characteristics
    """

    for key, value in characteristics.items():
        tender[key] = value

    return tender


def get_file_link(files: list, nameFile: str) -> str:
    """
        This function takes a list of files and a name of the file
        and returns the link to the appropriate file.

        Returns:
            str: The link to the file

        Possible inputs:
            files: list: A list of files
            nameFile: str: The name of the file. E.g. "buy_pi", "appendix_5"
    """

    for file in files:
        if nameFile in file["originalName"]:
            return file["originalName"], file["filePath"]
    return None, None