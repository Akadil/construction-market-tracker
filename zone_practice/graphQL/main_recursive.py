import requests
from dotenv import dotenv_values
import urllib3
import json

urllib3.disable_warnings()


def main():
    """ ==================================================================== """
    """
        Test:   Develop a code that will recursively call the API and get all
                the data from it. Plus I need to get all the possibilities of
                "RefBuyStatus"
        
    """
    """ ==================================================================== """

    # Prepare the variables
    envVar = dotenv_values(".env")
    url2 = f'{envVar["API_URL"]}/v3/graphql'
    token = envVar["TOKEN"]
    
    # Start the program

    """ ================================================== """
    """                 Print the data                       """
    """ ================================================== """
    isContinue = True
    lastId = None
    distinctStatus = dict()

    while isContinue:
        info = getResponse(url2, token, lastId)
        data = info["data"]["TrdBuy"]

        for tender in data:
            # RefBuyStatus
            if (tender["RefTradeMethods"]["id"] not in distinctStatus):
                distinctStatus[tender["RefTradeMethods"]["id"]] = tender["RefTradeMethods"]

        print(json.dumps(distinctStatus, indent=2, ensure_ascii=False))
        print(f'The number of elements: {len(distinctStatus)} - {distinctStatus.keys()}\n\n')

        if (info["extensions"]["pageInfo"]["hasNextPage"]):
            isContinue = input("Would you like to continue? (y/n) ")
            if (isContinue == "n"):
                isContinue = False
            else:
                lastId = data[-1]["id"]
                isContinue = True
        else:
            isContinue = False

    # Print refBuyStatus

    # print(json.dumps(data, indent=2, ensure_ascii=False))

def getResponse(url: str, token: str, cursor: str):

    # query = """
    #     query($filter: TrdBuyFiltersInput, $limit: Int, $after: Int) {
    #         TrdBuy(filter: $filter, limit: $limit, after: $after) {
    #             id
    #             numberAnno
    #             nameRu
    #             RefBuyStatus
    #             {
    #                 id
    #                 nameRu
    #                 code
    #             }
    #         }
    #     } 
    # """
    query = """
        query($filter: TrdBuyFiltersInput, $limit: Int, $after: Int) {
            TrdBuy(filter: $filter, limit: $limit, after: $after) {
                id
                numberAnno
                nameRu
                RefTradeMethods
                {
                    id
                    nameRu
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