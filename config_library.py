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

    if context == 'TASK':
        base_url = base_url + "/taskTypes"
        full_url = base_url + "/" + item

    if context == 'PROCESS':
        base_url = base_url + "/processTypes"
        full_url = base_url + "/" + item
    if context == 'BUSINESS_DOMAIN':
        base_url = base_url + "/businessDomainTypes"
        full_url = base_url + "/" + item

    if context == 'BUSINESS_DATA_VALUE_LIST':
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
def clear_key(data, key_to_clear):
    if isinstance(data, dict):
        # Clear the key's content if it exists in this dictionary
        if key_to_clear in data:
            data[key_to_clear] = None  # or any other default value you prefer
        # Recursively apply to each value
        for key in data:
            clear_key(data[key], key_to_clear)
    elif isinstance(data, list):
        # Apply the function to each item in the list
        for item in data:
            clear_key(item, key_to_clear)


def replace_chars_in_dict(d, old_chars, new_chars):
    if isinstance(d, dict):
        for key, value in d.items():
            d[key] = replace_chars_in_dict(value, old_chars, new_chars)
    elif isinstance(d, list):
        return [replace_chars_in_dict(item, old_chars, new_chars) for item in d]
    elif isinstance(d, str):
        return d.replace(old_chars, new_chars)
    return d


def sort_sublists_by_order_and_code(obj):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == 'sublist' and isinstance(value, list) and all(
                    isinstance(item, dict) and 'order' in item and 'code' in item for item in value):
                obj[key] = sorted(value, key=lambda x: (int(x['order']), x['code']))
            else:
                obj[key] = sort_sublists_by_order_and_code(value)
    elif isinstance(obj, list):
        obj = [sort_sublists_by_order_and_code(item) for item in obj]
    return obj


def sort_sublists_by_code(obj):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == 'sublist' and isinstance(value, list) and all(
                    isinstance(item, dict) and 'code' in item for item in value):
                obj[key] = sorted(value, key=lambda x: (x['code']))
            else:
                obj[key] = sort_sublists_by_code(value)
    elif isinstance(obj, list):
        obj = [sort_sublists_by_code(item) for item in obj]
    return obj


def sort_by_code(data):
    if "sublist" in data:
        data["sublist"] = sorted(data["sublist"], key=lambda x: x.get("code", ""))
        for item in data["sublist"]:
            sort_by_code(item)
    return data
