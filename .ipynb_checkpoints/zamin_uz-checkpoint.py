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

url = "https://zamin.uz/uz/"

navbar=[]
driver.get(url)
html_content = driver.page_source
soup = BeautifulSoup(html_content, "html.parser")

menu_items = soup.find("ul",class_="header-menu fx-row fx-center fx-1 to-mob").find_all("li")
for menu in menu_items:
    menu_link = menu.find("a",class_="title")["href"]
    print(menu_link)
    navbar.append(menu_link)

dataset = pd.DataFrame({"title":[""],"content":[""],"category":[""]})
pages = [349,1347,1547,255,1176,111,225,143,67,339]
temp,x = 0,True

for menu,page_ in zip(navbar,pages):
    
    category = menu.split('/')[-1]
    print(f"{menu} is started...")
    
    print(menu)
    for page in range(1,page_+1):
        driver.get(menu+f"page/{page}/")
        
        try:
            html_content = driver.page_source
            soup = BeautifulSoup(html_content, "html.parser")
            items = soup.find("div",class_="sect-content fx-row").find_all("div",class_="short-item")
            
            if len(items) < 1 :
                continue
            print(page)
            
            for item in items:
                link = item.find("a",class_="short-img img-resp img-fit anim")["href"]
                if len(link) < 1 :
                    continue
                print(link)
                driver2.get(link)
                html_content = driver2.page_source
                soup = BeautifulSoup(html_content, "html.parser")
                title = soup.find("article",class_="article").find("h1").text
                if len(title) < 1 :
                    continue
                
                content = "".join([text.text.strip() for text in soup.find("article",class_="article").find("div",class_="fdesc full-text video-box clearfix fx-1").find_all("p")])
                
                if len(content)==0:
                    content = "".join([text.text.strip() for text in soup.find("article",class_="article").find_all("span")])
                    if x:
                        print(content)
                        x=False
                if len(content)<=10:
                    print("olinmadi")
                    continue
                    
                if len(title)>1 and len(content)>10:
                    
                    new_row = pd.DataFrame({'title':[title], 'content':[content],"category":[category]})
                    dataset = pd.concat([dataset, new_row], ignore_index=True)
                    
        except:
            continue

dataset = dataset.drop_duplicates(subset=['content'],ignore_index=True)
dataset.to_csv('zamin_uz.csv', index=False)