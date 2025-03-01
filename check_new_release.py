


import requests
import json
import pathlib
from google import genai


# update ur key lol
GITHUB_API_KEY = "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"
client = genai.Client(api_key="AIzaSyAUq_ZTk_bm0k9dmGLZERlAMVCmrO7qISc")


def filter_download_link(response):
    pathlib.Path('a11.txt').write_text(response.text)
    
    my_file = client.files.upload(file='a11.txt')
    response = client.models.generate_content(
        model='gemini-2.0-flash', 
        contents=[
            'In this file, if there is a .deb file, give it first priority and return me the download link. Howveer if it doesnt exist, return me a tar.gz. file and it must support x86/amd. always use 64 bits. Return ur answer to me in 1 word (which is the link). If it dosent satisfy anything return nil.' , 
            my_file
        ]
    )
    download_link = response.text
    return download_link.strip



with open('apps.json', 'r') as file:
    app_data = json.load(file)

for value in app_data.values():
    owner = value.get('owner', 'No owner available')
    repo = value.get('repo', 'No repo available')
    

    url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
    headers = {"Authorization": f"token {GITHUB_API_KEY}"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        latest_version = response.json()["tag_name"]
        if latest_version != value['version']:
            value['version'] = latest_version
            download_link = filter_download_link(response)
            value["download"] = download_link
    else:
        print(f"Failed to fetch app_data: {response.status_code}, {response.json()}")

with open('apps.json', 'w') as file:
    json.dump(app_data, file, indent=4)
