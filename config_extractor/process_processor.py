import json
from pathlib import Path

import config_library
from config_library import sort_sublists_by_order_and_code


def create_process_files(data, dir_path, item, env):
    # Use the '/' operator for path manipulation
    dir_path_original = Path(dir_path) / f"original_{env}"
    output_file_original = dir_path_original / f"Process_{env}-{item}-original.json"

    dir_path_processed = Path(dir_path) / f"processed_{env}"
    output_file_clean = dir_path_processed / f"Process_{env}-{item}.json"

    # sort lists/element

    # businessDataTypes
    if "businessDataTypes" in data:
        # Sorting the processed items
        data["businessDataTypes"]["items"] = sorted(
            data["businessDataTypes"]["items"],
            key=lambda x: (int(x['order']), x['businessDataType']['code'])
        )

    if "taskTypes" in data and data["taskTypes"]:
        data["taskTypes"] = sorted(data["taskTypes"], key=lambda x: (int(x['displayOrder']), x['taskType']['code']))

    if "businessDomainTypes" in data:
        # Sorting businessDomainTypes items by their code
        data["businessDomainTypes"]["items"] = sorted(
            data["businessDomainTypes"]["items"],
            key=lambda x: x['code']
        )

        for item in data["businessDomainTypes"]["items"]:
            # Sorting creatableProcessTypes by displayOrder and processType code
            if "creatableProcessTypes" in item:
                item["creatableProcessTypes"] = sorted(
                    item["creatableProcessTypes"],
                    key=lambda x: (int(x['displayOrder']), x['processType']['code'])
                )

            # Sorting creatableDocumentTypes by displayOrder and documentType code
            if "creatableDocumentTypes" in item:
                item["creatableDocumentTypes"] = sorted(
                    item["creatableDocumentTypes"],
                    key=lambda x: (int(x['displayOrder']), x['documentType']['code'])
                )

    if "milestoneTypes" in data and "items" in data["milestoneTypes"]:
        data["milestoneTypes"]["items"] = sorted(
            data["milestoneTypes"]["items"],
            key=lambda x: x["code"]
        )

    if "permissions" in data and "items" in data["permissions"]:
        data["permissions"]["items"] = sorted(
            data["permissions"]["items"],
            key=lambda x: x["group"]["id"]
        )
    #sort all sublist in the json
    data = sort_sublists_by_order_and_code(data)

    # save original file before deleting elements
    with open(output_file_original, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=5)

    print(f"Data extracted successfully and stored in {output_file_original}")

    # remove unwanted elements / keys
    config_library.remove_key(data, "id")
    config_library.remove_key(data, "creationDate")
    config_library.remove_key(data, "creationUser")
    config_library.remove_key(data, "lastUpdateDate")
    config_library.remove_key(data, "lastUpdateUser")
    config_library.remove_key(data, "closureSource")
    config_library.remove_key(data, "closureDate")
    config_library.remove_key(data, "creationSource")
    config_library.remove_key(data, "lastUpdateSource")

    # save processed file after deleting elements
    with open(output_file_clean, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=3)

    print(f"Data extracted successfully and stored in {output_file_clean}")
