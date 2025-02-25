import requests
import re

def check_releases(APP, GITHUB_TOKEN):
    url = f"https://api.github.com/repos/{APP}/releases/latest"
    headers = {"User-Agent": "Python"}
    
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        release = response.json()

        print(f"🟢 Latest stable release for {APP}")
        print(f"🔖 Version: {release['tag_name']}\n")
        
        print("📥 Download links:")
        found_assets = []
        patterns = [
            (r'x86[_-]?64', 'x86_64'),
            (r'x64', 'x64'),
            (r'amd64', 'amd64')
        ]

        for asset in release.get('assets', []):
            name = asset['name'].lower()
            if 'linux' in name and name.endswith('.tar.gz'):
                for pattern, arch in patterns:
                    if re.search(pattern, name):
                        found_assets.append((arch, asset))
                        break  # Stop checking other patterns

        # Sort by priority and remove duplicates
        priority_order = {'x86_64': 0, 'x64': 1, 'amd64': 2}
        seen = set()
        for arch, asset in sorted(found_assets, key=lambda x: priority_order[x[0]]):
            if asset['id'] not in seen:
                seen.add(asset['id'])
                print(f"  - {asset['name']} ({arch})")
                print(f"    {asset['browser_download_url']}")

        if not found_assets:
            print("    No Linux x86_64/x64/amd64 .tar.gz assets found")

    except requests.exceptions.HTTPError as e:
        print(f"🔴 HTTP Error: {e}")
        if e.response.status_code == 404:
            print("This repository might not exist or have any releases")
    except Exception as e:
        print(f"🔴 Unexpected error: {str(e)}")
    print('')