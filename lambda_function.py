import json
import requests
import pprint
import os

def lambda_handler(request, context):


    print(request)

    # Fetch records using api calls
    (insertTransactions, newState, hasMore) = api_response(request['state'], request['secrets'])
    # Populate records in insert

    insert = {}
    insert['projects'] = insertTransactions

    schema = {}
    transactionsSchema = {}
    transactionsSchema['primary_key'] = ['id']
    schema['projects'] = transactionsSchema

    state = {}
    state =  newState

    response = {}
    # Add updated state to response
    response['state'] =  state
    # Add all the records to be inserted in response
    response['insert'] = insert
    # Add schema defintion in response
    response['schema'] = schema
    # Add hasMore flag
    response['hasMore'] = hasMore

    #print(json.dumps(response, indent=4, sort_keys=True))

    return response

def api_response(state, secrets):


    # CONFIG

    #if not request["state"]:
    #    request["state"]["projectsCursor"] = "2014-01-01"
    updated_since = "2014-01-01" #request["state"]["projectsCursor"]
    #print(state['projectsCursor'])
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

    # Do we see a page parameter? Otherwise 1
    if "page" not in state:
        state["page"] = 1

    # Do we see a updated_since parameter? Otherwise 2014
    if "cursor" not in state:
        state["cursor"] = "2014-01-01T00:00:00Z"

    if "temp_cursor" not in state:
        state["temp_cursor"] = state["cursor"]


    url = "https://api.harvestapp.com/v2/projects?page="+str(state["page"])+"&updated_since="+state["cursor"]
    print(url)
    response = requests.request("GET", url, headers=headers, data=payload)

    data  = response.json()
    data_content = data["projects"]
    data_next_page = data["next_page"]

    if data_content:
        max_updated_at = max(data_content, key=lambda ev: ev['updated_at'])["updated_at"]
    else:
        max_updated_at = state["cursor"]

    if data_next_page:
        state["page"] = data_next_page
        state["temp_cursor"] = max(max_updated_at,state["temp_cursor"])
        hasMore = "true"
    else:
        state["page"] = 1
        state["cursor"] = max(max_updated_at,state["temp_cursor"])
        hasMore = "false"

    #print(json.dumps(data, indent=4, sort_keys=True))

    data_content = [dict(
        id=k1["id"],
        name=k1["name"],
        updated_at=k1["updated_at"],
        created_at=k1["created_at"]
    ) for k1 in data_content]

    insertTransactions = data_content

    return (insertTransactions, state, hasMore)

if os.environ.get("AWS_EXECUTION_ENV") is None:
    request = {}
    request['state'] = {'cursor': '2022-02-08T20:56:27Z'}
    #request['state'] = {}
    request['secrets'] = 'secret'
    ref = lambda_handler(request, "context")
