import util, requests, json

def get_endpoint_vulnerabilities(headers, urldashboard, fr0m, siz3, min_date, max_date, endpoint_hash):
    params = {
        'from': fr0m,
        'size': siz3,
        'q': f"organizationEndpointVulnerabilitiesCreatedAt>{min_date};"
             f"organizationEndpointVulnerabilitiesCreatedAt<{max_date};"
             f"organizationEndpointVulnerabilitiesEndpoint.endpointHash=in=({endpoint_hash})",
        'sort' : '-organizationEndpointVulnerabilitiesCreatedAt',
    }
    
    jresponse = []
    try:
        response = requests.get(urldashboard + '/vicarius-external-data-api/organizationEndpointVulnerabilities/search', params=params, headers=headers)
        if response.status_code == 429:
            print("O limite da API foi excedido... O programa parou e continuará em breve")
            util.control_rate()
            response = get_endpoint_vulnerabilities(headers, urldashboard, fr0m, siz3, min_date, max_date, endpoint_hash)
        jresponse = json.loads(response.text)
  
    except:
        print("something is wrong, will try again....")
        util.control_rate()
        get_endpoint_vulnerabilities(headers, urldashboard, fr0m, siz3, min_date, max_date, endpoint_hash)

    return jresponse


def parse_endpoint_vulnerabilities(jresponse):
    vuln_report = []
    vuln_set = set()
    index = 0

    for i in jresponse['serverResponseObject']:
        index +=1
        cve = i['organizationEndpointVulnerabilitiesVulnerability']['vulnerabilityExternalReference']['externalReferenceExternalId']
        vulid = str(i['organizationEndpointVulnerabilitiesVulnerability']['vulnerabilityId'])
        link = 'https://www.vicarius.io/vsociety/vulnerabilities/'+ vulid + '/' + cve
        
        try:
            product_name = i['organizationEndpointVulnerabilitiesProduct']['productName']
        except:
            try: 
                product_name = i['organizationEndpointVulnerabilitiesOperatingSystem']['operatingSystemName']
            except:
                product_name = ""
    
        product_raw_entry_name = i['organizationEndpointVulnerabilitiesProductRawEntry']['productRawEntryName']
        sensitivity_level_name = i['organizationEndpointVulnerabilitiesVulnerability']['vulnerabilitySensitivityLevel']['sensitivityLevelName']
        vulnerability_summary = i['organizationEndpointVulnerabilitiesVulnerability']['vulnerabilitySummary'] 
        
        asset = i['organizationEndpointVulnerabilitiesEndpoint']['endpointName']

        if i['organizationEndpointVulnerabilitiesPatch']['patchId'] > 0:
            patchid = str(i['organizationEndpointVulnerabilitiesPatch']['patchId'])
            patch_name = (i['organizationEndpointVulnerabilitiesPatch']['patchName'])
            #handle exception when patchReleaseDate not present
            try:
                patch_release_date = i['organizationEndpointVulnerabilitiesPatch']['patchReleaseDate']
                patch_release_date = str(util.convert_timestamp_to_datetime(patch_release_date).strftime("%d-%m-%Y"))
            except: 
                patch_release_date = "n\\a"
        else:
            patchid = "n\\a"
            patch_name = "n\\a"
            patch_release_date = "n\\a"

        try:
            create_at = i['organizationEndpointVulnerabilitiesCreatedAt']
            update_at = i['organizationEndpointVulnerabilitiesUpdatedAt']
            create_at = str(util.convert_timestamp_to_datetime(create_at).strftime("%d-%m-%Y"))
            update_at = str(util.convert_timestamp_to_datetime(update_at).strftime("%d-%m-%Y"))
        except:
            create_at = ""
            update_at = ""

        product_name = product_name.replace(',',"").replace(";","")
        product_raw_entry_name = str(product_raw_entry_name).replace(',',"").replace(";","")
        vulnerability_summary = str(vulnerability_summary).replace("\"","'")
        vulnerability_summary = vulnerability_summary.replace("\r","").replace("\n",">>")
        vulnerability_summary = vulnerability_summary.replace(",","").replace(";","")
        
        vulnerability_v3_exploitability_level = i['organizationEndpointVulnerabilitiesVulnerability']['vulnerabilityV3ExploitabilityLevel']
        vulnerability_v3_base_score = i['organizationEndpointVulnerabilitiesVulnerability']['vulnerabilityV3BaseScore']
        vuln = [('Hostname', asset), ('Product Name', product_name), ('CVE Severity', sensitivity_level_name), ('CVE', cve), ('Vulnerability ID', vulid), ('Patch ID', patchid), ('Patch Name', patch_name), ('Patch Release Date', patch_release_date), ('Vulnerability Creation Date', create_at), ('Last Updated', update_at), ('Link', link), ('Description', vulnerability_summary), ('V3 Base Score', vulnerability_v3_base_score), ('Exploitability Level', vulnerability_v3_exploitability_level)]
        if vuln not in vuln_report:
            vuln_report.append(vuln)

    return vuln_report
