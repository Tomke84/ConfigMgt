import json
from pathlib import Path

import config_library
from config_library import sort_sublists_by_order_and_code


def create_task_files(data, dir_path, item, env, check):
    # Use the '/' operator for path manipulation
    dir_path_original = Path(dir_path) / f"original_{env}_{check}"
    output_file_original = dir_path_original / f"Task_{env}_{check}-{item}-original.json"

    dir_path_processed = Path(dir_path) / f"processed_{env}_{check}"
    output_file_processed = dir_path_processed / f"Task_{env}_{check}-{item}-processed.json"

    # sort lists/element
    if "businessDataTypes" in data:
        # Sorting the processed items
        data["businessDataTypes"]["items"] = sorted(
            data["businessDataTypes"]["items"],
            key=lambda x: (x['businessDataType']['code'])
        )

    if "processTypes" in data:
        # Sorting the processed items
        data["processTypes"]["items"] = sorted(
            data["processTypes"]["items"],
            key=lambda x: (x['code'])
        )



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
    with open(output_file_processed, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=3)

    print(f"Data extracted successfully and stored in {output_file_processed}")
