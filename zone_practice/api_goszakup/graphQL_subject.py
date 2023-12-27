import requests
from dotenv import dotenv_values
import urllib3
import json

urllib3.disable_warnings()

def getResponse(url: str, token: str):

    query = """
        query($filter: SubjectFiltersInput) {
            Subjects(filter: $filter) {
                pid
                bin
                iin
                inn
                unp
                regdate
                crdate
                indexDate
                numberReg
                series
                name
                nameRu
                nameKz
                fullName
                fullNameRu
                fullNameKz
                email
                phone
                website
                lastUpdateDate
                countryCode
                katoList
                qvazi
                customer
                organizer
                markNationalCompany
                refKopfCode
                markAssocWithDisab
                year
                markResident
                systemId
                supplier
                typeSupplier
                krpCode
                branches
                parentSubject
                okedList
                kseCode
                markWorldCompany
                markStateMonopoly
                markNaturalMonopoly
                markPatronymicProducer
                markPatronymicSupplyer
                markSmallEmployer
                isSingleOrg
                Address
                {   
                    id
                    pid
                    refSourceCode
                    addressType
                    address
                    katoCode
                    phone
                    countryCode
                    dateCreate
                    editDate
                    systemId
                    indexDate
                    RefKato
                    {
                        nameRu
                        nameKz
                        code
                        level
                        hij
                        fullNameKz
                        fullNameRu
                        parentCode
                        k
                        ef
                        ab
                        cd
                    }
                }
                Employees
                {
                    id
                    personId
                    pid
                    iin
                    resident
                    fio
                    disabled
                    role
                    roleName
                    startDate
                    editDate
                    endDate
                    systemId
                    indexDate
                }
                Admins
                {        
                    id
                    subjectId
                    adminId
                    bin
                    nameKz
                    nameRu
                    budgetKz
                    budgetRu
                    startDate
                    indexDate
                }
            }
        }
    """

    variables = {
        "filter": {
            "bin": "060240002985"
        }
    }

    payload = {
        "operationName": None,
        "variables": variables,
        "query": query,
    }

    headers: dict = {
        "content-type": "application/json",
        "Authorization": f'Bearer {token}'
    }
    response = requests.request("POST", url, json=payload, headers=headers, verify=False)

    print(response.status_code)
    return response.json()

def main():
    print("Get the response from the website:")
    print("==========================\n")

    # =================================================
    # Get env variables
    # =================================================
    envVar = dotenv_values(".env")

    # assign env variables
    url = f'{envVar["API_URL"]}/v3/graphql'
    token = envVar["TOKEN"]
    
    # Start the program
    # info = getResponse(url, token)
    info = getResponse(url, token)

    print("\n====================================")
    print(json.dumps(info, indent=2))

if __name__ == "__main__":
    main()

