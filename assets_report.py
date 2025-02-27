import util, requests, json

def get_endpoints(headers, urldashboard, fr0m, siz3):
    params = {
        'from': fr0m,
        'size': siz3,
    }

    try:
        response = requests.get(urldashboard + '/vicarius-external-data-api/endpoint/search', params=params, headers=headers)
        parsed = json.loads(response.text) 
        
    except:
        print("something is wrong, will try again....")
        
    endpoints_map = {}
    
    for i in parsed['serverResponseObject']:
        endpoint_updated_at = str((i['endpointUpdatedAt']))
        os_name = (i['endpointOperatingSystem']['operatingSystemName'])
        agent_version = (i['endpointVersion']['versionName'])
        
        endpoints_map[i['endpointHash']] = [('Hostname', i['endpointName']), ('Sistema Operacional', os_name), ('Agent Version', agent_version)]
        
    return endpoints_map


def get_endpoint_attributes(headers, urldashboard, fr0m, siz3, endpoints_map, endpoint_hash):
    params = {
        'from': fr0m,
        'size': siz3,
        'q': 'endpointAttributesEndpoint.endpointHash==' + endpoint_hash
    }

    try:
        response = requests.get(urldashboard + '/vicarius-external-data-api/endpointAttributes/search', params=params, headers=headers)
        parsed = json.loads(response.text) 
        if response.status_code == 429:
            print("O limite da API foi excedido...")
        
    except:
        print(f"Falha ao consultar atributos do endpoint: {endpoints_map[endpoint_hash][0][1]}.")
        return
    
    ipAddresses = ''

    for obj in parsed['serverResponseObject']:
        for line in obj:
            if line == 'endpointAttributesAttribute':
                if 'IP' in obj[line]['attributeAttributeSource']['attributeSourceName']:
                    ipAddresses += obj[line]['attributeExternalId'] + ', '
                    
    endpoints_map[endpoint_hash].append(('IP', ipAddresses[:-2]))
    
    
def get_endpoints_count(headers, urldashboard):
    params = {
        'from': 0,
        'size': 1,
        'sort': '+endpointId'
    }

    try:
        response = requests.get(urldashboard + '/vicarius-external-data-api/endpoint/search', params=params, headers=headers)
        json_response = json.loads(response.text)
        response_count = json_response['serverResponseCount']

    except:
        print("something is wrong, will try again....")
        print("response: ", response.text)
        return

    return response_count


def get_endpoint_patches(headers, urldashboard, fr0m, siz3, endpoints_map, endpoint_hash):
    params = {
        'from': fr0m,
        'size': siz3,
        'group': 'organizationEndpointExternalReferenceExternalReferencesPatches.patchName.raw;organizationEndpointExternalReferenceExternalReferencesPatches.patchDescription;organizationEndpointExternalReferenceExternalReferencesPatches.patchSensitivityLevel.sensitivityLevelName;organizationEndpointExternalReferenceExternalReferencesPatches.patchSensitivityLevel.sensitivityLevelRank;externalReferenceId;>;organizationEndpointExternalReferenceExternalReferencesPatches.patchId;externalReferenceSourceId;endpointId',
        'includeOriginalDoc': 'false',
        'newParser': 'true',
        'objectName': 'OrganizationEndpointExternalReferenceExternalReferences',
        'sort': 'OrganizationEndpointExternalReferenceExternalReferences.sensitivityLevelRank',
        'subAggregationLevel': '0',
        'sumLastSubAggregationBuckets': '0',
        'q': 'organizationEndpointExternalReferenceExternalReferencesEndpoint.endpointHash=in=('+endpoint_hash+')',
    }

    try:
        response = requests.get(urldashboard + '/vicarius-external-data-api/aggregation/searchGroup?', params=params, headers=headers)
        parsed = json.loads(response.text)
          
    except:
        print(f"Falha ao consultar patches do endpoint: {endpoints_map[endpoint_hash][0][1]}.")
        return

    str_endpoint_patches = ""
    str_endpoint_app_patches = ""
    str_endpoint_so_patches = ""
    i = j = k = 0
    for obj in parsed['serverResponseObject']:
        patch_descriptions = ''
        
        for agg in obj['aggregationAggregations']:
            if 'patchDescriptions' in agg['aggregationName']:
                patch_descriptions = agg['aggregationId']
                
        if any(keyword in patch_descriptions.lower() for keyword in ["kb"]):
            j += 1
            str_endpoint_so_patches += f"[{j}] " + patch_descriptions + "; \n"
        else:
            k += 1
            str_endpoint_app_patches += f"[{k}] " + patch_descriptions + "; \n"
        
        i += 1
        str_endpoint_patches += f"[{i}] " + patch_descriptions + "; \n"
    
    patches_count = len(parsed['serverResponseObject'])
    patches, so_patches, app_patches = str_endpoint_patches[:-3], str_endpoint_so_patches[:-3], str_endpoint_app_patches[:-3]
    
    endpoints_map[endpoint_hash].append(('Atualizações', patches_count))
    endpoints_map[endpoint_hash].append(('Atualizações do SO', so_patches))
    endpoints_map[endpoint_hash].append(('Atualizações de Apps', app_patches))


