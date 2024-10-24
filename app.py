import requests
from bs4 import BeautifulSoup
import json
import os

# read Data From settings
settingsJsonFile = open("settings.json") #settingsJsonFile location
settingsJsonData = json.load(settingsJsonFile) 
settingsJsonFile.close()
print("settings : ")
print(settingsJsonData)

#Http request
requestHeaders = {'user-agent': settingsJsonData["user-agent"]}
print("Http Request Headers:")
print(requestHeaders)

def getDataInHtml(url):
    r = requests.get(url)
    print("Http Status Code : "+ str(r.status_code))
    if r.status_code == 200:
        return BeautifulSoup(r.text,'html.parser')
    else : 
        print("Failed! can't conect to URL")
        exit()

def DlAllImgFromHtml(html):
    returnArray = []
    for i in html.find_all("img"):
        returnArray.append(i["src"])
        print("Found Image : "+str(i["src"]))
    return returnArray

def DlImg(url):
    if os.path.isdir(settingsJsonData["downloadDirectory"]) != True:
        os.mkdir(settingsJsonData["downloadDirectory"]) 

    with open(f"{settingsJsonData["downloadDirectory"]}/{url.split("/")[-1]}","wb") as file:
        file.write(requests.get(url).content)

def DlArrayImg(urlArray):
    for x in urlArray:
        DlImg(x)

print("Check Config Folder For Settings")

#test

a = input("url")
DlArrayImg(DlAllImgFromHtml(getDataInHtml(a)))