"""
{
  "data": {
    "Subjects": [
      {
        "pid": 91848,
        "bin": "060240002985",
        "iin": "",
        "inn": "",
        "unp": "",
        "regdate": "2023-02-10 00:00:00",
        "crdate": 2016,
        "indexDate": "2023-12-27 03:10:02",
        "numberReg": "4844",
        "series": "",
        "name": null,
        "nameRu": "\u0422\u041e\u041e \"\u0413\u0443\u043d\u043d \u0421\u0442\u0440\u043e\u0439 \u0441\u0435\u0440\u0432\u0438\u0441\"",
        "nameKz": "\"\u0413\u0443\u043d\u043d \u0421\u0442\u0440\u043e\u0439 \u0441\u0435\u0440\u0432\u0438\u0441\" \u0416\u0428\u0421",
        "fullName": null,
        "fullNameRu": "\u0422\u043e\u0432\u0430\u0440\u0438\u0449\u0435\u0441\u0442\u0432\u043e \u0441 \u043e\u0433\u0440\u0430\u043d\u0438\u0447\u0435\u043d\u043d\u043e\u0439 \u043e\u0442\u0432\u0435\u0442\u0441\u0442\u0432\u0435\u043d\u043d\u043e\u0441\u0442\u044c\u044e \"\u0413\u0443\u043d\u043d \u0421\u0442\u0440\u043e\u0439 \u0441\u0435\u0440\u0432\u0438\u0441\"",
        "fullNameKz": "\"\u0413\u0443\u043d\u043d \u0421\u0442\u0440\u043e\u0439 \u0441\u0435\u0440\u0432\u0438\u0441\" \u0436\u0430\u0443\u0430\u043f\u043a\u0435\u0440\u0448\u0456\u043b\u0456\u0433\u0456 \u0448\u0435\u043a\u0442\u0435\u0443\u043b\u0456 \u0441\u0435\u0440\u0456\u043a\u0442\u0435\u0441\u0442\u0456\u0433\u0456",
        "email": "gunn_stroi@mail.ru",
        "phone": "+77717017440",
        "website": "",
        "lastUpdateDate": "2023-02-13 12:41:20",
        "countryCode": "398",
        "katoList": [
          "750000000"
        ],
        "qvazi": 0,
        "customer": 0,
        "organizer": 0,
        "markNationalCompany": 0,
        "refKopfCode": "\u0422\u041e\u041e",
        "markAssocWithDisab": 0,
        "year": 2023,
        "markResident": 1,
        "systemId": 3,
        "supplier": 1,
        "typeSupplier": 1,
        "krpCode": 0,
        "branches": [
          ""
        ],
        "parentSubject": "",
        "okedList": 41202,
        "kseCode": 5,
        "markWorldCompany": 0,
        "markStateMonopoly": 0,
        "markNaturalMonopoly": 0,
        "markPatronymicProducer": 0,
        "markPatronymicSupplyer": 0,
        "markSmallEmployer": 0,
        "isSingleOrg": 0,
        "Address": [
          {
            "id": 79722,
            "pid": 91848,
            "refSourceCode": 2,
            "addressType": 1,
            "address": "\u0433.\u0410\u043b\u043c\u0430\u0442\u044b, \u0443\u043b. \u041c\u0438\u043a\u0440\u043e\u0440\u0430\u0439\u043e\u043d \u0410\u041b\u041c\u0410\u0421, \u0434\u043e\u043c 210",
            "katoCode": "750000000",
            "phone": "2971627",
            "countryCode": 398,
            "dateCreate": "2016-02-19 10:18:58",
            "editDate": "2023-09-13 18:18:35",
            "systemId": 3,
            "indexDate": "2023-12-27 03:11:38",
            "RefKato": {
              "nameRu": "\u0433.\u0410\u043b\u043c\u0430\u0442\u044b",
              "nameKz": "\u0410\u043b\u043c\u0430\u0442\u044b \u049b.",
              "code": "750000000",
              "level": 1,
              "hij": "000",
              "fullNameKz": "\u0410\u043b\u043c\u0430\u0442\u044b \u049b.",
              "fullNameRu": "\u0433.\u0410\u043b\u043c\u0430\u0442\u044b",
              "parentCode": "000000000",
              "k": 1,
              "ef": "00",
              "ab": "75",
              "cd": "00"
            }
          }
        ],
        "Employees": [
          {
            "id": "91848_186060",
            "personId": 186060,
            "pid": 91848,
            "iin": "670817301315",
            "resident": 1,
            "fio": "\u0410\u041c\u0418\u0420\u0413\u0410\u041b\u0418\u0415\u0412 \u0415\u0420\u0422\u0418\u0421\u0425\u0410\u041d \u041d\u0415\u0421\u0418\u041f\u0425\u0410\u041d\u041e\u0412\u0418\u0427",
            "disabled": 0,
            "role": 1,
            "roleName": "\u0420\u0443\u043a\u043e\u0432\u043e\u0434\u0438\u0442\u0435\u043b\u044c",
            "startDate": "2016-02-19 10:18:59",
            "editDate": "2023-02-13 12:41:20",
            "endDate": "2099-01-01 00:00:00",
            "systemId": null,
            "indexDate": "2023-12-27 03:12:29"
          },
          {
            "id": "91848_186042",
            "personId": 186042,
            "pid": 91848,
            "iin": "750217400517",
            "resident": 1,
            "fio": "\u0410\u041c\u0418\u0420\u0413\u0410\u041b\u0418\u0415\u0412\u0410 \u0410\u0419\u041a\u0415\u0420\u0418\u041c \u041d\u0415\u0421\u0418\u041f\u0425\u0410\u041d\u041e\u0412\u041d\u0410",
            "disabled": 0,
            "role": 2,
            "roleName": "\u0421\u043e\u0442\u0440\u0443\u0434\u043d\u0438\u043a",
            "startDate": "2016-02-19 10:18:58",
            "editDate": "2016-02-19 10:11:49",
            "endDate": "2099-01-01 00:00:00",
            "systemId": null,
            "indexDate": "2023-12-27 03:12:29"
          },
          {
            "id": "91848_1002337",
            "personId": 1002337,
            "pid": 91848,
            "iin": "730110400323",
            "resident": 1,
            "fio": "\u0422\u041e\u0419\u0416\u0410\u041d\u041e\u0412\u0410 \u042d\u041b\u042c\u041c\u0418\u0420\u0410 \u0421\u0410\u0413\u042b\u041d\u0414\u042b\u041a\u041e\u0412\u041d\u0410",
            "disabled": 0,
            "role": 2,
            "roleName": "\u0421\u043e\u0442\u0440\u0443\u0434\u043d\u0438\u043a",
            "startDate": "2022-08-12 13:05:32",
            "editDate": "2022-08-12 13:05:32",
            "endDate": "2099-01-01 00:00:00",
            "systemId": null,
            "indexDate": "2023-12-27 03:12:29"
          }
        ],
        "Admins": null
      }
    ]
  },

"""