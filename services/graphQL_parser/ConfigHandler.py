import logging
import regex as re

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

REGEX_OBJECT = re.compile(r"\${[a-zA-Z0-9]+}")

class ConfigHandler:
    """
        The ConfigHandler class is responsible for handling the configuration 
        data. Get the data, format them, formulate the queries and objects

        :todo       Write down some log messages
    """

    data: dict = None       # The configuration data
    queries: dict = None    # All available queries
    objects: dict = None    # All available objects
    filters: dict = None    # All available filters
    inputs: dict = None     # All available inputs

    def __init__(self, config_data: dict):

        if config.get("WHO_AM_I") != "GRAPHQL_PARSER":
            logger.error("Wrong config data passed to ConfigHandler")
            raise ImportError("ConfigHandler not initialized")
        
        self.data = config_data
        self.queries = config_data.get("QUERIES")
        self.objects = config_data.get("OBJECTS")
        self.filters = config_data.get("FILTERS")
        self.inputs = config_data.get("INPUTS")

        logger.setLevel(self.get_logging_level())
        logger.info("ConfigHandler initialized successfully")


    def get_query(self, query_name: str):
        """
            Returns the query 

            :example:
                query($filter: TrdBuyFiltersInput, $after: Int) { TrdBuy { id } }

            :return 
                Fail - returns None
                Success - returns the query

            :questions:
                1. Do I have to throw an exception? Depends on future requirements 
        """

        query: str = self.queries.get(query_name) # The query to get the tenders
        if (query == None):
            logger.error(f"Query {query_name} not found in QUERIES")
            return None

        object_trdbuy = REGEX_OBJECT.search(query, 1)
        if object_trdbuy.get("NAME") != "TrdBuy":
            logger.error("TRDBUY not found in the query")
            
            return None

        object_name = object_trdbuy.group(0)
        extendedQuery = self.extend_query(self.objects.get("TRDBUY"))
        query = query.replace(object_name, extendedQuery)

        return query


    def extend_query(self, parentObject: dict):
        """
            Extends the query by replacing the objects by query

            :example:
                ${ADDRESS}   ->   Address { id address katoCode }

            :param 
                parentObject: The object to be replaced

            :return
                Fail - returns None
                Success - returns the extended query
        """

        query = parentObject.get("QUERY") # The query to get the tenders
        restrictions = parentObject.get("RESTRICTIONS")

        # Iterate through query, if any object found, replace it
        object_regex = REGEX_OBJECT.search(query, 1)

        while (object_regex is not None):               ## if object found
            object_name: str = object_regex.group(0)
            myObject = self.objects.get(object_name[2:-1])

            if myObject == None:
                logger.error(f"Object {object_name} not found in OBJECTS")
                return None
            elif restrictions and restrictions[object[2:-1]] == False:
                # if the object is not allowed to be queried, remove it
                query = query.replace(object_name, "")
            else:
                ## the object may contain another object, so we need to run a recursivity 
                query = query.replace(object_name, self.extend_query(myObject))

            object_regex = REGEX_OBJECT.search(query, 1)
        
        return query
    

    def getFilter_trdbuy(self):
        """
            Returns the filter for the query

            :example:
                { "filter": { "refSubjectTypeId": 2, "refTradeMethodsId": 1, "refBuyStatusId": 1, "kato": 1, "finYear": 2023, "totalSum": 200000000 } }

            :return
                Fail - returns None
                Success - returns the filter
        """

        filter = selt.filters.get(queryName.upper())
    
        filter["kato"] = self.get_allKato()

        return filter


    def get_allKato(self):
        """
            Returns all the kato codes
        """

        returner = []

        for region in self.data['kato']:
            for kato in data['kato'][region]:
                returner.append(kato)
        return returner


    def get_logging_level(self):
        """
            Returns the logging level of current module
        """
        log_level: str = self.data["LOG_LEVEL_CONFIGHANDLER"]

        if (log_level == "debug"):
            return (logging.DEBUG)
        elif (log_level == "info"):
            return (logging.INFO)
        elif (log_level == "warning"):
            return (logging.WARNING)
        
        return (logging.ERROR)
        