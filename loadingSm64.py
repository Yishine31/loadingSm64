import requests
from bs4 import BeautifulSoup
import os
import time
import re

def create_folder(foldername):
    if not os.path.isdir(foldername):
        os.mkdir(foldername)

def get_url(url):
    urls = []
    for i in range(1,65):
        urls.append(f"{url+str(i)}")            
    return urls

def reg_things(things):
    re_thing = []
    res_1 = re.search("諸事：",things)
    res_2 = re.search("愛情：",things)
    res_3 = re.search("事業：",things)
    res_4 = re.search("財運：",things)
    res_5 = re.search("建議：",things)

    state =[]

    if(res_1):
        res_1 = res_1.span()
        state += '1'
    else:
        res_1 = ""
        state +='0'
    if(res_2):
        res_2 = res_2.span()
        state += '1'
    else:
        res_2 = ""
        state +='0'
    if(res_3):
        res_3 = res_3.span()
        state += '1'
    else:
        res_3 = ""
        state +='0'
    if(res_4):
        res_4 = res_4.span()
        state += '1'
    else:
        res_4 = ""
        state +='0'
    if(res_5):
        res_5 = res_5.span()
        state += '1'
    else:
        res_5 = "" 
        state +='0' 
    match state:
        case ['1', '1', '1', '0', '1']:
            if((str(type(res_1))=='<class \'tuple\'>') & (str(type(res_2))=='<class \'tuple\'>')):
                things_1 = things[res_1[0]:res_2[0]]
                re_thing += [things_1]
            if((str(type(res_2))=='<class \'tuple\'>') & (str(type(res_3))=='<class \'tuple\'>')):
                things_2 = things[res_2[0]:res_3[0]]
                re_thing += [things_2]
            if((str(type(res_3))=='<class \'tuple\'>') & (str(type(res_5))=='<class \'tuple\'>')):
                things_3 = things[res_3[0]:res_5[0]]
                re_thing += [things_3]
            if((str(type(res_5))=='<class \'tuple\'>')):
                things_5 = things[res_5[0]:]
                re_thing += [things_5]
        case ['1', '1', '1', '1', '1']:
            if((str(type(res_1))=='<class \'tuple\'>') & (str(type(res_2))=='<class \'tuple\'>')):
                things_1 = things[res_1[0]:res_2[0]]
                re_thing += [things_1]
            if((str(type(res_2))=='<class \'tuple\'>') & (str(type(res_3))=='<class \'tuple\'>')):
                things_2 = things[res_2[0]:res_3[0]]
                re_thing += [things_2]
            if((str(type(res_3))=='<class \'tuple\'>') & (str(type(res_4))=='<class \'tuple\'>')):
                things_3 = things[res_3[0]:res_4[0]]
                re_thing += [things_3]
            if((str(type(res_4))=='<class \'tuple\'>') & (str(type(res_5))=='<class \'tuple\'>')):
                things_4 = things[res_4[0]:res_5[0]]
                re_thing += [things_4]
            if((str(type(res_5))=='<class \'tuple\'>')):
                things_5 = things[res_5[0]:]
                re_thing += [things_5]
 
    # print(state)
    return re_thing

def get_content(url):
    text = ""
    print(f'content: {url} loading...')
    res = requests.get(url)
    bs = BeautifulSoup(res.text,"lxml")
    title = bs.find('div',id="block-bartik-pagetitle").find('h1').get_text()
    content = bs.find('div',id="block-bartik-content").find('div',class_="clearfix text-formatted field field--name-body field--type-text-with-summary field--label-hidden field__item")
    ps = content.find_all('p')
    
    name = "掛名 : " + ps[0].get_text()
    booksay = ps[1].get_text()
    things = ps[2].get_text()
    text += name + '\n' + booksay +'\n\n'
    rethings = reg_things(things)
    for i in rethings:
        text += i+'\n'
    cont = ""
    for j in range(4,8):
        cont += ps[j].get_text() + '\n'
    text += "\n掛詞解釋 : \n" + cont
    return text,title

    # text += title+'\n'
    # for tex in ps[:-2]:
    #     print(tex.get_text())
        # text += tex.get_text()+'\n'
    # return text,title

def get_titleAndSymbol(urls):  
    title = []
    for i in urls:
        temp = ""
        print(f'content: {i} loading...')
        res = requests.get(i)
        bs = BeautifulSoup(res.text,"lxml")
        temp_tit = bs.find('div',id="block-bartik-pagetitle").find('h1').get_text()
        temp_sym = bs.find('div',id="block-bartik-content").find_all('p')[0].find('span').get_text().strip()
        # text,title = get_content(url_1)
        temp_tit = temp_tit[:-1]
        temp += temp_tit + ' ' + temp_sym
        title.append(f"{temp}")
    print(title)
    text = ""
    for t in title:
        text += t + '\n'
    return text,title

def save_file(filename,text):
    f = open(f"simple64\{filename}.txt",'w',encoding='utf8')
    f.write('\ufeff')
    f.write(text)
    f.close()


url = 'https://www.eee-learning.com/simple64/'
urls = get_url(url)

url_1 = ['https://www.eee-learning.com/simple64/2']
# text,title  = get_content(url_1)

# text,title = get_titleAndSymbol(url_1)
# save_file("掛名與卦象",text)

# 爬取所有掛名與卦象

text,title = get_titleAndSymbol(urls)
save_file("掛名與卦象",text)

#爬取易學網內容
''' 
for i in urls:
    text,title = get_content(i)
    # text,title = get_content(url_1)
    title = title[:-1]
    print(title)
    save_file(f"simple64\{title}",txt,text)
    print(f"{title} -done!")
    time.sleep(10)
'''