def get_endpoint_event_count(headers, urldashboard, fr0m, siz3, endpointHash, trycount=0):
    errors = []

    params = {
        'from': fr0m,
        'size': siz3,
        'q': 'organizationEndpointVulnerabilitiesEndpoint.endpointHash=in=('+endpointHash+')',
        'includeFields' : 'organizationEndpointVulnerabilitiesEndpoint.endpointId,organizationEndpointVulnerabilitiesEndpoint.endpointHash,organizationEndpointVulnerabilitiesVulnerability.vulnerabilityExternalReference.externalReferenceExternalId,organizationEndpointVulnerabilitiesVulnerability.vulnerabilityId,organizationEndpointVulnerabilitiesProduct.productName,organizationEndpointVulnerabilitiesOperatingSystem.operatingSystemName,organizationEndpointVulnerabilitiesVersion.versionName,organizationEndpointVulnerabilitiesSubVersion.subVersionName,organizationEndpointVulnerabilitiesProductRawEntry.productRawEntryName,organizationEndpointVulnerabilitiesVulnerability.vulnerabilitySensitivityLevel.sensitivityLevelName,organizationEndpointVulnerabilitiesVulnerability.vulnerabilitySummary,organizationEndpointVulnerabilitiesEndpoint.endpointName,organizationEndpointVulnerabilitiesPatch.patchId,organizationEndpointVulnerabilitiesPatch.patchName,organizationEndpointVulnerabilitiesPatch.patchReleaseDate,organizationEndpointVulnerabilitiesCreatedAt,organizationEndpointVulnerabilitiesUpdatedAt,organizationEndpointVulnerabilitiesVulnerability.vulnerabilityV3ExploitabilityLevel,organizationEndpointVulnerabilitiesVulnerability.vulnerabilityV3BaseScore'
    }
    
    if (trycount < 2):
        try:
            response = requests.get(urldashboard + '/vicarius-external-data-api/organizationEndpointVulnerabilities/search', params=params, headers=headers)
            if response.status_code == 429:
                print("O limite da API foi excedido... O programa parou e continuará em breve")
                errors.append("API Rate Limit")
                util.control_rate()
                return get_endpoint_event_count(headers, urldashboard, fr0m, siz3, endpointHash, trycount + 1)
            jsonresponse = json.loads(response.text)
            #print(json.dumps(jsonresponse,indent=4))
            
            try:
                responsecount = int(jsonresponse['serverResponseCount'])
            except:
                responsecount = 0
            try: 
                return responsecount, jsonresponse, errors
            except Exception as e:
                errors.append(f"Return Exception: {e},")
                jsonresponse = {}
                return -1, jsonresponse, errors
            
        except Exception as e:
                print(f'something is wrong, will try again- EndpointHash: {endpointHash}, ')
                errors.append(f"Exception: {e}, EndpointHash: {endpointHash}")
                util.control_rate()
                return get_endpoint_event_count(headers, urldashboard, fr0m, siz3, endpointHash, trycount + 1)
    else:
        return -1, None, errors
    
    
    