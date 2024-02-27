# print current working directory
import sys
sys.path.append('/mnt/nfs/homes/akalimol/my_git/gss_market')

import logging

logging.basicConfig(level=logging.WARNING, 
            format='[%(name)s] - %(levelname)s - %(message)s')
myPath = "services/appendix_parser/"

from services.appendix_parser.RetrieveText import RetrieveText

def main():
    print("Testing GetTextFromFile")

    # Create an instance of the class
    tester = RetrieveText()

    # Test the function
    for i in range(1, 10):
        path = f"{myPath}examples/appendix_{str(i)}.pdf"

        # try:
        text = tester.retrieve(path)

        print(f"File: {path} parsed successfully")

        # write the content of text into a file
        with open(f"{myPath}/examples/rt_results/appendix_{str(i)}.txt", "w") as file:
            file.write(text)

        # except Exception as e:
        #     print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()