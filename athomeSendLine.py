
'''Scraping Section'''

from songline import Sendline
from selenium import webdriver
from msedge.selenium_tools import EdgeOptions
from msedge.selenium_tools import Edge
from bs4 import BeautifulSoup as soup
import time
import json
options = EdgeOptions()
options.use_chromium = True
options.add_argument('headless')
driverPath = r"edgedriver_win64/msedgedriver.exe"
driver = Edge(driverPath, options=options)


def getFacebookPost(page_name):

    url = "https://www.facebook.com/{}".format(page_name)
    driver.get(url)

    time.sleep(5)

    page_html = driver.page_source

    data = soup(page_html, 'html.parser')

    print(data)

    #posts = data.find_all()


getFacebookPost('AT-Home-Study-Travel-Team-143632995663399/')
driver.close()

'''Send Line Section'''


def send_to_line(token):
    lineBot = Sendline(token)

    f = ''
    try:
        f = open('athomeposts.json', 'rt')
    except:
        f = open('athomeposts.json', 'wt')
        f.write(json.dumps({'newestPost': ''}))
        f.close()
        f = open('athomeposts.json', 'rt')

    myJson = json.loads(f.read())
    indexFound = -1
    index = 0
    for post in facebookPost:
        if post == myJson['newestPost']:
            indexFound = index
        index += 1
    myJson['newestPost'] = facebookPost[0]
    f.close()
    f = open('athomeposts.json', 'wt')
    f.write(json.dumps(myJson))
    f.close()
    if indexFound < 0:
        # send allposts
        for post in facebookPost:
            # send
            lineBot.sendtext(post)
    else:
        index = 0
        for post in facebookPost:
            if index < indexFound:
                # send
                lineBot.sendtext(post)
            index += 1


token = 'JtWsHjKu8R3flkoQaDtEJUBDOevzkr0BLkAZmjiOX6q'
# send_to_line(token)
