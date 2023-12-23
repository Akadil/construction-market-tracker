import requests
from dotenv import dotenv_values
import urllib3

urllib3.disable_warnings()

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
    token = envVar["TOKEN"]
    
    # Start the program
    info = getResponse(url, token)

    print("\n====================================")
    print(info)

if __name__ == "__main__":
    main()