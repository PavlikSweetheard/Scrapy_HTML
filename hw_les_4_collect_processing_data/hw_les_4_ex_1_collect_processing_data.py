import requests
from lxml import html
from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
bd = client['News1207']
news = bd.news

url = 'https://lenta.ru/'

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}

responce = requests.get(url, headers=header)

dom = html.fromstring(responce.text)

if responce:
    news_blocks = dom.xpath("//section[contains(@class,'js-yellow-box')]//a/..") + dom.xpath(
        "//time[@class='g-time']/../..")

for new in news_blocks:
    news_dict = {}
    name = new.xpath(".//a/text()")[0]
    link = url + new.xpath(".//a/@href")[0]
    origin = url

    resp = requests.get(link, headers=header)
    dom = html.fromstring(resp.text)
    date = dom.xpath("//time[@pubdate]/@datetime")

    news_dict['name'] = name
    news_dict['link'] = link
    news_dict['date'] = date
    news_dict['origin'] = origin

    news.insert_one(news_dict)