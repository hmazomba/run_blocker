import requests
import json
# Replace 'YOUR_ACCESS_TOKEN' with your actual access token or private app access token
access_token = 'pat-na1-1de21061-6a6d-4a90-8e39-28a0735c0325'

# Replace 'YOUR_FORM_GUID' with the GUID of the form you want to retrieve submissions from
form_guid = 'c2c468a3-9304-4f02-a1d6-53985691bcff'

# Set the API endpoint URL
url = f'https://api.hubapi.com/form-integrations/v1/submissions/forms/{form_guid}'

headers = {
    'Authorization': f'Bearer {access_token}',
    'User-Agent': 'eCommerce Submissions'
}

params = {
    'limit': 30  # Optional: Adjust the limit parameter as needed
}

response = requests.get(url, headers=headers, params=params)

if response.status_code == 200:
    data = response.json()
    # Process the retrieved data as needed
    print(json.dumps(data, indent=4))  # Example: Print the response in JSON format
else:
    print(f'Request failed with status code {response.status_code}')

