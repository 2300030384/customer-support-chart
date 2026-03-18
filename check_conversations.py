import requests
import json

resp = requests.get('http://localhost:8000/conversations')
print(f'Status code: {resp.status_code}')
print(f'Response text: {resp.text}')
if resp.status_code == 200:
    data = resp.json()
    print(f'Response data: {json.dumps(data, indent=2)}')
