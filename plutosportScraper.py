import requests
from bs4 import BeautifulSoup
import csv

url = 'https://www.plutosport.nl/catalogsearch/result/index?categorie=2&p=1&q=thermoshirt'
last_url = 'https://www.plutosport.nl/catalogsearch/result/index?categorie=2&p=5&q=thermoshirt'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }


listOfLinks = []

current_url = url
page = 1

while current_url != last_url:
    response = requests.get(current_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    product_tags = soup.find_all('li', {'class': 'item product product-item'})

    for tag in product_tags:
        a_tag = tag.find('a', class_='product-item-link')
        href = a_tag.get('href')
        listOfLinks.append(href + '#reviews')

    page += 1
    current_url = 'https://www.plutosport.nl/catalogsearch/result/index?categorie=2&p=' + f'{page}' + '&q=thermoshirt'


with open('plutosport_thermoshirt.csv', 'w', encoding='utf-8', newline='') as csvfile:
    fieldnames = ['name', 'price', 'image']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for link in listOfLinks:
        response = requests.get(link, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        name = soup.find('h1', class_='page-title').text
        price = soup.find('span', class_='price').text
        price = price[-5:]
        image = soup.find('div', class_='gallery-placeholder')
        img_tag = image.find('img', class_='gallery-placeholder__image')
        img_url = img_tag['src']

        print(name, price, img_url)

        writer.writerow({'name': name, 'price': price, 'image': img_url})
