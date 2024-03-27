class GetTender:
    def __init__(self, config: dict):
        self.tender_id = tender_id

    def get_tenders():
        pass

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
                                json=payload, headers=headers, verify=False)

        return response
