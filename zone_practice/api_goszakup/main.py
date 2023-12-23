import ApiGoszakup
from dotenv import dotenv_values

def main():
    print("Hello world")

    envVar = dotenv_values(".env")
    if (envVar.__len__() == 0):
        print("Error: No env variables or no file .env\n")
        return
    elif (envVar.keys().__contains__("API_URL") == False or 
          envVar.keys().__contains__("TOKEN") == False):
        print("Error: No API_URL or TOKEN in .env\n")
        return

    # assign env variables
    url = f'{envVar["API_URL"]}'
    endpoint = 'v3/trd-buy/bin/920940000211'
    token = envVar["TOKEN"]

    apiGoszakup = ApiGoszakup.ApiGoszakup(url, endpoint, token)
    apiGoszakup.getTenders()

if __name__  == "__main__":
    main()