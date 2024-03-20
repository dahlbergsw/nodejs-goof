import requests
import json
import os

 GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
 GITHUB_REPOSITORY = os.getenv('GITHUB_REPOSITORY')

def parse_sarif_file(sarif_file_path):
    pass

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
    except Exeption as e:
        print(e)

    if response.status_code < 300:
        print(f'Successfully created issue: {title}, Status Code: {response.status_code}')
    else:
        print(f'Failed to create issue: {title}, Status Code: {response.status_code}')
        
if __name__=='__main__':
    create_github_issue()
    
