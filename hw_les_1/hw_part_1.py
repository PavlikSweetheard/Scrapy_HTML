import requests
from pprint import pprint

main_link = 'https://api.github.com/'

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'}
user_name = 'Makarov595'

response = requests.get(f'{main_link}users/{user_name}/repos', headers=header)

if response.ok:
    data = response.json()
    # pprint(data)
    print("У пользователя", user_name, "есть следующие репозитории:")
    for line in data:
        print(line["name"])


with open('GitHubRepositories.json', 'w') as f:
    f.write(response.text)
