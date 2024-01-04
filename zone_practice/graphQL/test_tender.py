import requests
from dotenv import dotenv_values
import urllib3
import json

urllib3.disable_warnings()

def getResponse2(url: str, token: str):

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

def decoder(text: str):
    print("Pre: ", text)
    raw_text = r'{}'.format(text)
    decoded_text = bytes(raw_text, "utf-8").decode("unicode_escape")
    print("Post: ", decoded_text)
    return decoded_text


def main():
    print("Get the response from the website:")
    print("==========================\n")

    # =================================================
    # Get env variables
    # =================================================
    envVar = dotenv_values(".env")

    # assign env variables
    url2 = f'{envVar["API_URL"]}/v3/graphql'
    token = envVar["TOKEN"]
    
    # Start the program
    # info = getResponse(url, token)
    info = getResponse2(url2, token)
    data = info["data"]["TrdBuy"][0]

    # data["nameRu"] = decoder(data["nameRu"])
    # data["nameKz"] = decoder(data["nameKz"])
    # data["orgNameRu"] = decoder(data["orgNameRu"])
    # data["Lots"][0]["nameRu"] = decoder(data["Lots"][0]["nameRu"])
    # data["Lots"][0]["descriptionRu"] = decoder(data["Lots"][0]["descriptionRu"])
    # data["Lots"][0]["Customer"]["nameRu"] = decoder(data["Lots"][0]["Customer"]["nameRu"])
    # data["Lots"][0]["Customer"]["Address"][0]["address"] = decoder(data["Lots"][0]["Customer"]["Address"][0]["address"])
    # data["Lots"][0]["Customer"]["Address"][1]["address"] = decoder(data["Lots"][0]["Customer"]["Address"][1]["address"])
    # data["Lots"][0]["Files"][0]["nameRu"] = decoder(data["Lots"][0]["Files"][0]["nameRu"])
    # data["Lots"][0]["Files"][1]["nameRu"] = decoder(data["Lots"][0]["Files"][1]["nameRu"])
    # data["Lots"][0]["Files"][2]["nameRu"] = decoder(data["Lots"][0]["Files"][2]["nameRu"])
    # data["Files"][0]["nameRu"] = decoder(data["Files"][0]["nameRu"])
    # data["Files"][1]["nameRu"] = decoder(data["Files"][1]["nameRu"])

    # data["RefTradeMethods"]["nameRu"] = decoder(data["RefTradeMethods"]["nameRu"])
    # data["RefSubjectType"]["nameRu"] = decoder(data["RefSubjectType"]["nameRu"])
    # data["RefBuyStatus"]["nameRu"] = decoder(data["RefBuyStatus"]["nameRu"])

    print("\n====================================")
    # print(data)
    print(json.dumps(data, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()