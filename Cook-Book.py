# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 00:59:20 2019

@author: admin
"""

import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup

urls = ['https://www.sanjeevkapoor.com/recipe/Carrot-Cake-Cakes-and-Bakes.html',
        'https://www.sanjeevkapoor.com/recipe/Aloo-ke-Paranthe.html',
        'https://www.sanjeevkapoor.com/Recipe/Chicken-Biryani-KhaanaKhazana.html']
list_soup=[]
for url in urls:
    html = urllib.request.urlopen(url).read()
    soup=BeautifulSoup(html, 'html.parser')
    list_soup.append(soup)
#tags = soup('a')
#for tag in tags:
#    print(tag.get('href', None))
    
# Extract all heading3 and heading4 from the given URL and store in file
import io
for soup in list_soup:
    with io.open('output_all_sql.txt', 'a', encoding='utf8') as f:
        for header in soup.find_all(['h3', 'h4']):
            f.write(header.get_text() + u'\n')
            for elem in header.next_siblings:
                if elem.name and elem.name.startswith('h'):
                    # stop at next header
                    break
                if elem.name == 'p':
                    f.write(elem.get_text() + u'\n')
    

# Use regex lib to extract only recipe and ingre
# Extract dish name and append to list

import re
ingre=[]
flag=0
recipes=[]
method=[]
master=[]
r=[]

# make empty list of dict
import pandas as pd
#del(df)
df = pd.DataFrame(columns=['dish', 'ing_list', 'method'])

with open('output_all_sql.txt', encoding='utf8') as infile:
    for i, line in enumerate(infile, start=1):
        if flag==2:
            word="Nutrition Info"
            if not word in line:
                method.append(line)
        elif flag==1:
            word="Method"
            if not word in line:
                ingre.append(line)
                ing=(line.split('  ', 3)[0])
#                print(ing)
                master.append(ing)
        if (re.match('^Nutrition Info', line)):
            row={"dish": " ".join(r[2:]), "ing_list": ''.join(map(str, ingre)), "method": ''.join(map(str, method))}
            method=[]
            ingre=[]
            flag=-1
            df=df.append(row, ignore_index=True)
        elif (re.match('^Method', line)):
            flag=2
        elif (re.match('^Ingredients for ', line)):
            r=[]
            for word in line.split():
                r.append(word)
            recipes.append(" ".join(r[2:]))
            flag=1


corpus=[]
for ele in master:
    c = re.sub('[^a-zA-Z]', ' ', ele)
    corpus.append(c.lower())
