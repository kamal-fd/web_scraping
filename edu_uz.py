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

url = 'https://edu.uz/uz/news/index?page='

dataset = pd.DataFrame({"title":[""],"cont%%fileent":[""],"category":["news"]})

for page in range(1,531):
    print(url+str(page)+"&per-page=10")
    driver.get(url+str(page))
    try:
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, "html.parser")
        title_items = soup.find_all("div",class_="col-md-10")
        
        for sub_page in title_items[1:]:
            text = sub_page.get_text()
            title = text[:text.find('Manba')]

            sub_page_link = "https://edu.uz" + sub_page.find_all('a')[0]['href']
            print(sub_page_link)
            driver2.get(sub_page_link)
            sub_request = driver2.page_source
            soup_sub = BeautifulSoup(sub_request, "html.parser")
            con = soup_sub.find_all("div",class_="col-md-12")
            content = con[0].get_text()
        

            new_row = pd.DataFrame({'title':[title], 'content':[content],"category":["news"]})
            dataset = pd.concat([dataset, new_row], ignore_index=True)
            
        print('page : ',page)
    except:
        continue

dataset = dataset.drop_duplicates(subset=['content'],ignore_index=True)
dataset.to_csv('edu_uz.csv', index=False)