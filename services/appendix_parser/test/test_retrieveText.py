from RetrieveText import RetrieveText
import logging

logging.basicConfig(
    level=logging.INFO, 
    format='[%(name)s] - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    logger.info("Testing GetTextFromFile")

    # Create an instance of the class
    tester = RetrieveText()

    # Test the function
    for i in range(1, 10):
        path = f"./test/examples/appendix_{str(i)}.pdf"

        # try:
        text = tester.retrieve(path)

        logger.info(f"File: {path} parsed successfully")

        # write the content of text into a file
        with open(f"test/results/appendix_{str(i)}.txt", "w") as file:
            file.write(text)

        # except Exception as e:
        #     print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()