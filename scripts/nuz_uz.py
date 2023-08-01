from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.common.exceptions import NoSuchElementException,ElementClickInterceptedException
import pandas as pd

webdriver_path = 'geckodriver'
firefox_options = Options()
firefox_options.add_argument('--headless')
firefox_options.add_argument('--no-sandbox')
firefox_options.add_argument('disable-infobars')
firefox_options.add_argument("--disable-extensions")
driver = webdriver.Firefox(service=Service(webdriver_path), options=firefox_options)

navbar = 'https://nuz.uz/uz/vse-novosti/page/'

dataset = pd.DataFrame({"title":[""],"content":[""],"category":[""]})
pages = 298

for page in range(1,pages+1):
    print(navbar+str(page))
    driver.get(navbar+str(page))
    try:
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, "html.parser")
        title_items = soup.find_all("h3",class_="entry-title td-module-title")
        content_items = soup.find_all("div",class_="td-post-text-content td-post-content tagdiv-type")
        for item_t,item_c in zip(title_items,content_items):
            title = item_t.find_all('a')[0]['title']
            content = item_c.get_text()
            new_row = pd.DataFrame({'title':[title], 'content':[content],"category":[""]})
            dataset = pd.concat([dataset, new_row], ignore_index=True)
            
        print('page : ',page)
    except:
        continue

dataset = dataset.drop_duplicates(subset=['content'],ignore_index=True)
dataset.to_csv('nuz_uz.csv', index=False)