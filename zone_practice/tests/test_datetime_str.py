from datetime import datetime

def main():
    """
        Test: Check the nature of the datetime
    """

    qwe = datetime.now().strftime("%Y-%m-%d_%H:%M:%S").__str__()
    asd = str(datetime.now().strftime("%Y-%m-%d_%H:%M:%S"))
    print(qwe)
    print(type(qwe))

    print(asd)
    print(type(asd))

main()

