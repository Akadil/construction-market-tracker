from bs4 import BeautifulSoup
import json
import re

def straightForwardWay(html_file='examples/results.html'):

    with open(html_file, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    # Find all tables in the HTML
    tables = soup.find_all('table')

    if not tables:
        print("No tables found in the HTML.")
        return None

    # Select the last table
    last_table = tables[-1]

    # Extract data from the table
    data = []
    header = []

    # Extract column headers
    for th in last_table.find('tr').find_all('th'):
        header.append(th.get_text(strip=True))

    # Define regex patterns for the columns you want to identify
    bin_pattern = re.compile(r'\bБИН\b', flags=re.IGNORECASE)
    inn_pattern = re.compile(r'\bИНН\b', flags=re.IGNORECASE)

    # Create a dictionary to store assigned names for identified columns
    assigned_names = {}

    # Check each header column against the regex patterns
    for col_name in header:
        if bin_pattern.search(col_name):
            assigned_names[col_name] = "BIN"
        elif inn_pattern.search(col_name):
            assigned_names[col_name] = "INN"

    # Iterate through rows and create dictionaries
    for row in last_table.find_all('tr')[1:]:
        row_data = [td.get_text(strip=True) for td in row.find_all('td')]
        participant_info = {}

        # Assign names based on identified columns
        for col_name, value in zip(header, row_data):
            if col_name in assigned_names:
                participant_info[assigned_names[col_name]] = value
                # participant_info[col_name] = value

        data.append(participant_info)

    data.pop(0)
    return data

if __name__ == "__main__":
    participants = straightForwardWay()
    for participant in participants:
        print(json.dumps(participant, indent=2, ensure_ascii=False))