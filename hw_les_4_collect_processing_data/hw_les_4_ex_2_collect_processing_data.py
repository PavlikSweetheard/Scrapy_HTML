import requests
from lxml import html
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

client = MongoClient('127.0.0.1', 27017)
bd = client['News1207']
news = bd.news

url = 'https://news.mail.ru/'

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}

responce = requests.get(url, headers=header)

dom = html.fromstring(responce.text)

if responce:
    news_blocks_links = dom.xpath("//td//a/@href")

for link in news_blocks_links:
    news_dict = {}
    resp = requests.get(link, headers=header)
    dom = html.fromstring(resp.text)

    name = dom.xpath("//h1/text()")[0]
    date = dom.xpath("//span[@datetime]/@datetime")[0]
    origin = dom.xpath("//span[contains(text(), 'источник')]/../a/@href")[0]

    news_dict['name'] = name
    news_dict['link'] = link
    news_dict['date'] = date
    news_dict['origin'] = origin

    try:
        news.insert_one(news_dict)
    except DuplicateKeyError:
        pass
