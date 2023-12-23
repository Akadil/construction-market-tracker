import requests
import json
import urllib3
from dotenv import dotenv_values

urllib3.disable_warnings()

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
    if (envVar.__len__() == 0):
        print("Error: No env variables or no file .env\n")
        return
    elif (envVar.keys().__contains__("API_URL") == False or 
          envVar.keys().__contains__("TOKEN") == False):
        print("Error: No API_URL or TOKEN in .env\n")
        return
    else:
        print("Env variables:")
        print("API_URL: ", envVar["API_URL"])
        print("TOKEN: ", envVar["TOKEN"], "\n")

    # assign env variables
    url = f'{envVar["API_URL"]}/v3/trd-buy/bin/920940000211'
    token = envVar["TOKEN"]
    
    # Start the program
    info = getResponse(url, token)
    # print("====================================")
    # print("Response from the website:")
    # print(info, "\n")
    print(info["items"][0].keys(), "\n")

    print("\n====================================")
    print("Response from the website (items):")

    unique_statuses = dict()
    unique_trades = dict()

    for item in info["items"]:
        if item["ref_buy_status_id"] not in unique_statuses:
            unique_statuses[item["ref_buy_status_id"]] = (item["number_anno"], item["name_ru"])
        if item["ref_trade_methods_id"] not in unique_trades:
            unique_trades[item["ref_trade_methods_id"]] = (item["number_anno"], item["name_ru"])
        print(item["publish_date"], item["name_ru"])

    print("====================================")
    print("Unique statuses:")
    print("====================================")
    # print(unique_statuses, "\n")
    for item in unique_statuses:
        print(item, unique_statuses[item])

    print("====================================")
    print("Unique trades:")
    print("====================================")
    # print(unique_trades, "\n")
    for item in unique_trades:
        print(item, unique_trades[item])

if __name__  == "__main__":
    main()
