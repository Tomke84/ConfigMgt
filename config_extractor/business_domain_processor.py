import json
from pathlib import Path
import config_library

def create_business_domain_files(data, dir_path, item, env, check):
    # Use the '/' operator for path manipulation
    dir_path_original = Path(dir_path) / f"original_{env}_{check}"
    output_file_original = dir_path_original / f"BD_{env}_{check}-{item}-original.json"

    dir_path_processed = Path(dir_path) / f"processed_{env}_{check}"
    output_file_processed = dir_path_processed / f"BD_{env}_{check}-{item}-processed.json"

    # sort lists/element
    if "creatableProcessTypes" in data:
        data["creatableProcessTypes"] = sorted(
            data["creatableProcessTypes"],
            key=lambda x: (int(x['displayOrder']), x['processType']['code'])
        )

    if "creatableDocumentTypes" in data:
        data["creatableDocumentTypes"] = sorted(
            data["creatableDocumentTypes"],
            key=lambda x: (int(x['displayOrder']), x['documentType']['code'])
        )

    if "creatableDocumentTypes" in data:
        data["creatableDocumentTypes"] = sorted(
            data["creatableDocumentTypes"],
            key=lambda x: (int(x['displayOrder']), x['documentType']['code'])
        )
    for creatableDocumentType in data["creatableDocumentTypes"]:
        creatableDocumentType["documentType"]["subtypes"] = sorted(
            creatableDocumentType["documentType"]["subtypes"],
            key=lambda x: x['code']
        )

        creatableDocumentType["documentType"]["documentSubtypes"] = sorted(
            creatableDocumentType["documentType"]["documentSubtypes"],
            key=lambda x: x['code']['code']
        )



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
