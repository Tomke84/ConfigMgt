import json

def sort_by_code(data):
    if "sublist" in data:
        data["sublist"] = sorted(data["sublist"], key=lambda x: x.get("code", ""))
        for item in data["sublist"]:
            sort_by_code(item)

# Example JSON data
json_data = {
    "sublist": [
        {
            "code": "DOCMNG-SUBTYPE-ANA",
            "sublist": [
                {
                    "code": "DOCMNG-SUBTYPE-ANA-CLASSMENT",
                    "sublist": []
                },
                {
                    "code": "DOCMNG-SUBTYPE-C_016-SC_068-TH_006",
                    "sublist": []
                },
                {
                    "code": "DOCMNG-SUBTYPE-CONT_DECISION-TBE",
                    "sublist": []
                }
            ]
        }
    ]
}

# Sorting the data
sort_by_code(json_data)

# Convert the result to JSON string for display (you can also work with the json_data object directly)
sorted_json = json.dumps(json_data, indent=4)
print(sorted_json)
