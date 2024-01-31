from django.core.management.base import BaseCommand, CommandError
from projects.models import Tender
import requests
from dotenv import dotenv_values
import urllib3

urllib3.disable_warnings()


class Command(BaseCommand):
    help = "Feed the database with initial data"
    kato_codes = [
        '751110000', '751210000', '751310000', '751410000', '751510000', '751710000', '751810000', '751910000',
        '191000000', '191600000', '192600000', '193200000', '193400000', '193600000', '194000000', '194200000', '194400000',
        '194600000', '194800000', '195000000', '195200000', '195600000', '195800000', '196000000', '196200000', '196400000',
        '196600000', '196800000',
        '331000000', '331800000', '333200000', '333400000', '333600000', '334000000', '334200000', '334400000', '334600000', '334800000'
    ]
    status_codes = [210, 220, 230, 240, 250, 260, 350, 440]
    subject_type_id = 2
    trade_method_id = 188
    api_url = "https://ows.goszakup.gov.kz/v3/graphql"
    graphql_name = "TrdBuy"
    token = None
    query = """
        query($filter: TrdBuyFiltersInput, $after: Int) {
            TrdBuy(filter: $filter, after: $after) {
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
            }
        }    
    """


    def handle(self, *args, **options):
            
        # Get the last updated tender
        """
            last_id - the id of the last tender in the database
        """
        last_id, tenders_to_update = self.get_last_update()


        # traverse through the tenders

        try:
            for tender in self.get_tenders(last_id, tenders_to_update):
                # Create a new tender
                # new_tender = Tender(
                #     id_goszakup=tender['id'],
                #     tender_number=tender['tenderNumber'],
                #     name=tender['name'],
                #     total_sum=tender['amount'],
                #     status=tender['status'],
                #     start_date=tender['startDate'],
                #     end_date=tender['endDate'],
                # )
                # new_tender.save()
                self.stdout.write(
                    self.style.SUCCESS('Successfully fed the database! "%s"' %tender)
                )
                isContinue = input("Let's continue?")


        except Exception as e:
            raise CommandError(e)


        # ======================================================================
        # Print the results
        self.stdout.write(
            self.style.SUCCESS('Successfully fed the database! "%s"' %last_id)
        )
        for tender in tenders_to_update:
            self.stdout.write(
                self.style.SUCCESS('Successfully fed the database! "%s"' %tender)
            )


    def get_tenders(self, last_id: str, updateTenders: list):
        """
            This function is used to get the tenders from the API
        """

        # declare the variables
        env_variables = dotenv_values(".env")
        is_newTenders: bool = True              # Stop condition for new tenders
        is_updateTenders: bool = True           # Stop condition for updated tenders
        next_id = None                          # next id to be used in the API call
        updateTenders_id: list = []             # list of the ids of the updated tenders

        # Define the variables
        if env_variables.keys().__contains__("TOKEN"):
            self.token = env_variables["TOKEN"]
        else:
            raise Exception("Error: No TOKEN env variable")
        updateTenders_id = [tender.id_goszakup for tender in updateTenders]
        is_updateTenders = True if len(updateTenders_id) > 0 else False


        # Continue till lastId reached and no more tenders to update
        while is_newTenders or is_updateTenders:

            # Make an API call
            response = self.getResponse(next_id)
            if (response.status_code != 200):
                raise Exception("Error in API call")
            response = response.json()
            if "errors" in response.keys():
                raise Exception("Some undefined errors")

            # Get the tenders
            tenders = response["data"][self.graphql_name]

            # yield the tenders
            for tender in tenders:
                # check if the tender is already in the database
                if (tender["id"] == last_id):
                    is_newTenders = False
                    if is_updateTenders == False:
                        break
                    continue
                if tender["finYear"] ==  last_id == None:
                    last_id = tender["id"]

                # check if it is a construction work
                if (str(tender["isConstructionWork"]) == "4" and 
                        int(tender["totalSum"]) > 200000000):
                    if is_newTenders == True:
                        tender["isNew"] = True
                        yield tender
                    elif is_updateTenders == True:
                        if tender["id"] in updateTenders_id:
                            updateTenders_id.remove(tender["id"])
                            if updateTenders_id.__len__() == 0:
                                is_updateTenders = False
                            tender["isNew"] = False
                            yield tender
                    else:
                        break
                    

            # ask the user if he wants to continue
            if (response["extensions"]["pageInfo"]["hasNextPage"]):
                next_id = tenders[-1]["id"]
            elif is_newTenders == True or is_updateTenders == True:
                    raise Exception("Error: something went wrong. No more tenders, \
                                                but the last tender was not reached")


    def getResponse(self, cursor: str):
        variables = {
            "filter": {
                "refBuyStatusId": self.status_codes,
                "refSubjectTypeId": self.subject_type_id,    
                "refTradeMethodsId": self.trade_method_id,
                "kato": self.kato_codes,
            }
        }

        if cursor:
            variables["after"] = cursor

        payload = {
            "query": self.query,
            "variables": variables,
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
        }
        response = requests.request("POST", self.api_url, json=payload, headers=headers, verify=False)

        return response


    def get_last_update(self):
        """
            This function is used to get the current state of the database
        """

        # declare the variables
        last_id: str = None
        tenders_to_update: list = []

        # Get the last updated tender
        if (Tender.objects.count() == 0):
            return last_id, tenders_to_update
        else:
            # order_by("-id") - descending order / actually can take directly the first element
            # first() - returns the first element
            # id_goszakup - the id of the tender in the goszakup
            last_id = Tender.objects.order_by("-id").first().id_goszakup
        
        # Get all the tenders that need to be updated
        tenders_to_update = Tender.objects.filter(
            status__in=[
                "Published",
                "PublishedOrderTaking",
                "PublishedAdditionDemands",
                "PublishedPriceOffers",
                "BidReview",
                "BidAdditionalReview",
                "CompleteWaiting",
                "OnAppellation",
                "BeforeReviwePI",
            ]
        )

        return last_id, tenders_to_update
