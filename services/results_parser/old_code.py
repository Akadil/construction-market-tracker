import requests
from bs4 import BeautifulSoup
import re

class ParseHTML:
    
    fileContent = None
    patterns = {
        "bin": re.compile(r'\bБИН\b', flags=re.IGNORECASE),
        "inn": re.compile(r'\bИНН\b', flags=re.IGNORECASE),
        "name": re.compile(r'\bНаименование\b', flags=re.IGNORECASE),
        "pun": re.compile(r'\bналогов\b', flags=re.IGNORECASE),
        "experience": re.compile(r'\bОпыт\b', flags=re.IGNORECASE),
        "address": re.compile(r'\bНахождение\b', flags=re.IGNORECASE),
        "negative": re.compile(r'\bОтрицательные \b', flags=re.IGNORECASE),
        "discount": re.compile(r'\bРазмер\b', flags=re.IGNORECASE),
        "finance": re.compile(r'\bфинансовой\b', flags=re.IGNORECASE)
    }
    columns = {}

    def __init__(self, link: str):
        self.link = link


    def downloadFile(self) -> bool:
        try: 
            response = requests.get(self.link, verify=False)

            if response.status_code == 200:
                print(f"ParseHTML: File content saved")

                self.fileContent = response.content
            else:
                print(f"ParseHTML: Failed to download the file. Status code: {response.status_code}")

        except requests.exceptions.RequestException as re:
            print(f"ParseHTML: Failed to download the file: {re}")
            return False
        
        except Exception as e:
            print(f"ParseHTML: An unexpected error occurred: {e}")
            return False

        return True    


    def parseFile(self) -> list:
        if self.fileContent is None:
            print(f"ParseHTML: File content is empty. Download the file first.")
            return None

        try:
            soup = BeautifulSoup(self.fileContent, 'html.parser')
            tables = soup.find_all('table')
            last_table = tables[-1]
            data = []
            header = []

            for th in last_table.find('tr').find_all('th'):
                header.append(th.get_text(strip=True))

            for col_name in header:
                for pattern in self.patterns:
                    if self.patterns[pattern].search(col_name):
                        self.columns[col_name] = pattern

            for row in last_table.find_all('tr')[2:]:
                row_data = [td.get_text(strip=True) for td in row.find_all('td')]
                participant_info = {}

                for col_name, value in zip(header, row_data):
                    if col_name in self.columns:
                        participant_info[self.columns[col_name]] = value

                data.append(participant_info)

            return data

        except Exception as e:
            print(f"ParseHTML: An unexpected error occurred: {e}")
            return None
        

    def extractHeaders(self, header):
        for th in last_table.find('tr').find_all('th'):
            header.append(th.get_text(strip=True))

        for col_name in header:
            for pattern in self.patterns:
                if self.patterns[pattern].search(col_name):
                    self.columns[col_name] = pattern


# bin_pattern = re.compile(r'\bБИН\b', flags=re.IGNORECASE)
# name_pattern = re.compile(r'\bНаименование\b', flags=re.IGNORECASE)
# pun_pattern = re.compile(r'\bналогов\b', flags=re.IGNORECASE)
# experience_pattern = re.compile(r'\bОпыт\b', flags=re.IGNORECASE)
# address_pattern = re.compile(r'\bНахождение\b', flags=re.IGNORECASE)
# negative_pattern = re.compile(r'\bОтрицательные \b', flags=re.IGNORECASE)
# discount_pattern = re.compile(r'\bРазмер\b', flags=re.IGNORECASE)
# finance_pattern = re.compile(r'\bфинансовой\b', flags=re.IGNORECASE)