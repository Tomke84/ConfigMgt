import json
from pathlib import Path
import config_library


with open('config_list/list_processes.txt', 'r') as file:
    list_process = [line.strip() for line in file]

# Reading list_tasks from a file
with open('config_list/list_tasks.txt', 'r') as file:
    list_tasks = [line.strip() for line in file]

# Reading list_business_domain from a file
with open('config_list/list_business_domains.txt', 'r') as file:
    list_business_domain = [line.strip() for line in file]

with open('config_list/list_business_data.txt', 'r') as file:
    list_business_data = [line.strip() for line in file]

with open('config_list/parameter.json', 'r') as file:
    params = json.load(file)

# create Directories
# Directory Path
dir_path = Path(params['base_directory'] + params['jira'] + "-" + params['date_str'])


# Directory per environment
deploy_env = params['deploy_env']
deploy_env_source = params['deploy_env_source']
dir_path_processed = Path(params['base_directory'] + params['jira'] + "-" + params['date_str'] + "\\processed_" + deploy_env_source)

bearer_token = ""
base_url = ""
with open('config_list/connexion.json', 'r') as file:
    connexion = json.load(file)

if deploy_env == "int":
    base_url = connexion['base_url_int']
    bearer_token = connexion['bearer_token_int']

if deploy_env == "acc":
    base_url = connexion['base_url_acc']
    bearer_token = connexion['bearer_token_acc']

if deploy_env == "prd":
    base_url = connexion['base_url_prd']
    bearer_token = connexion['bearer_token_prd']

output_file_path = dir_path / 'deploy.http'
# Open a new file in write mode. Replace 'output.txt' with your desired file name.
with open(output_file_path, 'w') as output_file:

    output_file.write("# deploy from : " + deploy_env_source + " to : " + deploy_env + "\n")
    output_file.write("@baseUrl = " + base_url + "\n")
    output_file.write("@bearerToken = Bearer \n")
    output_file.write("\n")

# execution
    for item in list_process:
        file_path = dir_path_processed / f"Process_{deploy_env_source}-{item}.json"
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                response = config_library.extract_json(deploy_env, "PROCESS", item)
                if response.status_code == 200:
                    output_file.write("### PUT "+item+"\n")
                    output_file.write("PUT {{baseUrl}}/processTypes/"+item+" HTTP/1.1"+"\n")
                    output_file.write("content-type: application/json"+"\n")
                    output_file.write("Authorization: {{bearerToken}} "+"\n")
                    output_file.write("\n")
                    output_file.write("< "+str(file_path)+"\n")
                    output_file.write(" "+"\n")
                if response.status_code != 200:
                    output_file.write("### POST "+item+"\n")
                    output_file.write("POST {{baseUrl}}/processTypes/"+" HTTP/1.1"+"\n")
                    output_file.write("content-type: application/json"+"\n")
                    output_file.write("Authorization: {{bearerToken}} "+"\n")
                    output_file.write(" "+"\n")
                    output_file.write("< "+str(file_path)+"\n")
                    output_file.write(" "+"\n")
                pass
        except FileNotFoundError as e:
            print(f"File not found: {file_path} - {e}")
            continue


    for item in list_tasks:
        file_path = dir_path_processed / f"Task_{deploy_env_source}-{item}.json"
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                response = config_library.extract_json(deploy_env, "TASK", item)
                if response.status_code == 200:
                    output_file.write("### PUT "+item+"\n")
                    output_file.write("PUT {{baseUrl}}/taskTypes/"+item+" HTTP/1.1"+"\n")
                    output_file.write("content-type: application/json"+"\n")
                    output_file.write("Authorization: {{bearerToken}} "+"\n")
                    output_file.write(" "+"\n")
                    output_file.write("< "+str(file_path)+"\n")
                    output_file.write(" "+"\n")

                if response.status_code != 200:
                    output_file.write("### POST "+item+"\n")
                    output_file.write("POST {{baseUrl}}/taskTypes/"+" HTTP/1.1"+"\n")
                    output_file.write("content-type: application/json"+"\n")
                    output_file.write("Authorization: {{bearerToken}} "+"\n")
                    output_file.write(" "+"\n")
                    output_file.write("< " + str(file_path)+"\n")
                    output_file.write(" "+"\n")

                pass
        except FileNotFoundError as e:
            print(f"File not found: {file_path} - {e}")
            continue

    for item in list_business_data:
        file_path = dir_path_processed / f"data_{deploy_env_source}-{item}.json"
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                response = config_library.extract_json(deploy_env, "BUSINESS_DATA_VALUE_LIST", item)

                output_file.write("### PUT "+item+"\n")
                output_file.write("PATCH {{baseUrl}}/businessDataTypes/valueList/"+item+" HTTP/1.1"+"\n")
                output_file.write("content-type: application/json"+"\n")
                output_file.write("Authorization: {{bearerToken}} "+"\n")
                output_file.write(" "+"\n")
                output_file.write("< "+str(file_path)+"\n")
                output_file.write(" "+"\n")

                pass
        except FileNotFoundError as e:
            print(f"File not found: {file_path} - {e}")
            continue