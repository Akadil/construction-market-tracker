import requests
import json
from dotenv import dotenv_values

def getResponse(url: str, token: str): 
    payload: str = ""
    headers: dict = {
        "content-type": "application/json",
        "Authorization": f'Bearer {token}',
    }
    response = requests.request("GET", url, data=payload, headers=headers, verify=True)

    return json.loads(response.text)

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
        print("API_URL: ", envVar["API_URL"])
        print("TOKEN: ", envVar["TOKEN"], "\n")

    # assign env variables
    url = f'{envVar["API_URL"]}/v3/trd-buy/bin/920940000211'
    token = envVar["TOKEN"]
    
    # Start the program
    info = getResponse(url, token)
    print(info)


    

if __name__  == "__main__":
    main()
