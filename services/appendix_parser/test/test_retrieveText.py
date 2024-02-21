# print current working directory
import sys
sys.path.append('/mnt/nfs/homes/akalimol/my_git/gss_market')

from services.appendix_parser.RetrieveText import GetText


def main():
    print("Testing GetTextFromFile")

    # Create an instance of the class
    tester = GetText()

    # Test the function
    while (True):
        filename = input("Enter the name of the file: ")
        path = "services/appendix_parser/examples/" + filename

        text = tester.get_text(path)
        print(text)


if __name__ == "__main__":
    main()