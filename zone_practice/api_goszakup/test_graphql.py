import requests
from dotenv import dotenv_values
import urllib3
import json

urllib3.disable_warnings()

#/help/v3/schema/
def getResponse2(url: str, token: str):
    query = """
    query($filter: TrdBuyFiltersInput) {
        TrdBuy(filter: $filter)
        {
            id
            nameRu
            numberAnno
        }
    }
    """
    query = """
        query($filter: TrdBuyFiltersInput, $limit: Int) {
            TrdBuy(filter: $filter, limit: $limit) {
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
                    customerBin
                    customerNameRu
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
                RefTradeMethods
                {
                    nameRu
                    code
                    isActive
                } 
                RefSubjectType
                {
                    nameRu
                }
                RefBuyStatus
                {
                    nameRu
                    code
                }
            }
        }    
    """

    variables = {
        "limit": 1,
        "filter": {
            "orgBin": "920940000211"
        }
    }

    payload = {
        "operationName": None,
        "variables": variables,
        "query": query,
    }

    headers: dict = {
        "content-type": "application/json",
        "Authorization": f'Bearer {token}'
    }
    response = requests.request("POST", url, json=payload, headers=headers, verify=False)

    print(response.status_code)
    # return json.loads(response.text)
    return response.json()

#/help/v3/schema/
def getResponse(url: str, token: str): 
    headers: dict = {
        "content-type": "application/json",
        "Authorization": f'Bearer {token}'
    }
    response = requests.request("GET", url, headers=headers, verify=False)

    # return json.loads(response.text)
    return response.json()

def main():
    print("Get the response from the website:")
    print("==========================\n")

    # =================================================
    # Get env variables
    # =================================================
    envVar = dotenv_values(".env")

    # assign env variables
    url = f'{envVar["API_URL"]}/help/v3/schema/'
    url2 = f'{envVar["API_URL"]}/v3/graphql'
    token = envVar["TOKEN"]
    
    # Start the program
    # info = getResponse(url, token)
    info = getResponse2(url2, token)

    print("\n====================================")
    print(json.dumps(info, indent=2))

if __name__ == "__main__":
    main()