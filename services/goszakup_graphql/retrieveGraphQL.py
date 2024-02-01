import urllib3
from dotenv import dotenv_values
import requests

urllib3.disable_warnings()

class Graphqltio:
    """ ==================================================================== """
    """
        Goal:   Create a class that will work with GraphQL API

                Retrieve all finished tenders from the API

        TODO:   INIT: Work with SMTH.graphql and its generated code
                    check for its existence      
    """
    """ ==================================================================== """
    url: str
    endpoint: str
    token: str
    refBuyStatusId: list = [210, 220, 230, 240, 250, 260, 350, 440]
    refSubjectTypeId: int = 2,
    refTradeMethodsId: int = 188,

    def __init__(self, endpoint: str):
        envVar = dotenv_values(".env")

        if (envVar["API_URL"] == ""):
            raise Exception("API_URL is not set in .env file")
        if (envVar["TOKEN"] == ""):
            raise Exception("TOKEN is not set in .env file")
        
        self.url = envVar["API_URL"]
        self.token = envVar["TOKEN"]
        self.endpoint = endpoint

        # get the values from generateted code

    def getFinishedTenders(self):
        # Keep making requests till hasNextPage is False
        while True:

            info = self.getRespoonse(self.query, self.variables)
            tenders = info["data"]["TrdBuy"]

            for tender in tenders:
                



    def getRespoonse(self, query: str, variables: dict):

        url = f'{self.url}{self.endpoint}'
        json = {
            "query": query,
            "variables": variables
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f'Bearer {self.token}'
        }

        response = requests.request("POST", url=url, json=json, 
                                    headers=headers, verify=False)

        if (response.status_code == 200):
            return response.json()
        return None


def main():

    try:
        gql = Graphqltio("/v3/graphql")
    except() as e:
        print("Error")

if __name__ == "__main__":
    main()