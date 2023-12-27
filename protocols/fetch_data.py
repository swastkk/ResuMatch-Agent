import json

import requests


def fetch_jobs():
    url = "https://api.adzuna.com/v1/api/jobs/in/search/1?app_id=91477adb&app_key=79c0cdb58e35ff78466ac6cb885743fa&what=UI%20engineer"
    response = requests.get(url)
    return response.json()


print(json.dumps(fetch_jobs(), indent=4))
