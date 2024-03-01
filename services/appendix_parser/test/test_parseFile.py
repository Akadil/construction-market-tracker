from ParseFile import ParseFile
import logging
import yaml
import urllib3

urllib3.disable_warnings()

logging.basicConfig(
    level=logging.INFO,
    format='[%(name)s] - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def main():
    logger.info("Testing ParseFile")

    # write me a code to open the config file in yaml format
    with open("config.yml", "r") as file:
        config = yaml.safe_load(file)["PARSEFILE"]

    # Create an instance of the class
    parser = ParseFile()

    # Test the function
    for test in config["TEST"]:

        try:
            result = parser.parseFile(test["name"], test["url"])

            logger.info(f"File: {test['name']} parsed successfully")
            logger.info(f"Data: {result}")

        except Exception as e:
            logger.error(f"Error: {str(e)}")


if __name__ == "__main__":
    main()