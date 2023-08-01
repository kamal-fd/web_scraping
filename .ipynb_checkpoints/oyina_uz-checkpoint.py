from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.common.exceptions import NoSuchElementException,ElementClickInterceptedException
import pandas as pd
import requests

webdriver_path = 'geckodriver'
firefox_options = Options()
firefox_options.add_argument('--headless')
firefox_options.add_argument('--no-sandbox')
firefox_options.add_argument('disable-infobars')
firefox_options.add_argument("--disable-extensions")
driver = webdriver.Firefox(service=Service(webdriver_path), options=firefox_options)
driver2 = webdriver.Firefox(service=Service(webdriver_path), options=firefox_options)

urls = {"http://oyina.uz/uz/category/siyosat" : 84,"http://oyina.uz/uz/category/jamiyat" : 237,
        "http://oyina.uz/uz/category/ilm-fan" : 18,"http://oyina.uz/uz/category/madaniyat" : 33,
       "http://oyina.uz/uz/category/sport" : 12,"http://oyina.uz/uz/category/jahon" :14,
       "http://oyina.uz/uz/category/iqtisod" : 21,"http://oyina.uz/uz/articles/tarix" : 8,
       "http://oyina.uz/uz/articles/til" : 4,"http://oyina.uz/uz/articles/adabiyot" : 9,
       "http://oyina.uz/uz/articles/ta-lim" : 4,"http://oyina.uz/uz/articles/san-at" : 5, 
       "http://oyina.uz/uz/articles/mafkura" : 4,"http://oyina.uz/uz/articles/jarayon" : 2}


dataset = pd.DataFrame({"title":[""],"content":[""],"category":["news"]})

for url,total_page in zip(urls.keys(),urls.values()):
    category = url[url.rfind('/')+1:]
    print(url)
    for page in range(1,total_page):
        print('page : ',page)
        print(url + '?page=' + str(page))
        driver.get(url+'?page=' + str(page))

        html_content = driver.page_source
        soup = BeautifulSoup(html_content, "html.parser")
        title_items = soup.find_all("a",class_="category-news-content-main")

        for sub_page in title_items:

            title = sub_page.get_text()[:-1]
            title = title[title.rfind('\n')+1:]

            sub_page_link = sub_page['href']
            print(sub_page_link)
            
            driver2.get(sub_page_link)
            sub_request = driver2.page_source
            soup_sub = BeautifulSoup(sub_request, "html.parser")
            con = soup_sub.find_all("div",class_="single-news-paragraph")
            content = con[0].get_text()[1:-1]

            new_row = pd.DataFrame({'title':[title], 'content':[content],"category": [category]})
            dataset = pd.concat([dataset, new_row], ignore_index=True)
            '''if internet speed is low remove below #'''
            # dataset.to_csv('oyina_uz.csv', index=False) 

data = pd.read_csv('oyina_uz.csv')
data = data.drop_duplicates(subset=['content'])
data.to_csv('oyina_uz.csv',index=False)