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
        
        Results:    1. I got all the data from the API (in .md file)
                    2. Just added "after" parameter to the query to get the 
                        data recursively
    """
    """ ==================================================================== """

    # Prepare the variables
    envVar = dotenv_values(".env")
    url2 = f'{envVar["API_URL"]}/v3/graphql'
    token = envVar["TOKEN"]
    isContinue = True
    lastId = None
    distinctStatus = dict()

    # Continue till user wants to stop
    while isContinue:
        # Make an API call
        info = getResponse(url2, token, lastId)
        tenders = info["data"]["TrdBuy"]

        # Get all the distinct statuses
        for tender in tenders:
            if (tender["RefBuyStatus"]["id"] not in distinctStatus):
                distinctStatus[tender["RefBuyStatus"]["id"]] = tender["RefBuyStatus"]

        print(json.dumps(distinctStatus, indent=2, ensure_ascii=False))
        print(f'The number of elements: {len(distinctStatus)} - {distinctStatus.keys()}\n\n')

        if (info["extensions"]["pageInfo"]["hasNextPage"]):
            isContinue = input("Would you like to continue? (y/n) ")
            if (isContinue == "n"):
                isContinue = False
            else:
                lastId = tenders[-1]["id"]
                isContinue = True
        else:
            isContinue = False

    # print(json.dumps(data, indent=2, ensure_ascii=False))

def getResponse(url: str, token: str, cursor: str):

    query = """
        query($filter: TrdBuyFiltersInput, $limit: Int, $after: Int) {
            TrdBuy(filter: $filter, limit: $limit, after: $after) {
                id
                numberAnno
                nameRu
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