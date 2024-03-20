import requests
import json
import os

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_REPOSITORY = os.getenv('GITHUB_REPOSITORY')
VULN_SCAN_FILE = os.getenv('VULN_SCAN_FILE')

def parse_sarif_file(sarif_file_path):

    with open(sarif_file_path, 'r') as f:
        print(f.readlines())
    
    pass

def read_critical_vulnerabilities_from_scanner(page: int, per_page: int = 100):
    url = f"https://api.github.com/repos/{GITHUB_REPOSITORY}/code-scanning/alerts"

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    params = {
        "state": "critical",
        "page": page,
        "per_page": per_page
        }

    try:
        response = requests.get(url, params=params, headers=headers)
    except Exception as e:
        print(e)

    if response.status_code < 300:
        print(f'Successfully retrieved Code Scanning results, Status Code: {response.status_code}')
    else:
        print(f'Failed to retriev Code Scanning results, Status Code: {response.status_code}')        


def create_github_issue():
    # TODO: Remove
    title = "Test"
    body = "Test"

    # END_TODO
    
    url = f'https://api.github.com/repos/{GITHUB_REPOSITORY}/issues'
    print(url)

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    payload = {
        'title': title,
        'body': body
    }
    
    data = json.dumps(payload)

    try:
        response = requests.post(url, data=data, headers=headers)
    except Exception as e:
        print(e)

    if response.status_code < 300:
        print(f'Successfully created issue: {title}, Status Code: {response.status_code}')
    else:
        print(f'Failed to create issue: {title}, Status Code: {response.status_code}')
        
if __name__=='__main__':
    print("SARIF_FILE")
    parse_sarif_file(SARIF_FILE)
    # read_critical_vulnerabilities_from_scanner(page=1)
    # create_github_issue()
    
