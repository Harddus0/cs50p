import requests
import zipfile
import os
import shutil
from unidecode import unidecode
from datetime import datetime
from dateutil.relativedelta import relativedelta


def download_sinapi_table():
    """Download and extract SINAPI table"""

    # Get user state
    state = get_state()

    # Get 'desonerado'
    desonerado = get_desonerado()

    # Download the zip file
    month_count = 1
    while True:
        date = get_date(month_count)
        s = requests.Session()
        s.max_redirects = 100
        s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
        url = "https://www.caixa.gov.br/Downloads/sinapi-a-partir-jul-2009-" + state + "/SINAPI_ref_Insumos_Composicoes_" + state.upper() + "_" + date + "_" + desonerado + ".zip"

        try:
            r = s.get(url)
            if r.status_code == 200:
                with open('sinapi.zip', 'wb') as f:
                    f.write(r.content)  
            else:
                print(f"Failed to download file. HTTP Status Code: {r.status_code}")
                return

            extract_folder = "downloads"
            with zipfile.ZipFile('sinapi.zip', 'r') as zip_ref:
                zip_ref.extractall(extract_folder)
            break
        except zipfile.BadZipFile:
            print("Downloaded file is not a valid zip file. Retrying with an earlier month.")
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}. Retrying with an earlier month.")
        except Exception as e:
            print(f"An error occurred: {e}. Retrying with an earlier month.")

        # Try an earlier month
        month_count += 1
        
        if month_count > 2:
            print("Failed to download a valid zip file after multiple attempts.")

            return 
        
    # Extract the zip file into the "downloads" folder
    extract_folder = "downloads"
    with zipfile.ZipFile('sinapi.zip', 'r') as zip_ref:
        zip_ref.extractall(extract_folder)

    # Move the wanted file up one directory (from "downloads" to the root folder)
    wanted_file = "SINAPI_Custo_Ref_Composicoes_Sintetico_" + state + "_" + date + "_" + desonerado + ".xlsx"
    source_path = os.path.join(extract_folder, wanted_file)
    destination_path = os.path.join(os.getcwd(), wanted_file)  # Move to the current working directory

    if os.path.exists(source_path):
        shutil.move(source_path, destination_path)

    # Remove the entire "downloads" directory after moving the file
    if os.path.exists(extract_folder):
        shutil.rmtree(extract_folder)

    # return wanted_file name
    return wanted_file


def get_state():
    """Get desired state for SINAPI table"""

    states = [
    ["Acre", "AC"],
    ["Alagoas", "AL"],
    ["Amapa", "AP"],
    ["Amazonas", "AM"],
    ["Bahia", "BA"],
    ["Ceara", "CE"],
    ["Distrito Federal", "DF"],
    ["Espirito Santo", "ES"],
    ["Goias", "GO"],
    ["Maranhao", "MA"],
    ["Mato Grosso", "MT"],
    ["Mato Grosso do Sul", "MS"],
    ["Minas Gerais", "MG"],
    ["Para", "PA"],
    ["Paraiba", "PB"],
    ["Parana", "PR"],
    ["Pernambuco", "PE"],
    ["Piaui", "PI"],
    ["Rio de Janeiro", "RJ"],
    ["Rio Grande do Norte", "RN"],
    ["Rio Grande do Sul", "RS"],
    ["Rondonia", "RO"],
    ["Roraima", 'RR'],
    ["Santa Catarina", "SC"],
    ["Sao Paulo", "SP"],
    ["Sergipe", "SE"],
    ["Tocantins", "TO"]
    ]

    while True:
        user_state = unidecode(input("Enter your state: "))
        
        if len(user_state) == 2:
            user_state = user_state.upper()
        else:
            user_state = user_state.title()

        for state in states:
            if user_state in state:
                return state[1].lower()
                
        print("Not found, try again")


def get_desonerado():
    """Get 'desonerado' SINAPI attribute from user"""

    while True:
        desonerado = input("Desonerado? y or n: ").strip().lower()
        if desonerado in ["y", "yes"]:
            return "Desonerado"
        elif desonerado in ["n", "no"]:
            return "NaoDesonerado"
        else:
            print("Invalid answer")


def get_date(month_count=0):
    date = datetime.today() - relativedelta(months=month_count)
    return date.strftime('%Y%m')