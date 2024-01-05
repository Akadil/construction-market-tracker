import requests
from dotenv import dotenv_values
import urllib3
import json

urllib3.disable_warnings()


def main():
    """ ==================================================================== """
    """
        Test:   Get all possible values of kato code from the API

        Results: No way to check it. Just retrieve all the data and check 
                    it manually
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
    while isContinue:
        # Make an API call
        info = getResponse(url2, token, lastId)
        # print(info)
        tenders = info["data"]["TrdBuy"]

        # Get all the distinct statuses
        for tender in tenders:
            # if (tender["Lots"][0]["psdSign"] not in distinctTenders):
            #     distinctTenders[tender["Lots"][0]["psdSign"]] = tender
            # else:
            #     print("Duplicate: ", tender["Lots"][0]["psdSign"])
            #     print(json.dumps(tender, indent=2, ensure_ascii=False))
            print(json.dumps(tender, indent=2, ensure_ascii=False))

        print("====================================\n\n")
        # print(json.dumps(distinctTenders, indent=2, ensure_ascii=False))
        # print("Total: ", len(distinctTenders))

        if (info["extensions"]["pageInfo"]["hasNextPage"]):
            isContinue = input("Would you like to continue? (y/n) ")
            if (isContinue == "n"):
                isContinue = False
            else:
                lastId = info["extensions"]["pageInfo"]["lastId"]
                isContinue = True
        else:
            isContinue = False

    # print(json.dumps(data, indent=2, ensure_ascii=False))

def getResponse(url: str, token: str, cursor: str):

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