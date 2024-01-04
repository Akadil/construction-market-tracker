import requests
from dotenv import dotenv_values
import urllib3
import json

urllib3.disable_warnings()


def main():
    """ ==================================================================== """
    """
        Test: Identify all the available references, codes and etc
        
        1) RefTradeMethods
        2) RefSubjectType
        3) RefBuyStatus

        Results: Almost all data was retrieved (in .md file), except RefBuyStatus.

                But as I understand, only 4xx numbers are bad one and I have to 
                keep going with the rest numbers
    """
    """ ==================================================================== """

    # Prepare the variables
    envVar = dotenv_values(".env")
    url2 = f'{envVar["API_URL"]}/v3/graphql'
    token = envVar["TOKEN"]
    
    # Start the program
    info = getResponse(url2, token)
    data = info["data"]["TrdBuy"]

    """ ================================================== """
    """                 Print the data                       """
    """ ================================================== """
    
    name = []
    refTradeMethods = []
    refSubjectType = []
    refBuyStatus = []

    for tender in data:
        name.append(tender["nameRu"])
        refTradeMethods.append(tender["RefTradeMethods"])
        refSubjectType.append(tender["RefSubjectType"])
        refBuyStatus.append(tender["RefBuyStatus"])
    
    length = len(name)

    # Print tradeMethods
    print("RefTradeMethods: \n =========================")
    for i in range(length):
        # print(f'\n{i+1}) {name[i]}: ', end='')
        print(f'{refTradeMethods[i]}, ')
    print('\n\n')

    # Print refSubjectType
    print("RefSubjectType: \n =========================")
    for i in range(length):
        # print(f'\n{i+1}) {name[i]}: ', end='')
        print(f'{refSubjectType[i]}, ')
    print('\n\n')

    # Print refBuyStatus
    print("RefBuyStatus: \n =========================")
    for i in range(length):
        # print(f'\n{i+1}) {name[i]}: ', end='')
        print(f'{refBuyStatus[i]}, ')

    # print(json.dumps(data, indent=2, ensure_ascii=False))

def getResponse(url: str, token: str):

    query = """
        query($filter: TrdBuyFiltersInput, $limit: Int) {
            TrdBuy(filter: $filter, limit: $limit) {
                id
                numberAnno
                nameRu
                RefTradeMethods
                {
                    id
                    nameRu
                } 
                RefSubjectType
                {
                    id
                    nameRu
                }
                RefBuyStatus
                {
                    id
                    nameRu
                    code
                }
            }
        }    
    """

    variables = {
        "limit": 20,
        "filter": {
            "orgBin": "920940000211"
        }
    }

    payload = {
        "variables": variables,
        "query": query,
    }

    headers: dict = {
        "content-type": "application/json",
        "Authorization": f'Bearer {token}'
    }
    response = requests.request("POST", url, json=payload, headers=headers, verify=False)

    print(response.status_code)
    return response.json()


if __name__ == "__main__":
    main()