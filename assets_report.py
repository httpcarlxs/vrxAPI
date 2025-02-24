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
        endpointUpdatedAt = str((i['endpointUpdatedAt']))
        operatingSystemName = (i['endpointOperatingSystem']['operatingSystemName'])
        agentVersion = (i['endpointVersion']['versionName'])
        
        endpoints_map[i['endpointHash']] = [('Hostname', i['endpointName']), ('Sistema Operacional', operatingSystemName), ('Agent Version', agentVersion)]
        
    
    return endpoints_map
