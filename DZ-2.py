'''
2. Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа).
Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.
'''

import requests
import json

link = 'https://api.apify.com/v2/key-value-stores/'
Country = '1brJ0NLbQaJKPTWMO' # Россия
token = 'hxoeoMqaJcv93Euzv58kecnwE'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'Accept': '*/*'}

params = {'token': token}

response = requests.get(f'{link}{Country}/records/LATEST', params=params, headers=headers)

data = response.json()
a = json.dumps(data, ensure_ascii=False, indent=4)
with open('DZ-2.json', 'wb') as f:
    f.write(a.encode('utf-8'))
