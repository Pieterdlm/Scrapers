import math
import requests
from bs4 import BeautifulSoup
import csv

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
service = Service("C:\ChromeDriver\chromedriver.exe")
driver = webdriver.Chrome(service=service, options=chrome_options)


base_url = 'https://www.decathlon.nl/browse/c0-sportkleding/c1-thermokleding/c2-thermoshirt/_/N-1lrof8z'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

lijstvanlinks = []
lijstVanProductPaginas = []
lijstvanFotoLinks = []
lijstVanProductNames = []
lijstVanProductPrices = []
arrayListVanReviews = []


with open('decathlon_thermoshirt.csv', 'w', encoding='utf-8', newline='') as csvfile:
    fieldnames = ['Naam', 'Prijs', 'Foto', 'Review']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    driver.get(base_url)
    time.sleep(1)  # add a delay to allow the page to load completely

    amount_of_products = driver.find_element(By.XPATH, "//span[@class='vtmn-tag vtmn-tag_size--medium vtmn-tag_variant--accent tag-variant--primary']")
    amount_of_pages = int(amount_of_products.text)
    pages_to_scrape = math.floor(amount_of_pages / 32)
    print(amount_of_products.text)
    print(pages_to_scrape)
    teller = 1

    for page in range(6):
        print(teller)
        teller += 1
        url = base_url + f'?from={page * 32}&size=32'
        driver.get(url)
        time.sleep(1)  # add a delay to allow the page to load completely
        product_tags = driver.find_elements(By.XPATH, "//div[@class='vtmn-flex vtmn-flex-col vtmn-items-center vtmn-relative vtmn-overflow-hidden vtmn-text-center vtmn-z-0 dpb-holder svelte-2ckipo']")

        for tag in product_tags:
            productPage = tag.find_element(By.XPATH, ".//a").get_attribute("href")
            lijstVanProductPaginas.append(productPage)
            reviewLink = productPage.replace('/p/', '/r/')
            print(reviewLink)
            lijstvanlinks.append(reviewLink)

        for fotolink in lijstVanProductPaginas:
            driver.get(fotolink)
            prijs = driver.find_element(By.XPATH, '//*[@id="app"]/main/article/div[3]/div[1]/div')
            #time.sleep(1)
            lijstVanProductPrices.append(prijs.text)
            naam = driver.find_element(By.XPATH, '//*[@id="app"]/main/article/div[3]/h1')
            lijstVanProductNames.append(naam.text)
            productPicture = driver.find_element(By.XPATH, "//*[@id='app']/main/article/div[2]/div[2]/div[2]/div/div/section[2]/img").get_attribute("src")
            #print(productPicture)
            lijstvanFotoLinks.append(productPicture)




    for link in lijstvanlinks:
        driver.get(link)
        time.sleep(1)  # add a delay to allow the page to load completely
        lijstVanReviews = []

        try:
            for number in range(1, 3):
                xpath_expression = f'//*[@id="reviews-floor"]/div/section/article[{number}]/p'
                product_reviews = driver.find_element(By.XPATH, xpath_expression)
                review_text = product_reviews.text
                print(review_text)
                lijstVanReviews.append(review_text)

        except NoSuchElementException:
            print("No more reviews to scrape")

        arrayListVanReviews.append(lijstVanReviews)


    for naam, prijs, fotolink, list in zip(lijstVanProductNames, lijstVanProductPrices, lijstvanFotoLinks, arrayListVanReviews):
        writer.writerow({'Naam': naam, 'Prijs': prijs, 'Foto': fotolink, 'Review': list})



driver.quit()