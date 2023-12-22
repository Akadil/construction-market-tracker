import requests
from dotenv import dotenv_values

class ApiGoszakup:

    endpoints: str
    url: str
    token: str
    tenders: list

    def __init__(self, url: str, endpoint: str, token: str) -> None:
        self.url = url
        self.token = token
        self.endpoints = endpoint


    def makeRequest(self, url: str):

        headers: dict = {
            "content-type": "application/json",
            "Authorization": f'Bearer {self.token}'
        }
        response = requests.request("GET", url, headers=headers, verify=False)

        if 200 <= response.status_code < 300:
            print(f"[API Goszakup] Success request {url}")
            return response.json()
        else:
            print(f"[API Goszakup] Error: {response.status_code}, {response.text}")
            return None

    def getTenders(self):

        isFinished = False
        url = f'{self.url}/{self.endpoints}'
        info = self.makeRequest(url)

        # Loop to make iterative API calls
        while (info is not None and isFinished == False):
            tenders = info["items"]
            for tender in tenders:
                if (self.isAppropriate(tender) == False):
                    isFinished = True
                    break
                print("Tender: ", tender["name_ru"])


        return info

    def isAppropriate(self, tender: dict) -> bool:
        


