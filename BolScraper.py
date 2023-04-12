import requests
from bs4 import BeautifulSoup
import csv

url = 'https://www.bol.com/nl/nl/s/?searchtext=thermoshirt'
last_url = 'https://www.bol.com/nl/nl/s/?page=10&searchtext=thermoshirt&view=list'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }


listOfLinks = []

current_url = url
page = 1

while current_url != last_url:
    response = requests.get(current_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    product_tags = soup.find_all('li', {'class': 'product-item--row js_item_root'})

    for tag in product_tags:
        a_tag = tag.find('a', class_='product-title')
        href = a_tag.get('href')
        listOfLinks.append('https://www.bol.com' + href)
        #print('https://www.bol.com' + href)

    page += 1
    current_url = 'https://www.bol.com/nl/nl/s/?' + f'page={page}' + '&searchtext=thermoshirt&view=list'


with open('bol_thermoshirt.csv', 'w', encoding='utf-8', newline='') as csvfile:
    fieldnames = ['name', 'price', 'image', 'reviews']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for link in listOfLinks:
        response = requests.get(link, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        name = soup.find('h1', class_='page-heading').text
        image = soup.find('div', class_='container-item container-item__current js_current_item')
        img_tag = image.find('img', class_='js_selected_image')
        img_url = img_tag['src']

        price = soup.find('span', class_='promo-price').text
        price = price.strip().replace('\n', '')
        price = price.replace(' ', '')
        if '-' in price:
            price = price[:-1] + '.00'
        else :
            price = price[:-2] + '.' + price[-2:]

        #print(name, price, img_url)

        reviews_list = []
        alleReviews = soup.find_all('li', {'class': 'review js-review'})

        for review in alleReviews:
            review_body = review.find('div', {'class': 'review__body'})
            if review_body is not None:
                p_tags = review_body.find_all('p')
                if len(p_tags) == 2:
                    textInhoud = p_tags[1].text.strip()
                    reviews_list.append(textInhoud)
                    #print(textInhoud)
                elif len(p_tags) == 1:
                    textInhoud = p_tags[0].text.strip()
                    reviews_list.append(textInhoud)
                    #print(textInhoud)

        writer.writerow({'name': name, 'price': price, 'image': img_url, 'reviews': reviews_list})
