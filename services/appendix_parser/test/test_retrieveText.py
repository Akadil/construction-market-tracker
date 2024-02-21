# print current working directory
import sys
sys.path.append('/mnt/nfs/homes/akalimol/my_git/gss_market')

from services.appendix_parser.RetrieveText import RetrieveText


def main():
    print("Testing GetTextFromFile")

    # Create an instance of the class
    tester = RetrieveText()

    # Test the function
    while (True):
        filename = input("Enter the name of the file: ")
        path = "services/appendix_parser/examples/" + filename

        text = tester.get_text(path)
        print("The text is: ")
        print(text)
        print("-----------------")


if __name__ == "__main__":
    main()