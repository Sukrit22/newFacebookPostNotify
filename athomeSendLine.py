
'''Scraping Section'''

import os
import json
import time
from bs4 import BeautifulSoup as soup
from bs4.element import Tag
from bs4.element import NavigableString
from selenium.webdriver.common.by import By
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.service import Service
from selenium import webdriver
from songline import Sendline
options = webdriver.EdgeOptions()
options.use_chromium = True
options.add_argument('headless')
options.add_argument("window-size=1920,1080")
# driverPath = r"./edgedriver_win64/msedgedriver.exe"
driver = webdriver.Edge(service=Service(
    EdgeChromiumDriverManager().install()), options=options)

f = open('linetoken.txt', 'r')
token = f.read()
f.close()


def getFacebookPost(page_name):

    url = "https://www.facebook.com/{}".format(page_name)
    driver.get(url)
    time.sleep(5)
    driver.execute_script("window.scrollTo(0, 1000)")  # to load more posts
    time.sleep(5)

    page_html = driver.page_source
    driver.quit()

    data = soup(page_html, 'html.parser')

    # print(data.prettify())

    # with open('spoiler.txt', 'w', encoding='utf-16') as f:
    #    f.write(data.prettify())

    # post = data.find(text='Just now')
    # print(post)

    '''test post class and filter out span of emoji
    with <div dir="auto" style="text-align: start;">...</div> per line in the post

    1. filter find_all class = kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x c1et5uql ii04i59q
    2. filter line by for each posts find_all <div dir="auto" style="text-align: start;">
    3. filter out emoji by for each line and do some magic to filter out <span> </span>
    '''
    posts = data.find_all(
        'div', {'class': 'kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x c1et5uql ii04i59q'})

    # print('before :\n'+str(posts))
    posts.pop(0)
    # print('after :\n'+str(posts))
    sss = []
    postsData = []
    # onlyString = []
    for post in posts:
        line = post.find_all('div', {'dir': 'auto'})
        for l in line:
            l = l.contents
            for inl in l:
                if isinstance(inl, Tag):
                    # print('Tag')
                    sss.append(inl.img['alt'])
                if isinstance(inl, NavigableString):
                    # print('String')
                    sss.append(inl.string)
                    # onlyString.append(inl.string)
                # print(type(inl), end='\n---\n')
            # print(l, end='\n---\n')
        mypost = ' '.join(sss)
        sss = []
        print('mypost :\n'+mypost)
        postsData.append(mypost)
        mypost = ''

    # onlyString = ' '.join(onlyString)
    # print(sss)
    # return [mypost, onlyString]
    return postsData
    # print(posts)
    # allposts = []
    # for p in posts:
    #    print(p, end='\n\n')


posts = getFacebookPost('AT-Home-Study-Travel-Team-143632995663399/')

# post = myArr[0]
# myTxt = myArr[1]
# print(type(post))
# print(type(myTxt))

# getFacebookPost('animethspoiler/')

''' check if this post is not in txt

1. read file = > r
2. compare if r == post:
3. yes nothing
3. no send line and delete file the create again and write post = > file
'''
f = ''
try:
    f = open('newpost.txt', 'r', encoding='utf-16')
except:
    f = open('newpost.txt', 'w', encoding='utf-16')
    f.write(json.dumps({'newestPost': ''}))
    f.close()
    f = open('newpost.txt', 'r', encoding='utf-16')

r = json.loads(f.read())
f.close()
indexFound = -1
index = 0
for post in posts:
    if post == r['newestPost']:
        indexFound = index
    index += 1
r['newestPost'] = posts[0][:60]

if os.path.exists("newpost.txt"):
    os.remove('newpost.txt')
f = open('newpost.txt', 'w', encoding='utf-16')
f.write(json.dumps(r))
f.close()
# r['others'] = posts[1:]

'''Send Line Section'''


def send_to_line(token, facebookPost):
    lineBot = Sendline(token)
    lineBot.sendtext(facebookPost)
    lineBot.sticker(180, 3)


if indexFound < 0:  # not found so we send all
    # send allposts
    for post in posts:
        # send
        send_to_line(token, post)
else:  # found at position so we send until that position
    index = 0
    for post in posts:
        if index < indexFound:
            # send
            send_to_line(token, post)
        index += 1
