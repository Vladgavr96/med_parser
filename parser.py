import requests
from bs4 import BeautifulSoup as bs
import csv
from sys import argv

url = 'https://novex.ru'
search_str = argv[1]


def get_item_urls(value):
    item_urls = []
    r = requests.get(url+value)
    soup = bs(r.text, "html.parser")
    data = soup.find_all('a', class_='link')
    for i in data:
        item_urls.append(url+str(i['href']))
    return item_urls

def get_item_description(url):
    r = requests.get(url)
    soup = bs(r.text, "html.parser")
    print(r.url)

    #название
    item_name = soup.find('h1').get_text()
    print(item_name)

    # марка
    item_info_list = soup.find('div', class_='vocabulary-list').find('span').find_all('div', class_='vocabulary-list__item')
    for i in item_info_list:
        if i.find('div', class_='vocabulary-list__property').get_text() == 'Торговая марка':
            trademark = i.find('div', class_='vocabulary-list__value').get_text()
            break


    #цена
    for element in soup.find_all('sup'):
        element.extract()
    price = soup.find_all('span', class_='price')[0].get_text()
    print(price)

    #место продажи
    place = soup.find('a', class_='header-delivery__link city header-link').get_text().strip()
    print(place)

    return item_name, trademark, place, price


with open('items.csv', 'w', newline='') as file:
    field_list = [["Название косметического средства", "Торговая марка", "Название точки продаж","Цена, руб"]]
    writer = csv.writer(file, quoting=csv.QUOTE_ALL, delimiter = ',')
    writer.writerows(field_list)

    urls = get_item_urls(f'/search/?search={search_str}]')
    for url in urls:
        data = get_item_description(url)
        writer.writerow(data)

