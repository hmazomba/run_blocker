import requests
import json

access_token = 'pat-na1-1de21061-6a6d-4a90-8e39-28a0735c0325'
form_guid = 'c2c468a3-9304-4f02-a1d6-53985691bcff'
url = f'https://api.hubapi.com/form-integrations/v1/submissions/forms/{form_guid}'

headers = {
    'Authorization': f'Bearer {access_token}',
    'User-Agent': 'eCommerce Submissions'
}

params = {
    'limit': 30
}

response = requests.get(url, headers=headers, params=params)

if response.status_code == 200:
    data = response.json()
    print(json.dumps(data, indent=4))
else:
    error_message = response.json().get('message')
    print(f'Request failed with status code {response.status_code}: {error_message}')

