from datetime import datetime, timedelta
import pandas as pd
import assets_report, vulnerabilities_report
import util
import requests, json
from io import BytesIO


def gen_assets_report(headers, urldashboard, fr0m, siz3):
    util.control_rate()
    endpoints_map = assets_report.get_endpoints(headers, urldashboard, fr0m, siz3)
    
    for key in endpoints_map:
        util.control_rate()
        assets_report.get_endpoint_attributes(headers, urldashboard, fr0m, siz3, endpoints_map, key)
        
        util.control_rate()
        assets_report.get_endpoint_patches(headers, urldashboard, fr0m, siz3, endpoints_map, key)
        
        util.control_rate()
        events_count, response, errors = assets_report.get_endpoint_event_count(headers, urldashboard, fr0m, siz3, key)
        if response:
            endpoints_map[key].append(('CVE\'s', events_count))
        else:
            for error in errors:
                print(error)
    
    return endpoints_map


def gen_vuln_report(headers, urldashboard, fr0m, siz3, timestamp, endpoints_map):
    vuln_report = []
    
    date_now = str(int(float(datetime.now().timestamp() * 1000)))
    min_date = str(int(float((datetime.now() - timedelta(days=timestamp)).timestamp() * 1000)))
    
    for key in endpoints_map:
        jresponse = vulnerabilities_report.get_endpoint_vulnerabilities(headers, urldashboard, fr0m, siz3, min_date, date_now, key)
        print(json.dumps(jresponse,indent=4))
        assetVulnerabilitiesReport = vulnerabilities_report.parse_endpoint_vulnerabilities(jresponse)
        if len(assetVulnerabilitiesReport) > 0:
            vuln_report.extend(assetVulnerabilitiesReport)
    
    return vuln_report


def gen_excel_file(file_name, df_hosts, df_vuln, prefixes, column_widths):
    with pd.ExcelWriter(f"report/{file_name}", engine="openpyxl") as writer:
        util.split_and_write(writer, "Hosts", df_hosts, prefixes, column_widths)
        util.split_and_write(writer, "Vulnerabilities", df_vuln, prefixes, column_widths)

    print(f"Arquivo salvo como {file_name}")


if __name__ == "__main__":
    API_KEY, API_URL, DESCRIPTION_FILE_URL, DESCRIPTION_FILE_PATH = util.load_configuration()
    print(DESCRIPTION_FILE_URL, DESCRIPTION_FILE_PATH)
    
    HEADERS = {
        'Accept': 'application/json',
        'Vicarius-Token': API_KEY,
    }
    
    COLUMN_WIDTHS = {
        "Hosts": {
            'Hostname': 17, 'IP': 17, 
            'Sistema Operacional': 15, 
            'Agent Version': 11, 'CVE\'s': 11, 'Atualizações': 12, 
            'Atualizações do SO': 50, 'Atualizações de Apps': 50
        },
        "Vulnerabilities": {
            'Hostname': 17, 
            'Product Name': 15, 'Patch Name': 22, 
            'Patch ID': 10, 'CVE': 15, 'CVE Severity': 10, 'V3 Base Score': 10, 'Exploitability Level': 12, 
            'Vulnerability ID': 12, 'Patch Release Date': 12, 'Vulnerability Creation Date': 15, 
            'Last Updated': 12,  
            'Link': 40, 
            'Description': 70
        }
    }
    
    print('Gerando relatório de hosts...')
    endpoints_map = gen_assets_report(HEADERS, API_URL, 0, 500)
    
    print('Gerando relatório de vulnerabilidades...')
    vuln_report = gen_vuln_report(HEADERS, API_URL, 0, 500, 30, endpoints_map)
    
    assets_data = [{key: value for key, value in asset} for asset in endpoints_map.values()]
    df_hosts = pd.DataFrame(assets_data)
    
    vuln_data = [{key: value for key, value in vuln} for vuln in vuln_report]
    df_vuln = pd.DataFrame(vuln_data)
    
    response = requests.get(DESCRIPTION_FILE_URL)
    df_description = None
    if response.status_code == 200:
#        df_description = pd.read_excel(BytesIO(response.content), usecols=[["Name", "Notes"]])
        df_description = pd.read_excel(BytesIO(response.content), usecols=["Column1", "Column9"])
        print("Arquivo carregado com sucesso.")
    else:
        print(f"Erro ao baixar o arquivo: {response.status_code}")
        
    if df_description is None:
        try:
            df_description = pd.read_excel(DESCRIPTION_FILE_PATH, usecols=["Column1", "Column9"])            
        except:
            print("Erro ao carregar o arquivo... relatório de hosts não terá suas respectivas descrições.")
    
    if df_description is not None and not df_description.empty:
        df_description.rename(columns={"Column1": "Hostname", "Column9": "Descrição"}, inplace=True)
        df_hosts = df_hosts.merge(df_description, on="Hostname", how="left")
        df_hosts.method({"Descrição": "Sem descrição"}, inplace=True)
        
    prefixes = ["SP", "RJ", "RS"]
    gen_excel_file("vrx_reports.xlsx", df_hosts, df_vuln, prefixes, COLUMN_WIDTHS)