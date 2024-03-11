import json
from pathlib import Path

import config_library
from config_library import sort_by_code



def create_business_data_files(data, dir_path, item, env):
    # Use the '/' operator for path manipulation
    dir_path_original = Path(dir_path) / f"original_{env}"
    output_file_original = dir_path_original / f"Data_{env}-{item}-original.json"

    dir_path_processed = Path(dir_path) / f"processed_{env}"
    output_file_clean = dir_path_processed / f"data_{env}-{item}.json"

    # Reading list_business_domain from a file
    data = sort_by_code(data)



    # save original file before deleting elements
    with open(output_file_original, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=5)

    print(f"Data extracted successfully and stored in {output_file_original}")

    # remove unwanted elements / keys
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
