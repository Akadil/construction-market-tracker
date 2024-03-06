from . import config, token
from tender_characteristics import TenderCharacteristics
from services.appendix_parser import *

def get_tenders():
    """
        Get the tenders from the GraphQL api

        Returns:
            generator: A generator that yields tenders

        Exceptions:
            Exception: If the api call fails

        @todo: check the characteristic of the tenders
    """
    
    last_cursor = None # The last cursor to get the next page

    # Traverse till no more data is left
    while true:

        # Make an api call to get the tenders
        response = getResponse(last_cursor);
        if (response.status_code != 200):
            response.raise_for_status()
            return
        
        response = response.json()
        tenders = response['data'][config.get("GRAPHQL_NAME")]

        # traverse through tenders
        for tender in tenders:

            # Remove tenders that are not construction work
            if (str(tender["isConstructionWork"]) != "4"):
                continue

            # Check the characteristics of the tender
            characteristics = TenderCharacteristics(tender)
            if (characteristics.is_valid() == False):
                continue
            else:
                characteristics.apply()

            yield tender

        # Check if there is more data
        if (response["extensions"]["pageInfo"]["hasNextPage"]):
            last_cursor = response["extensions"]["pageInfo"]["lastId"]
        else:
            break


def getResponse(self, cursor: str = None):
        variables = {
            "filter": {
                "refSubjectTypeId": 2,    
                "refTradeMethodsId": config.get_tradeMethod_id(),
                "refBuyStatusId": config.get_statusFinished_id(),
                "kato": config.get_allKato(),
                "finYear": 2023,
                "totalSum": 200000000,  # 200 million
            }
        }

        if cursor:
            variables["after"] = cursor

        payload = {
            "query": config.get("QUERY"),
            "variables": variables,
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }
        response = requests.post(config.get("GRAPHQL_URL"), 
                                    json=payload, 
                                    headers=headers, 
                                    verify=False)

        return response