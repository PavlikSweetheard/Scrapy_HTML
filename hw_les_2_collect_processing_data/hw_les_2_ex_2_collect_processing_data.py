"""
Вариант 2
Необходимо собрать информацию по продуктам питания с сайта: Список протестированных продуктов на сайте Росконтроль.рф
Приложение должно анализировать несколько страниц сайта (вводим через input или аргументы).
Получившийся список должен содержать:

Наименование продукта.
Все параметры (Безопасность, Натуральность, Пищевая ценность, Качество) Не забываем преобразовать к цифрам
Общую оценку
Сайт, откуда получена информация.
Общий результат можно вывести с помощью dataFrame через Pandas. Сохраните в json либо csv.
"""
import requests
from pprint import pprint
from bs4 import BeautifulSoup



def sbor_info(dom_structure, max_page, link_cat):
    try:
        pages = dom_structure.find('div', {'class': 'page-pagination'}).findChildren()
        for page in pages:
            try:
                if int(page['href'][-1]) > max_page:
                    max_page = int(page['href'][-1])
            except:
                None
    except:
        None

    for i in range(max_page):

        response_2 = requests.get(link_cat, params=params, headers=headers)
        dom_structure = BeautifulSoup(response_2.text, 'html.parser')

        products = dom_structure.find_all('div', {
            'class': 'wrap-product-catalog__item grid-padding grid-column-4 grid-column-large-6 grid-column-middle-12 grid-column-small-12 grid-left js-product__item'})

        for product in products:

            product_dict = {}
            name = product.find('div', {'class': 'product__item-link'}).getText()

            try:
                safety = int(product.find('div', text='Безопасность').
                             next_sibling.next_sibling('i')[0]['data-width'])
            except:
                safety = None
            try:
                nutritional_value = int(product.find('div', text='Пищевая ценность').
                                        next_sibling.next_sibling('i')[0]['data-width'])
            except:
                nutritional_value = None
            try:
                naturalness = int(product.find('div', text='Натуральность').
                                  next_sibling.next_sibling('i')[0]['data-width'])
            except:
                naturalness = None
            try:
                quality = int(product.find('div', text='Качество').
                              next_sibling.next_sibling('i')[0]['data-width'])
            except:
                quality = None
            try:
                overal_assessment = int(product.find('div', {'class': 'rate'}).getText())
            except:
                overal_assessment = None

            link = url + product.find('a', {
                'class': 'block-product-catalog__item js-activate-rate util-hover-shadow clear'})['href']

            product_dict['name'] = name
            product_dict['overal_assessment'] = overal_assessment
            product_dict['safety'] = safety
            product_dict['nutritional_value'] = nutritional_value
            product_dict['naturalness'] = naturalness
            product_dict['quality'] = quality
            product_dict['link'] = link

            category_poducts_list.append(product_dict)

        params['page'] = int(params['page']) + 1
    return (category_poducts_list)


# https://roscontrol.com/category/produkti/yaytsa/?page=2

url = 'https://roscontrol.com'
#
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}

response = requests.get(url + '/category/produkti/', headers=headers)

dom_structure = BeautifulSoup(response.text, 'html.parser')

category_poducts = dom_structure.find_all('div', {
    'class': 'grid-padding grid-column-3 grid-column-large-6 grid-flex-mobile grid-column-middle-6 grid-column-small-12 grid-left'})

category_poducts_list = []


for category in category_poducts:
    category_info = {}
    link_cat = url + category.find('a')['href']

    params = {'page': '1'}

    response_2 = requests.get(link_cat, params=params, headers=headers)
    dom_structure = BeautifulSoup(response_2.text, 'html.parser')

    type_products = dom_structure.find_all('div', {
        'class': 'grid-padding grid-column-3 grid-column-large-6 grid-flex-mobile grid-column-middle-6 grid-column-small-12 grid-left'})

    print(len(type_products))

    if len(type_products) == 0:
        max_page = 1
        sbor_info(dom_structure, max_page, link_cat)
    elif len(type_products) > 0:
        for type_product in type_products:
            link_type_prod = url + type_product.find('a')['href']
            response_3 = requests.get(link_type_prod, params=params, headers=headers)
            dom_structure = BeautifulSoup(response_3.text, 'html.parser')
            max_page = 1
            sbor_info(dom_structure, max_page, link_type_prod)
        pprint(category_poducts_list)

pprint(category_poducts_list)