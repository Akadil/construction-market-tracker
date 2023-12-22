import ApiGoszakup

def main():
    print("Hello world")

    apiGoszakup = ApiGoszakup.ApiGoszakup()
    tenders = apiGoszakup.getData()

if __name__  == "__main__":
    main()