import json
import requests
import pprint
import os

def lambda_handler(request, context):


    print(request)

    if not request["state"]:
        request["state"]["projectsCursor"] = "2014-01-01"

    # Fetch records using api calls
    (insertTransactions, newTransactionCursor) = api_response(request['state'], request['secrets'])
    # Populate records in insert

    insert = {}
    insert['projects'] = insertTransactions
    state = {}
    state['projectsCursor'] = newTransactionCursor

    schema = {}
    transactionsSchema = {}
    transactionsSchema['primary_key'] = ['id']
    schema['projects'] = transactionsSchema

    response = {}
    # Add updated state to response
    response['state'] =  state
    # Add all the records to be inserted in response
    response['insert'] = insert
    # Add schema defintion in response
    response['schema'] = schema
    # Add hasMore flag
    response['hasMore'] = 'false'

    #print(json.dumps(response, indent=4, sort_keys=True))

    return response

def api_response(state, secrets):
    print(state['projectsCursor'])
    endpoint = "https://invisodanmark.harvestapp.com/"
    harvest_token ="639717.pt.YhyRXRe9At65SHz0YJNrIEV0yuSVUBfUPpmRGZLKR6XuoAyWFWEnuNlPniiqspwSCfX6EqfuNK80-bGTGinROA"
    headers = {
        'authorization': "Bearer " + harvest_token,
        'content-type': "application/json",
        'accept': "application/json",
        'User-Agent': 'Harvest API Example',
        'Harvest-Account-ID': '586549'
    }

    payload={}

    url = "https://api.harvestapp.com/v2/projects?updated_since="+state['projectsCursor']
    response = requests.request("GET", url, headers=headers, data=payload)

    data  = response.json()
    data_content = data["projects"]

    maxs = max(data_content, key=lambda ev: ev['updated_at'])["updated_at"]

    data_content = [dict(
        id=k1["id"],
        name=k1["name"],
        updated_at=k1["updated_at"],
        created_at=k1["created_at"]
    ) for k1 in data_content]

    #print(json.dumps(data_content, indent=4, sort_keys=True))

    insertTransactions = data_content

    return (insertTransactions, '2018-01-01T00:00:00Z')

if os.environ.get("AWS_EXECUTION_ENV") is None:
    request = {}
    #request['state'] = {'projectsCursor': '2018-01-01T00:00:00Z'}
    request['state'] = {}
    request['secrets'] = 'secret'
    ref = lambda_handler(request, "context")
