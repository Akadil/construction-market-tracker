from services.appendix_parser import parseFile
from . import utils


class TenderCharacteristics:
    """
        Get and check the characteristics of the tender
    """
    tender: dict
    isValidFull: bool = (False, False, False, False)
    isValid: bool = False

    def __init__(self, tender):
        self.tender = tender

        # Prepare the tender for the update
        set_characteristics_to_null(self.tender)
        
        for lot in self.tender["lots"]:
            characteristics = self.get_characteristics(lot)
            if (characteristics == None):
                continue

            lot["level"] = characteristics["level"]
            if (lot["level"] < 3):
                self.isValid[0] = True
            lot["tech_diff"] = characteristics["tech_diff"]
            if (lot["tech_diff"] < 4):
                self.isValid[1] = True
            lot["type"] = characteristics["type"]
            lot["goal"] = characteristics["goal"]





    def set_characteristics_to_null(self):
        """
            Set the characteristics of the tender to None
        """
        self.tender["level"] = None
        self.tender["tech_diff"] = None
        self.tender["type"] = None
        self.tender["goal"] = None
        for lot in self.tender["lots"]:
            lot["level"] = None
            lot["tech_diff"] = None
            lot["type"] = None
            lot["goal"] = None

    
    def get_characteristics(self, lot):
        """
            Get the characteristics of the lot
        """
        fileName, filePath = utils.get_file_link(lot["files"], "appendix_5")
        if (fileName == None):      # if the file is not there
            return None

        response = parseFile(filePath, fileName)
        if (response["status_code"] != 200):    # if the file could not be parsed
            return None
        
        return response["char"]













def update_characteristics(tender):
    """
        Check the technical characteristics of the tender and update the tender
        accordingly. 

        Args:
            tender: The tender to check

        Returns:
            bool: True if the tender is valid, False otherwise
    """
    tender = set_none(tender)

    for lot in tender["lots"]:
        fileName, filePath = get_file_link(lot["files"], "appendix_5")
        if (fileName == None):      # if the file is not there
            continue

        response = parseFile(filePath, fileName)
        if (response["status_code"] != 200):
            continue

        if (response["char"]["level"][0] == 3):
            continue
        if (response["char"]["type"][0] == 4):
            continue
        if (response["char"]["goal"][0] != 1):
            continue

        lot["level"] = response["char"]["level"][1]
        lot["tech_diff"] = response["char"]["tech_diff"][1]
        lot["type"] = response["char"]["type"][1]
        lot["goal"] = response["char"]["goal"][1]

    tender["level"] = tender["lots"][0]["level"]
    tender["tech_diff"] = tender["lots"][0]["tech_diff"]
    tender["type"] = tender["lots"][0]["type"]
    tender["goal"] = tender["lots"][0]["goal"]


def set_none(tender):
    """
        Set the characteristics of the tender to None
    """
    tender["level"] = None
    tender["tech_diff"] = None
    tender["type"] = None
    tender["goal"] = None
    for lot in tender["lots"]:
        lot["level"] = None
        lot["tech_diff"] = None
        lot["type"] = None
        lot["goal"] = None
    return tender