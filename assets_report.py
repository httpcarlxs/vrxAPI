import os, requests, json

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
        
    except:
        print(f"Falha ao consultar atributos do endpoint: {endpoints_map[endpoint_hash][0][1]}.")
    
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

    return response_count
