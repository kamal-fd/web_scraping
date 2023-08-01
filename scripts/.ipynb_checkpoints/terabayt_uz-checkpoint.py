from bs4 import BeautifulSoup 
import pandas as pd
import requests
import csv 

url = "https://terabayt.uz/"
all_pages = []

page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")
items = soup.find_all("ul",class_="header_bottom-nav")
menu = []
count = 0
for item in items:
    links = [a['href'] for a in item.find_all('a')]
    for link in links:
        if 'uz' in link and link not in menu:
            menu.append(link)

dataset = pd.DataFrame({'title': [],'content': [],'category': []})
for one_page in menu[13:]:

    one = requests.get(one_page)
    soup_one = BeautifulSoup(one.content, "html.parser")

    if soup_one.find_all("li",class_="last"):
        items_one = soup_one.find_all("li",class_="last")
        tag = items_one[0].find_all('a')
        last_sub_page_link = tag[0]['href']
        st = tag[0]['href'].find('?page=') + 6
        end = tag[0]['href'].find('&')
        last_sub_page_number = int(tag[0]['href'][st:end])
        ending = last_sub_page_link.find('?')
        category_text = last_sub_page_link[10:ending]
    else:
        continue
   
    print(last_sub_page_number)
    
    for loop in range(1,last_sub_page_number+1):
        
        sub_page = url + last_sub_page_link[:st] + str(loop) + last_sub_page_link[end:]
        print(sub_page)
        info = requests.get(sub_page)
        html_code = BeautifulSoup(info.content, "html.parser")
        news = html_code.find_all("div",class_="news_item")
        posts = [i.find_all('a')[0]['href'] for i in news]
        posts = list(set(posts))
        
        for post in posts:
            scraping_page = url + 'uz' + post 
            if scraping_page not in all_pages:
                all_pages.append(scraping_page)
            
            else:
                continue

            

            response = requests.get(scraping_page)
            response_parse = BeautifulSoup(response.content, "html.parser")
            
            for_title = response_parse.find_all('div',class_ = 'article post-view')

            second_parse = BeautifulSoup((str(for_title[0])),'html.parser')
            title_text = second_parse.find('h1').text
            for_content = response_parse.find_all('div',class_ = 'article-content')
            content = BeautifulSoup((str(for_content[0])),'html.parser')
            content_text = ''
            for i in content.find_all('p'):
                
                parse = BeautifulSoup(str(i),'html.parser')
                content_text += parse.find('p').text

            count += 1
            print('count = ' ,count) 
            print('category = ',category_text)
            print(scraping_page)




            new_row = pd.DataFrame({'title':[title_text], 'content':[content_text], 'category': [category_text]})
            dataset = pd.concat([dataset, new_row], ignore_index=True)
            # dataset.to_csv('terabayt_uz' + category_text + '.csv', index=False)

ataset = dataset.drop_duplicates(subset=['content'],ignore_index=True)
dataset.to_csv('terabayt_uz', index=False)