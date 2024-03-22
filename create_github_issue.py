import requests
import json
import os


# Read environment variables created by workflow
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_REPOSITORY = os.getenv('GITHUB_REPOSITORY')

# Read in JSON file produced by Snyk vulnerability scan and parse out required
# fields into a list of objects.
def parse_json_file(file_path: str) -> []:
    with open(file_path, 'r') as f:
        data = json.load(f)
        vulnerabilities = data.get("vulnerabilities", [])

        vuln_descriptions = []
        
        for vuln in vulnerabilities:
            line = {
                "id": vuln.get("id"),
                "title": vuln.get("title"),
                "package": vuln.get("packageName"),
                "version": vuln.get("version")
                }

            vuln_descriptions.append(line)

        return vuln_descriptions        

# Generate a new issue in GitHub containing a table of found vulnerabilities and
# their associated information.
def create_github_issue(vulns: []):
    if GITHUB_REPOSITORY == "" or GITHUB_REPOSITORY is None:
        raise ValueError("GITHUB_REPOSITORY is missing value")

    if GITHUB_TOKEN == "" or GITHUB_TOKEN is None:
        raise ValueError("GITHUB_TOKEN is missing value")
    
    title = "Critical Vulnerabilities"
    
    url = f'https://api.github.com/repos/{GITHUB_REPOSITORY}/issues'
    
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    body = format_vulns(vulns)
    
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
        print(f'Failed to create issue, Status Code: {response.status_code}')
        raise Exception(f'Client side HTTPS error, Status Code: {response.status_code}')

# Format list of vuln objects into an table using HTML
def format_vulns(vulns: []) -> str:
    if len(vulns) == 0:
        return "No Security Issues Found"
    
    html = "<table>"
    html += "<tr><th>ID</th><th>Title</th><th>Package</th><th>Package Version</th>"

    for vuln in vulns:
        html += "<tr><td>" + vuln["id"] + "</th><td>" + vuln["title"] + "</th><td>" + vuln["package"] + "</td><td>" + vuln["version"] + "</th>"

    html += "</table>"

    return html

    
if __name__ == '__main__':
    vulns = parse_json_file("critical_vuln_scan.json")
    create_github_issue(vulns)
    
    
