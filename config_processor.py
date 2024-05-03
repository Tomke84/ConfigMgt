import json
from pathlib import Path


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


def sort_sublists_by_code(obj):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == 'sublist' and isinstance(value, list) and all(
                    isinstance(item, dict) and 'code' in item for item in value):
                obj[key] = sorted(value, key=lambda x: (x['code']))
                sort_sublists_by_code(value)
            else:
                obj[key] = sort_sublists_by_code(value)
    elif isinstance(obj, list):
        obj = [sort_sublists_by_code(item) for item in obj]
    return obj

def sort_creatableprocesstypes_by_code(obj):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == 'creatableProcessTypes' and isinstance(value, list) and all(
                    isinstance(item, dict) and 'processType' in item for item in value):
                obj[key] = sorted(value, key=lambda x: (x['processType']['code']))
            else:
                obj[key] = sort_creatableprocesstypes_by_code(value)
    elif isinstance(obj, list):
        obj = [sort_creatableprocesstypes_by_code(item) for item in obj]
    return obj

def sort_creatabledocumenttypes_by_code(obj):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == 'creatableDocumentTypes' and isinstance(value, list) and all(
                    isinstance(item, dict) and 'documentType' in item for item in value):
                obj[key] = sorted(value, key=lambda x: (x['documentType']['code']))
                sort_creatabledocumenttypes_by_code(value)
            elif key == 'subtypes' and isinstance(value, list) and all(
                    isinstance(item, dict) and 'code' in item for item in value):
                obj[key] = sorted(value, key=lambda x: (x['code']))
                sort_creatabledocumenttypes_by_code(value)
            elif key == 'documentSubtypes' and isinstance(value, list) and all(
                    isinstance(item, dict) and 'code' in item for item in value):
                obj[key] = sorted(value, key=lambda x: (x['code']['code']))
                sort_creatabledocumenttypes_by_code(value)
            else:
                obj[key] = sort_creatabledocumenttypes_by_code(value)
    elif isinstance(obj, list):
        obj = [sort_creatabledocumenttypes_by_code(item) for item in obj]
    return obj


def config_processor(data, dir_path, item, env, check, type):
    dir_path_original = Path(dir_path) / f"original_{env}_{check}"
    output_file_original = dir_path_original / f"{type}_{env}_{check}-{item}-original.json"

    dir_path_processed = Path(dir_path) / f"processed_{env}_{check}"
    output_file_processed = dir_path_processed / f"{type}_{env}_{check}-{item}-processed.json"

    # save original file before deleting elements and sorting
    with open(output_file_original, 'w', encoding='utf-8') as f:
       json.dump(data, f, ensure_ascii=False, indent=5)

    print(f"Data extracted successfully and stored in {output_file_original}")


    # deleting elements in json
    remove_key(data, "id")
    remove_key(data, "creationDate")
    remove_key(data, "creationUser")
    remove_key(data, "lastUpdateDate")
    remove_key(data, "lastUpdateUser")
    remove_key(data, "closureSource")
    remove_key(data, "closureDate")
    remove_key(data, "creationSource")
    remove_key(data, "lastUpdateSource")
    remove_key(data, "usedBy")

    # sorting json
    if "acceptedValues" in data:
        data = sort_sublists_by_code(data)

    if "businessDataTypes" in data:
        data["businessDataTypes"]["items"] = sorted(
            data["businessDataTypes"]["items"],
            key=lambda x: (x['businessDataType']['code'])
        )
        data = sort_sublists_by_code(data)

    if "taskTypes" in data:
        data["taskTypes"] = sorted(
            data["taskTypes"],
            key=lambda x: (x['taskType']['code'])
        )

    if "businessDomainTypes" in data:
        data["businessDomainTypes"]["items"] = sorted(
            data["businessDomainTypes"]["items"],
            key=lambda x: (x['code'])
        )
        sort_creatableprocesstypes_by_code(data)
        sort_creatabledocumenttypes_by_code(data)

    if "activityCode" in data:
        sort_creatableprocesstypes_by_code(data)
        sort_creatabledocumenttypes_by_code(data)

    if "permissions" in data:
        data["permissions"]["items"] = sorted(
            data["permissions"]["items"],
            key=lambda x: (x['group']['nodeId'])
        )

    if "processTypes" in data:
        data["processTypes"]["items"] = sorted(
            data["processTypes"]["items"],
            key=lambda x: (x['code'])
        )
# zonder toevoeging van \":[{ in onderstaande regel wordt er een foutmelding gegeven als "subprocessesTypes": [] voorkomt in json
    if "subprocessesTypes" in data:
        data["subprocessesTypes"] = sorted(
            data["subprocessesTypes"],
            key=lambda x: (x["processType"]['code'])
        )

    # if "parentProcessTypes" in data:
    #    ...

    # save processed file
    with open(output_file_processed, 'w', encoding='utf-8') as f:
       json.dump(data, f, ensure_ascii=False, indent=3)

    print(f"Data extracted successfully and stored in {output_file_processed}")