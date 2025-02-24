import os, requests, json
from datetime import datetime, timedelta
import time
import re
import pandas as pd
import assets_report, vulnerabilities_report
from openpyxl.styles import Alignment, Font
import util


def gen_assets_report(headers, urldashboard, fr0m, siz3):
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
        assetVulnerabilitiesReport = vulnerabilities_report.parse_endpoint_vulnerabilities(jresponse)
        if len(assetVulnerabilitiesReport) > 0:
            vuln_report.extend(assetVulnerabilitiesReport)
    
    return vuln_report


if __name__ == "__main__":
    API_KEY, API_URL = util.load_configuration()
    HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
    }
    
    endpoints_map = gen_assets_report(HEADERS, API_URL, 0, 500)
    vuln_report = gen_vuln_report(HEADERS, API_URL, 0, 500, 30, endpoints_map)
    