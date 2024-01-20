import requests
from dotenv import dotenv_values
import urllib3
import json

urllib3.disable_warnings()


def main():
    """ ==================================================================== """
    """
        Test:   Get all possible values of kato code from the API

        https://tenderplus.kz/kato - all possible KATO codes

        Results:    "?75*" - all the codes of the Almaty city
                    "?19*" - all the codes of the Almaty region
                    "?33*" - all the codes of the Zhetisu region
    """
    """ ==================================================================== """

    # Prepare the variables
    envVar = dotenv_values(".env")
    url2 = f'{envVar["API_URL"]}/v3/graphql'
    token = envVar["TOKEN"]
    isContinue = True
    lastId = None

    # Continue till user wants to stop
    while isContinue:
        # Make an API call
        info = getResponse(url2, token, lastId)
        print(info)
        tenders = info["data"]["TrdBuy"]

        # Get all the distinct statuses
        for tender in tenders:
            print(json.dumps(tender, indent=2, ensure_ascii=False))

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
                isLightIndustry
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
                Cancel
                {
                    id
                    numberDecision
                    dateDecision
                    nameAuthority
                    dateCreate
                    trdBuyId
                    actTypeNameRu
                    actTypeNameKz
                    typeActionsNameRu
                    typeActionsNameKz
                    typeActionsCode
                    systemId
                    indexDate
                }
                Pause
                {
                    id
                    status
                    dateCreate
                    datePause
                    decideNumber
                    decideDate
                    decideDocKz
                    decideDocRu
                    statusNameRu
                    statusNameKz
                    solutionNameRu
                    solutionNameKz
                    lots
                    {
                        id
                    }
                    systemId
                    indexDate
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
            "orgBin": "920940000211",
            "strKato": "?75*",
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