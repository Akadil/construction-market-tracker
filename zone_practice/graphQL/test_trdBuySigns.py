import requests
from dotenv import dotenv_values
import urllib3
import json

urllib3.disable_warnings()


def main():
    """ ==================================================================== """
    """
        Test:   Check all possiblities of trdBuySigns

        Results: Strange results. 0, 2, 6<= numbers are valid.
                    No results. Hypothesis failed
    """
    """ ==================================================================== """

    # Prepare the variables
    envVar = dotenv_values(".env")
    url2 = f'{envVar["API_URL"]}/v3/graphql'
    token = envVar["TOKEN"]
    isContinue = True
    lastId = None
    distinctTenders = dict()

    # Continue till user wants to stop
    for i in range(0, -2147483647, -1):
        # Make an API call
        info = getResponse(url2, token, lastId, i)
        # print(info)
        tenders = info["data"]["TrdBuy"]

        # Get all the distinct statuses
        if (tenders is not None and len(tenders) > 0):
            print(f'{i} is a valid sign')
            print(json.dumps(info, indent=2, ensure_ascii=False))

    # print(json.dumps(data, indent=2, ensure_ascii=False))

def getResponse(url: str, token: str, cursor: str, sign: int):

    query = """
        query($filter: TrdBuyFiltersInput, $limit: Int, $after: Int) {
            TrdBuy(filter: $filter, limit: $limit, after: $after) {
                nameRu
                isConstructionWork
                Lots
                {
                    nameRu
                    isConstructionWork
                    psdSign
                }
            }
        } 
    """

    variables = {
        "limit": 1,
        "filter": {
            
            "refBuyStatusId": [210, 220, 230, 240, 250, 260, 350, 440],
            "refSubjectTypeId": 2,
            "refTradeMethodsId": 188,
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

    # print(response.status_code)
    return response.json()


if __name__ == "__main__":
    main()