import json
import requests
import pprint

def lambda_handler(request, context):

    # Fetch records using api calls
    (insertTransactions, newTransactionCursor) = api_response(request['state'], request['secrets'])
    # Populate records in insert
    insert = {}
    insert['transactions'] = insertTransactions
    state = {}
    state['transactionsCursor'] = newTransactionCursor
    transactionsSchema = {}
    transactionsSchema['primary_key'] = ['id']
    schema = {}
    schema['transactions'] = transactionsSchema
    response = {}
    # Add updated state to response
    response['state'] =  state
    # Add all the records to be inserted in response
    response['insert'] = insert
    # Add schema defintion in response
    response['schema'] = schema
    # Add hasMore flag
    response['hasMore'] = 'false'
    return response

def api_response(state, secrets):

    # your api call goes here
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

    url = "https://api.harvestapp.com/v2/projects?updated_since="+request['state']['transactionsCursor']
    response = requests.request("GET", url, headers=headers, data=payload)

    data  = response.json()
    data_content = data["projects"]

    maxs = max(data_content, key=lambda ev: ev['updated_at'])["updated_at"]

    data_content = [dict(
        id=k1["id"],
        name=k1["name"],
        updated_at=k1["updated_at"],
    ) for k1 in data_content]

    #print(json.dumps(data_content, indent=4, sort_keys=True))


    insertTransactions = data_content


    return (insertTransactions, '2018-01-01T00:00:00Z')

#request = {}
#request['state'] = {'transactionsCursor': '2018-01-01T00:00:00Z'}
#request['secrets'] = 'secret'

#ref = lambda_handler(request, "context")
