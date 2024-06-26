import json
from pathlib import Path
import config_library
import config_processor

# Reading lists from files
with open('config_list/list_business_domains.txt', 'r') as file:
    list_business_domain = [line.strip() for line in file]

with open('config_list/list_processes.txt', 'r') as file:
    list_process = [line.strip() for line in file]

with open('config_list/list_tasks.txt', 'r') as file:
    list_tasks = [line.strip() for line in file]

with open('config_list/list_business_data.txt', 'r') as file:
    list_business_data = [line.strip() for line in file]

# Reading params from a file
with open('config_list/parameter.json', 'r') as file:
    params = json.load(file)


# create Directories
# Directory Path
dir_path = Path(params['base_directory'] + params['jira'] + "-" + params['date_str'])
dir_path.mkdir(parents=True, exist_ok=True)

# Directory per environment
list_env = params['env']
for env_item in list_env:
    dir_path_original = Path(params['base_directory'] + params['jira'] + "-" + params['date_str'] + "\\original_" + env_item + "_" + params['check'])
    dir_path_original.mkdir(parents=True, exist_ok=True)
    dir_path_processed = Path(params['base_directory'] + params['jira'] + "-" + params['date_str'] + "\\processed_" + env_item + "_" + params['check'])
    dir_path_processed.mkdir(parents=True, exist_ok=True)

print(f"Directory {dir_path} created successfully")

# execution
for env_item in list_env:
    for task_item in list_tasks:
        response = config_library.extract_json(env_item, "TASK", task_item)
        if response.status_code == 200:
            config_processor.config_processor(response.json(), dir_path, task_item, env_item, params['check'], "task")
            print(config_library.extract_accepted_values_codes(response.json()))
            list_business_data.extend(config_library.add_linked_business_data(response.json()))
            list_business_data = list(dict.fromkeys(list_business_data))
            print(list_business_data)
        if response.status_code != 200:
            print(f"Task Configuration : {task_item} not found {response.status_code}")

    for process_item in list_process:
        response = config_library.extract_json(env_item, "PROCESS", process_item)
        if response.status_code == 200:
            config_processor.config_processor(response.json(), dir_path, process_item, env_item, params['check'], "proc")
            print(config_library.extract_accepted_values_codes(response.json()))
            list_business_data.extend(config_library.add_linked_business_data(response.json()))
            list_business_data = list(dict.fromkeys(list_business_data))
            print(list_business_data)
#            list_business_domain.extend(config_library.add_linked_business_domain(response.json()))
#            list_business_domain = list(dict.fromkeys(list_business_domain))
#            print(list_business_domain)
        if response.status_code != 200:
            print(f"Process Configuration : {process_item} not found {response.status_code}")

    for business_domain_item in list_business_domain:
        response = config_library.extract_json(env_item, "BUSINESS_DOMAIN", business_domain_item)
        if response.status_code == 200:
            config_processor.config_processor(response.json(), dir_path, business_domain_item, env_item, params['check'], "bdom")
        if response.status_code != 200:
            print(f"Business Domain Configuration : {business_domain_item} not found {response.status_code}")

    for business_data_item in list_business_data:
        response = config_library.extract_json(env_item, "BUSINESS_DATA", business_data_item)
        if response.status_code == 200:
            config_processor.config_processor(response.json(), dir_path, business_data_item, env_item, params['check'], "bdat")
        if response.status_code != 200:
            print(f"Business Data Configuration : {business_data_item} not found {response.status_code}")

    # GET all valueLists
    #response_vl = config_library.extract_json(env_item, "BUSINESS_DATA_VALUE_LIST", "")
    #if response_vl.status_code == 200:
    #    config_processor.config_processor(response_vl.json(), dir_path, "all", env_item, params['check'], "list")
    #    data_business_data = response_vl.json()
    #    for business_data_item in list_business_data:
    #        for item in data_business_data["sublist"]:
    #            if item["code"] == business_data_item:
    #                config_processor.config_processor(item, dir_path, business_data_item, env_item, params['check'])
    #                break
    #if response_vl.status_code != 200:
    #    print(f"Business Data Value List  : not found {response.status_code}")

# save self-extracted items
#with open('config_list/list_business_data.txt', 'w') as filelbdat:
#    for business_data_item in list_business_data:
#        filelbdat.write(business_data_item+"\n")

