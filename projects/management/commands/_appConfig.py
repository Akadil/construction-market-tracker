from dotenv import dotenv_values

"""
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
                    id
                    lotNumber
                    refLotStatusId
                    count
                    amount
                    nameRu
                    nameKz
                    descriptionRu
                    descriptionKz
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
                    RefLotsStatus
                    {
                        id
                        nameRu
                        nameKz
                        code
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


"""

class AppConfig:

    KATO_CODES = [
        '751110000', '751210000', '751310000', '751410000', '751510000', '751710000', '751810000', '751910000',
        '191000000', '191600000', '192600000', '193200000', '193400000', '193600000', '194000000', '194200000', '194400000',
        '194600000', '194800000', '195000000', '195200000', '195600000', '195800000', '196000000', '196200000', '196400000',
        '196600000', '196800000',
        '331000000', '331800000', '333200000', '333400000', '333600000', '334000000', '334200000', '334400000', '334600000', '334800000'
    ]

    STATUS_CODES = [210, 220, 230, 240, 250, 260, 350, 440]
    SUBJECT_TYPE = 2
    TRADE_METHOD_ID = 188
    API_URL = "https://ows.goszakup.gov.kz/v3/graphql"
    GRAPHQL_NAME = "TrdBuy"
    TOKEN = None
    QUERY = """
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
                    id
                    lotNumber
                    refLotStatusId
                    count
                    amount
                    nameRu
                    nameKz
                    descriptionRu
                    descriptionKz
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
                    RefLotsStatus
                    {
                        id
                        nameRu
                        nameKz
                        code
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

    def __init__(self):

        # Initialize the token for retrieving data from Goszakup
        env_variables = dotenv_values(".env")

        if env_variables.keys().__contains__("TOKEN"):
            self.TOKEN = env_variables["TOKEN"]






