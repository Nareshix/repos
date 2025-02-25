from check_releases import check_releases
import json
GITHUB_TOKEN = "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"


with open('apps.json') as f:
    apps = json.load(f)
    for app in apps.keys(): 
        check_releases(app,GITHUB_TOKEN)

