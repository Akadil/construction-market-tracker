import requests
from datetime import datetime
import urllib3

urllib3.disable_warnings()

class ApiGoszakup:

    endpoints: str
    url: str
    token: str
    tenders: list
    date_begin: datetime = datetime(2023, 1, 1)
    total_tenders: int

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
        self.total_tenders = int(info["total"])
        lowerBoundRequests: int = 1

        # Loop to make iterative API calls
        while (info is not None and isFinished == False and self.total_tenders > 0 and lowerBoundRequests > 0):
            tenders = info["items"]
            self.total_tenders -= len(tenders)
            for tender in tenders:
                if (self.isAppropriate(tender) == False):
                    continue
                if (self.isOutdated(tender["publish_date"]) == True):
                    isFinished = True
                    break
                print("Tender: ", tender, "\n")

            # Make the next request
            url = f'{self.url}{info["next_page"]}'
            # print("Next page: ", url)
            info = self.makeRequest(url)
            lowerBoundRequests -= 1


    def isAppropriate(self, tender: dict) -> bool:
        # Check the price
        if (int(tender["total_sum"]) < 100000000):
            return False
        if (int(tender["ref_trade_methods_id"]) != 188):
            return False
        if (int(tender["ref_buy_status_id"]) in [190, 410]):
            return False
        return True
    
    def isOutdated(self, tenderDate: str) -> bool:
        date = datetime.strptime(tenderDate, "%Y-%m-%d %H:%M:%S")
        if (date < self.date_begin):
            return True
        return False



