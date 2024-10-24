import requests
from bs4 import BeautifulSoup
requestHeaders = {'user-agent': 'Penguinly/1.0.0'}

def getDataInHtml(url):
    r = requests.get(url)
    print("Http Status Code : "+ str(r.status_code))
    return BeautifulSoup(r.text,'html.parser')

def DlAllImgFromHtml(html):
    for i in html.find_all("img"):
        print(i["src"])

print("Check Config Folder For Settings")
a = input("url")
DlAllImgFromHtml(getDataInHtml(a))
