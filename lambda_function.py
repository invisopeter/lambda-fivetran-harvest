import json
import requests
import pprint
import os
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

targets = {
  "projects": {
    "path": "projects",
    "primary_key": ['id'],
    "columns": ['id', 'name', 'updated_at', 'created_at'],
    "cursor": "2014-01-01T00:00:00Z",  # default
    "page": 1,  # default
    "insert": {}
  }
}


def lambda_handler(request, context):

    state = request['state']

    # Update with state

    # z = dict_merge(targets,state)

    for target in targets:
        targets[target]["cursor"] = state[target]["cursor"]
        targets[target]["page"] = state[target]["page"]
        #print(dump(targets[target]))
        #(state, insertTransactions, hasMore) = get_updates(targets[target], state)

        #prep respnse

    print(dump(targets))
    exit()

    # Fetch records using api calls
    (insertTransactions, newState, hasMore) = api_response(
        request['state'], request['secrets'])
    # Populate records in insert

    insert = {}
    insert['projects'] = insertTransactions

    schema = {}
    transactionsSchema = {}
    transactionsSchema['primary_key'] = ['id']
    schema['projects'] = transactionsSchema

    state = {}
    state = newState

    response = {}
    # Add updated state to response
    response['state'] = state
    # Add all the records to be inserted in response
    response['insert'] = insert
    # Add schema defintion in response
    response['schema'] = schema
    # Add hasMore flag
    response['hasMore'] = hasMore

    #print(json.dumps(response, indent=4, sort_keys=True))

    return response


def get_updates(target, state):

    return ({}, {}, {})


def api_response(state, secrets):

    headers = {
        'authorization': "Bearer " + config["harvest"]["token"],
        'content-type': "application/json",
        'accept': "application/json",
        'User-Agent': 'Harvest API Example',
        'Harvest-Account-ID': '586549'
    }

    payload = {}

    # Do we see a page parameter? Otherwise 1
    if "page" not in state:
        state["page"] = 1

    # Do we see a updated_since parameter? Otherwise 2014
    if "cursor" not in state:
        state["cursor"] = "2014-01-01T00:00:00Z"

    if "temp_cursor" not in state:
        state["temp_cursor"] = state["cursor"]

    url = config["harvest"]["endpoint"]+"/projects?page=" + \
        str(state["page"])+"&updated_since="+state["cursor"]
    print(url)
    response = requests.request("GET", url, headers=headers, data=payload)

    data = response.json()
    data_content = data["projects"]
    data_next_page = data["next_page"]

    if data_content:
        max_updated_at = max(data_content, key=lambda ev: ev['updated_at'])[
                             "updated_at"]
    else:
        max_updated_at = state["cursor"]

    if data_next_page:
        state["page"] = data_next_page
        state["temp_cursor"] = max(max_updated_at, state["temp_cursor"])
        hasMore = "true"
    else:
        state["page"] = 1
        state["cursor"] = max(max_updated_at, state["temp_cursor"])
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


def dump(response):
    return json.dumps(response, indent=4, sort_keys=True)


def dict_merge(dct, merge_dct):
    """ Recursive dict merge. Inspired by :meth:``dict.update()``, instead of
    updating only top-level keys, dict_merge recurses down into dicts nested
    to an arbitrary depth, updating keys. The ``merge_dct`` is merged into
    ``dct``.
    :param dct: dict onto which the merge is executed
    :param merge_dct: dct merged into dct
    :return: None
    """
    for k, v in merge_dct.iteritems():
        if (k in dct and isinstance(dct[k], dict)
                and isinstance(merge_dct[k], collections.Mapping)):
            dict_merge(dct[k], merge_dct[k])
        else:
            dct[k] = merge_dct[k]


if os.environ.get("AWS_EXECUTION_ENV") is None:
    request = {}
    request['state'] = {"projects": {
        'cursor': '2022-02-08T20:56:27Z', 'page': 4}}
    #request['state'] = {}
    #request['secrets'] = 'secret'
    ref = lambda_handler(request, "context")
