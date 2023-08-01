from bs4 import BeautifulSoup 
import pandas as pd
import requests
import csv 

dictionary = {
    'https://latifa.uz/uz_latn/tag/er-xotin?page=':75,
    'https://latifa.uz/uz_latn/tag/ayollar?page=':126,
    'https://latifa.uz/uz_latn/tag/bolalar?page=':66,
    'https://latifa.uz/uz_latn/tag/qisqa?page=':70,
    'https://latifa.uz/uz_latn/tag/hayvonot?page=':35,
    'https://latifa.uz/uz_latn/tag/qorayumor?page=':36,
    'https://latifa.uz/uz_latn/tag/ota-ona?page=':27,
    'https://latifa.uz/uz_latn/tag/pul-boylik?page=':44,
    'https://latifa.uz/uz_latn/tag/haydovchilar?page=':23,
    'https://latifa.uz/uz_latn/tag/yoshlar?page=':45,
    'https://latifa.uz/uz_latn/tag/oqish-maktab?page=':25,
    'https://latifa.uz/uz_latn/tag/erkaklar?page=':127,
    'https://latifa.uz/uz_latn/tag/uddaburonlar?page=':43,
    'https://latifa.uz/uz_latn/tag/kasalxonada?page=':16,
    'https://latifa.uz/uz_latn/tag/boshqalar?page=':45,
    'https://latifa.uz/uz_latn/tag/sevishganlar?page=':15,
    'https://latifa.uz/uz_latn/tag/afandi?page=':31,
    'https://latifa.uz/uz_latn/tag/dostlar?page=':27,
    'https://latifa.uz/uz_latn/tag/shifokorlar?page=':24,
    'https://latifa.uz/uz_latn/tag/qariyalar?page=':20,
    'https://latifa.uz/uz_latn/tag/ustoz-shogird?page=':11,
    'https://latifa.uz/uz_latn/tag/ishxona?page=':21,
    'https://latifa.uz/uz_latn/tag/drunk?page=':17,
    'https://latifa.uz/uz_latn/tag/ovqatlanish?page=':19,
    'https://latifa.uz/uz_latn/tag/millatlar?page=':14,
    'https://latifa.uz/uz_latn/tag/jinoyatchilar?page=':13,
    'https://latifa.uz/uz_latn/tag/dokon-bozor?page=':15,
    'https://latifa.uz/uz_latn/tag/ozbekona?page=':59,
    'https://latifa.uz/uz_latn/tag/boshliqlar?page=':12,
    'https://latifa.uz/uz_latn/tag/internet?page=':13,
    'https://latifa.uz/uz_latn/tag/qoshnilar?page=':10,
    'https://latifa.uz/uz_latn/tag/janjal?page=':8,
    'https://latifa.uz/uz_latn/tag/talabalar?page=':10,
    'https://latifa.uz/uz_latn/tag/sport?page=':10,
    'https://latifa.uz/uz_latn/tag/kaltafahmlar?page=':36,
    'https://latifa.uz/uz_latn/tag/transportda?page=':8,
    'https://latifa.uz/uz_latn/tag/dan?page=':7,
    'https://latifa.uz/uz_latn/tag/telefon?page=':15,
    'https://latifa.uz/uz_latn/tag/harbiylar?page=':7,
    'https://latifa.uz/uz_latn/tag/bemorlar?page=':15,
    'https://latifa.uz/uz_latn/tag/shoh-boy?page=':8,
    'https://latifa.uz/uz_latn/tag/qaynona-qaynota?page=':8,
    'https://latifa.uz/uz_latn/tag/jinnilar?page=':6,
    'https://latifa.uz/uz_latn/tag/uchrashuv?page=':6,
    'https://latifa.uz/uz_latn/tag/militsiya?page=':4,
    'https://latifa.uz/uz_latn/tag/lof-yolgon?page=':29,
    'https://latifa.uz/uz_latn/tag/dugonalar?page=':9,
    'https://latifa.uz/uz_latn/tag/haqiqat-adolat?page=':37,
    'https://latifa.uz/uz_latn/tag/sudda?page=':5,
    'https://latifa.uz/uz_latn/tag/oila?page=':78,
    'https://latifa.uz/uz_latn/tag/bayramlar?page=':4,
    'https://latifa.uz/uz_latn/tag/kafe-restoran?page=':5,
    'https://latifa.uz/uz_latn/tag/ertaklar?page=':10,
    'https://latifa.uz/uz_latn/tag/mehmon-mezbon?page=':4,
    'https://latifa.uz/uz_latn/tag/salomatlik?page=':16,
    'https://latifa.uz/uz_latn/tag/uynash-jazman?page=':6,
    'https://latifa.uz/uz_latn/tag/uqituvchi-domla?page=':10,
    'https://latifa.uz/uz_latn/tag/ovchi-baliqchi?page=':4}


dataset = pd.DataFrame({'title': [],'content': []})


for url,last in zip(dictionary.keys(),dictionary.values()):
    title_text = url[url.rfind('/')+1:url.rfind('?')]
    for i in range(last):
        page = requests.get(url+str(i))

        soup = BeautifulSoup(page.content, "html.parser")
        items = soup.find_all("div",class_="bg-white rounded mb-2 p-3")
        print('title_text = ',title_text)
        print('page_number = ',i)
        for item in items:
            content_text = item.text[1:item.text.rfind('.')]

            new_row = pd.DataFrame({'title':[title_text], 'content':[content_text]})
            dataset = pd.concat([dataset, new_row], ignore_index=True)
            

dataset = dataset.drop_duplicates(subset=['content'],ignore_index=True)
dataset.to_csv('latifa_uz.csv', index=False)