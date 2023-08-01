from bs4 import BeautifulSoup 
import pandas as pd
import requests
import csv
from urllib.request import Request, urlopen

urls = ["https://ertak.uz/tale/taleuz","https://ertak.uz/tale/taleru","https://ertak.uz/tale/wtale",
        "https://ertak.uz/masal/ezop","https://ertak.uz/masal/krilov",
        "https://ertak.uz/poetry"] 

dataset = pd.DataFrame({'title': [],'content': []})

for url in urls:
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    items = soup.find_all("div",class_="wp-pagenavi")
    last_sub_page = items[0].find_all('a')[-1]['href']
    number = int(last_sub_page[last_sub_page.rfind('/')+1:]) + 1    
    
    
    for loop in range(1,number):
        
        for_script = last_sub_page[:last_sub_page.rfind('/')] + str(loop)
        page_for_script = requests.get(for_script)
        html = BeautifulSoup(page_for_script.content, "html.parser")
        items_html = html.find_all("h1",class_="entry-title")
        links = [item.find_all("a")[0]['href'] for item in items_html]
        
        for link in links:
            request_link = requests.get(link)
            html_link = BeautifulSoup(request_link.content, "html.parser")
            items_link = html_link.find_all("span",class_="date")
            title_text = [item.find_all("a")[0]['title'] for item in items_link][0]
            
            for_content = html_link.find_all("div",class_="entry-content")
            
            content = BeautifulSoup((str(for_content[0])),'html.parser')
            content_text = ''
            for i in content.find_all('p'):
                
                parse = BeautifulSoup(str(i),'html.parser')
                content_text += parse.find('p').text
                
            new_row = pd.DataFrame({'title':[title_text], 'content':[content_text]})
            dataset = pd.concat([dataset, new_row], ignore_index=True)
            

dataset = dataset.drop_duplicates(subset=['content'],ignore_index=True)
dataset.to_csv('ertak_uz.csv', index=False)