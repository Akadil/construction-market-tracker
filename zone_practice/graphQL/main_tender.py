import requests
from dotenv import dotenv_values
import urllib3
import json

urllib3.disable_warnings()

def main():
    """ ==================================================================== """
    """ 
        Goal:   Get the proper data using proper filters from the API 

        Filters: 
            - (refTradeMethodsId) - Trading method 
            - (refSubjectTypeId) - Type of the tender
            - (refBuyStatusId) - Status of the tender 
            - (finYear) - Year of the tender 
            - (orgBin) - BIN of the organizer 
            
            - (kato) - KATO code of the tender
            - (publishDate) - Date of the tender publication

        Results:    All data was retrieved successfully
    """
    """ ==================================================================== """
    
    envVar = dotenv_values(".env")
    url2 = f'{envVar["API_URL"]}/v3/graphql'
    token = envVar["TOKEN"]
    isContinue = True
    lastId = None

    # Continue till user wants to stop
    while isContinue:
        # Make an API call
        info = getResponse(url2, token, lastId)
        tenders = info["data"]["TrdBuy"]

        # Get all the distinct statuses
        for tender in tenders:
            if (str(tender["isConstructionWork"]) == "4"):
                print(json.dumps(tender, indent=2, ensure_ascii=False))

        # ask the user if he wants to continue
        if (info["extensions"]["pageInfo"]["hasNextPage"]):
            isContinue = input("Would you like to continue? (y/n) ")
            if (isContinue == "n"):
                isContinue = False
            else:
                lastId = tenders[-1]["id"]
                isContinue = True
        else:
            isContinue = False


def getResponse(url: str, token: str, cursor: str):

    query = """
        query($filter: TrdBuyFiltersInput, $limit: Int, $after: Int) {
            TrdBuy(filter: $filter, limit: $limit, after: $after) {
                id
                numberAnno
                nameRu
                nameKz
                totalSum
                refTradeMethodsId
                orgBin
                orgNameRu
                startDate
                endDate
                publishDate
                itogiDatePublic
                biinSupplier
                isConstructionWork
                finYear
                kato
                Lots
                {
                    count
                    amount
                    nameRu
                    descriptionRu
                    isConstructionWork
                    Customer
                    {
                        bin
                        nameRu
                        Address
                        {
                            id
                            address
                            katoCode
                        }
                    } 
                    Files
                    {
                        filePath
                        originalName
                        nameRu
                    }
                }
                Files
                {
                    filePath
                    originalName
                    nameRu
                }
            }
        }    
    """

    variables = {
        "filter": {
            "orgBin": "920940000211",
            "refBuyStatusId": [210, 220, 230, 240, 250, 260, 350, 440],
            "refSubjectTypeId": 2,
            "refTradeMethodsId": 188,
            "finYear": 2023,
        }
    }
    if (cursor is not None):
        variables["after"] = cursor

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