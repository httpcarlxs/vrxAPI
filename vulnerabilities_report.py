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
        jresponse = json.loads(response.text)
  
    except:
        print("something is wrong, will try again....")
        util.control_rate()
        get_endpoint_vulnerabilities(headers, urldashboard, fr0m, siz3, min_date, max_date, endpoint_hash)

    return jresponse