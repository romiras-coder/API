'''
1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев
для конкретного пользователя, сохранить JSON-вывод в файле *.json.
'''

import requests
import json

link = 'https://api.github.com/users/'
user = 'romiras-coder'
repos = 'repos'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
    'Accept': 'application/vnd.github.v3+json'}
response = requests.get(f'{link}{user}/{repos}', headers=headers)
data = response.json()
a = json.dumps(data, ensure_ascii=False, indent=4)
with open('DZ-1.json', 'wb') as f:
    f.write(a.encode('utf-8'))
