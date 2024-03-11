import yaml
import requests
from bs4 import BeautifulSoup
import re
import json

def main():

    # Open the config file with yaml
    with open('config.yml', 'r') as file:
        data = yaml.safe_load(file)
        config = data["RESULTS_PARSER"]["TESTS"][0]

    # Get the parameters from the config file
    tendername = config["tendername"]
    filename = config["filename"]
    link = config["link"]

    # Get the file (download it)
    response = requests.get(link, verify=False)
    fileContent = response.content

    # soupify the file
    soup = BeautifulSoup(fileContent, 'html.parser')
    tables = soup.find_all('table')

    table_results = tables[-1]
    table_experience = tables[-2]

    print("Results table")
    print(table_results, "\n\n")

    print("Experience table")
    print(table_experience, "\n\n")

    participants_info = []
    dict_participants = {}

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

        # print(json.dumps(participant, indent=4))

        dict_participants[participant["b_id"]] = participant
        participants_info.append(participant)


    for row in table_results.find_all('tr')[2:]:
        row_data = [td.get_text(strip=True) for td in row.find_all('td')]
        
        participant_info = dict_participants[row_data[2]]

        participant_info["bid"] = row_data[4]
        participant_info["financial_stability"] = row_data[8]
        participant_info["applied_time"] = row_data[9]

        # print (participant_info)

    print(json.dumps(participants_info, indent=4))


if __name__ == "__main__":
    main()