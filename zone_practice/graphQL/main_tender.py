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
            - (isConstructionWork) - Is it a construction work or not
            
            - (orgBin) - BIN of the organizer 
            - (kato) - KATO code of the tender
            - (publishDate) - Date of the tender publication
    """
    """ ==================================================================== """
    
    envVar = dotenv_values(".env")
    url2 = f'{envVar["API_URL"]}/v3/graphql'
    token = envVar["TOKEN"]
    
    # Start the program
    info = getResponse(url2, token)
    data = info["data"]["TrdBuy"][0]

    print(json.dumps(data, indent=2, ensure_ascii=False))


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
                RefTradeMethods
                {
                    id
                    nameRu
                    nameKz
                    code
                    type
                    symbolCode
                    isActive
                    f1
                    ord
                    f2
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
        "filter": {
            "orgBin": "920940000211"
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