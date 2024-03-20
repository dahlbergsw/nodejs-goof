import requests
import json
import os


GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_REPOSITORY = os.getenv('GITHUB_REPOSITORY')

def parse_json_file(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
        vulnerabilities = data["vulnerabilities"]

        vuln_descriptions = []
        
        for vuln in vulnerabilities:
            line = {
                "id": vuln["id"],
                "title": vuln["title"],
                "package": vuln["packageName"],
                "version": vuln["version"]
                }

            vuln_descriptions.append(line)

        return vuln_descriptions

def format_vulns(vulns):
    if len(vulns) == 0:
        return "No Security Issues Found"
    
    html = "<table>"
    html += "<tr><th>ID</th><th>Title</th><th>Package</th><th>Package Version</th>"

    for vuln in vulns:
        html += "<tr><td>" + vuln["id"] + "</th><td>" + vuln["title"] + "</th><td>" + vuln["package"] + "</td><td>" + vuln["version"] + "</th>"

    html += "</table>"

    return html
        
    
def create_github_issue(vulns: str):

    title = "Critical Vulnerabilities found for PR: "
    
    url = f'https://api.github.com/repos/{GITHUB_REPOSITORY}/issues'
    
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    body = format_vulns(vulns)
    print(body)
    
    payload = {
        'title': title,
        'body': body
    }
    
    data = json.dumps(payload)

    try:
        response = requests.post(url, data=data, headers=headers)
    except Exception as e:
        print(e)
        raise(e)

    if response.status_code < 300:
        print(f'Successfully created issue: {title}, Status Code: {response.status_code}')
    else:
        print(f'Failed to create issue: {title}, Status Code: {response.status_code}')
        raise Exception(f'Client side HTTPS error, Status Code: {response.status_code}')
        
if __name__ == '__main__':
    vulns = parse_json_file("critical_vuln_scan.json")
    create_github_issue(vulns)
    
