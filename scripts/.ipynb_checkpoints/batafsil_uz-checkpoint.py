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

url = 'https://batafsil.uz/cat/ajax/load.php?SECTION_ID=&PAGE_NUMBER=11&LAST_ID=NaN&IBLOCK_ID=43&IBLOCK_TYPE=news&AUTHOR_ID='

dataset = pd.DataFrame({"title":[""],"content":[""],"category":["news"]})

cnt = 0   

while True:
    cnt +=1
    print('page : ',cnt)
    try :
        driver.get(url[:url.find('NUMBER=')+7] + str(cnt) + url[url.find('&LAST_ID'):])

        html_content = driver.page_source
        soup = BeautifulSoup(html_content, "html.parser")
        title_items = soup.find_all("h3",class_="post-title entry-title")


        for sub_page in title_items:

            title = sub_page.find_all('a')[0].get_text()


            sub_page_link = "https://www.batafsil.uz" + sub_page.find_all('a')[0]['href']
            print(sub_page_link)
            driver2.get(sub_page_link)
            sub_request = driver2.page_source
            soup_sub = BeautifulSoup(sub_request, "html.parser")
            con = soup_sub.find_all("div",class_="detail-text")


            content = con[0].get_text()[1:]
            
            name = 'Ўзбекистон, Тошкент – Batafsil.uz. '
            if name in content:
                content = content[content.find(name)+len(name):]

            new_row = pd.DataFrame({'title':[title], 'content':[content],"category":["news"]})
            dataset = pd.concat([dataset, new_row], ignore_index=True)
            
    except:
        break

dataset = dataset.drop_duplicates(subset=['content'],ignore_index=True)
dataset = dataset[1:]
dataset.to_csv('batafsil_uz.csv',index=False)
