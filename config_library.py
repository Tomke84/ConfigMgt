import json
import requests


def extract_json(item_env, context, item):
    bearer_token = ""
    base_url = ""
    full_url = ""
    with open('config_list/connexion.json', 'r') as file:
        connexion = json.load(file)

    if item_env == "int":
        base_url = connexion['base_url_int']
        bearer_token = connexion['bearer_token_int']

    if item_env == "acc":
        base_url = connexion['base_url_acc']
        bearer_token = connexion['bearer_token_acc']

    if item_env == "prd":
        base_url = connexion['base_url_prd']
        bearer_token = connexion['bearer_token_prd']

    if context == 'PROCESS':
        base_url = base_url + "/processTypes"
        full_url = base_url + "/" + item

    if context == 'BUSINESS_DOMAIN':
        base_url = base_url + "/businessDomainTypes"
        full_url = base_url + "/" + item

    if context == 'TASK':
        base_url = base_url + "/taskTypes"
        full_url = base_url + "/" + item

    if context == 'BUSINESS_DATA':
        base_url = base_url + "/businessDataTypes"
        full_url = base_url + "/" + item

    if context == 'VALUE_LIST':
        base_url = base_url + "/businessDataTypes/valueList"
        full_url = base_url

    headers = {
        'Authorization': 'Bearer ' + bearer_token,
        'Content-Type': 'application/json',
        'Cache-Control': 'no-cache'
    }

    print(full_url)

    response = requests.get(full_url, headers=headers)
    # response.raise_for_status()  # This will an HTTPError
    response.encoding = 'utf-8'

    return response


def remove_key(data, key_to_remove):
    if isinstance(data, dict):
        # Remove the key if it exists in this dictionary
        data.pop(key_to_remove, None)
        # Recursively apply to each value
        for key in list(data.keys()):
            remove_key(data[key], key_to_remove)
    elif isinstance(data, list):
        # Apply the function to each item in the list
        for item in data:
            remove_key(item, key_to_remove)

def extract_accepted_values_codes(json_data):
    codes = []

    # Recursively search for 'acceptedValues' in the dictionary
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            if key == 'acceptedValues' and 'code' in value:
                codes.append(value['code'])
            else:
                codes.extend(extract_accepted_values_codes(value))
    elif isinstance(json_data, list):
        for item in json_data:
            codes.extend(extract_accepted_values_codes(item))

    return codes

def add_linked_business_data(json_data):
    listbdat = []

    # Recursively search for 'businessDataTypes' in the dictionary
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            if key == 'businessDataType' and 'code' in value:
                listbdat.append(value['code'])
            else:
                listbdat.extend(add_linked_business_data(value))
    elif isinstance(json_data, list):
        for item in json_data:
            listbdat.extend(add_linked_business_data(item))

    return listbdat

def add_linked_business_domain(json_data):
    listbdom = []

    # Recursively search for 'businessDomainTypes' in the dictionary
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            listbdom.extend(add_linked_business_domain(value))
    elif isinstance(json_data, list):
        for item in json_data:
            if 'activityCode' in item:
                listbdom.append(value['code'])
            else:
                listbdom.extend(add_linked_business_domain(item))

    return listbdom
