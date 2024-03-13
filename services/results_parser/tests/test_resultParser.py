from dotenv import load_dotenv
import os
import yaml
import logging 
import json

logging.basicConfig(level=logging.INFO, 
            format='[%(name)s] - %(levelname)s - %(message)s')

# load the environment variables
load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")


def main():

    # open the config file and read the data in yaml format
    with open("./config.yml", "r") as file:
        config = yaml.safe_load(file)
        config = config["RESULTS_PARSER"]
        tests = config["TESTS"]
    
    # create an instance of the ResultParser class
    from services.results_parser.ResultsParser import ResultsParser
    
    resultParser = ResultsParser()

    # parse the data and return the results
    for test in tests:
        logging.info(f"Testing: {test['name']} for the tender: \n{test['tendername']}\n")
        result = resultParser.parse(test["link"])
        
        data = result["data"]

        # pint the dictionary data beautifully using json.dumps
        # print(json.dumps(data, indent=4))
        
        # print the data by yourself. The data is a list of dictionaries
        for d in data:
            # d is a dictionary
            print(d["lot_number"])

            for participant in d["participants"]:
                for key, value in participant.items():
                    print(f"{key}: {value}")
                print("\n")
            print("\n\n")


if __name__ == "__main__":
    main()