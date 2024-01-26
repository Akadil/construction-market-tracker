import requests
import json
import urllib3
from dotenv import dotenv_values

urllib3.disable_warnings()

envVar = dotenv_values(".env")
url = f'{envVar["API_URL"]}/v3/graphql'
token = envVar["TOKEN"]

# The GraphQL query
# graphql_query = '''
# {
#   __type(name: "TrdBuyFiltersInput") {
#     inputFields {
#       name
#       type {
#         name
#         kind
#         enumValues {
#           name
#         }
#       }
#     }
#   }
# }
# '''

graphql_query = '''
{
  __type(name: "TrdBuyFiltersInput") {
    inputFields {
      name
      type {
        kind
        name
        fields {
            name
            description
            isDeprecated
            deprecationReason
        }
        interfaces {
            name
        }
        possibleTypes {
            name
        }
        inputFields {
            name
        }
        ofType {
            name
        }
        enumValues {
          name
          description
          isDeprecated
          deprecationReason
        }
      }
    }
  }
}
'''

# Set headers for the request
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {token}',}

# Make the request to the GraphQL endpoint
response = requests.post(url, data=json.dumps({'query': graphql_query}), headers=headers, verify=False)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    result = response.json()

    print("GraphQL request succeeded!")
    # print(json.dumps(result, indent=2, ensure_ascii=False))

    # Extract and print the enum values
    for field in result['data']['__type']['inputFields']:
        if field['name'] == 'refTrdBuySigns':
            print(json.dumps(field, indent=2, ensure_ascii=False))
else:
    print("GraphQL request failed with status code:", response.status_code)
    print(response.text)
