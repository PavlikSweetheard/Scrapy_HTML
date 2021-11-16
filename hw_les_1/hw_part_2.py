import requests
from pprint import pprint

# https://api.vk.com/method/users.get   ?   user_id=210700286   &   v=5.52

header = {
    'User_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'}

method = 'account.getProfileInfo'

main_link = f'https://api.vk.com/method/{method}'

f = open('for_vk.txt', 'r')
token = f.readline()

params = {'v': '5.52', 'access_token': token}

response = requests.get(main_link, headers=header, params=params)

if response.ok:
    data = response.json()
    print(data)

with open ('DB_vk.json', 'w') as f:
    f.write(response.text)
    print('Ok')