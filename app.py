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

def convertUrlForDlImg(imgUrl,websiteUrl):
    if imgUrl.startswith("https://") or imgUrl.startswith("http://") :
        return imgUrl
    elif imgUrl.startswith("//"):
        return "http:"+imgUrl
    else :
        if (imgUrl.startswith("/") & websiteUrl.endswith("/") == False) or (imgUrl.startswith("/") == False & websiteUrl.endswith("/")) :
            return websiteUrl+imgUrl
        elif imgUrl.startswith("/") == False & websiteUrl.endswith("/") == False:
            return websiteUrl+"/"+imgUrl
        elif imgUrl.startswith("/") & websiteUrl.endswith("/") :
            return websiteUrl+imgUrl[1:]



def getDataInHtml(url):
    r = requests.get(url)
    print("Http Status Code : "+ str(r.status_code))
    if r.status_code == 200:
        return BeautifulSoup(r.text,'html.parser')
    else : 
        print("Failed! can't conect to URL")
        exit()

def getAllImgFromHtml(html):
    returnArray = []
    for i in html.find_all("img"):
        returnArray.append(i["src"])
        print("Found Image : "+str(i["src"]))
    return returnArray

def DlImg(url):
    if os.path.isdir(settingsJsonData["downloadDirectory"]) != True:
        os.mkdir(settingsJsonData["downloadDirectory"])
    
    try:
        with open(f"{settingsJsonData["downloadDirectory"]}/{url.split("/")[-1]}","wb") as file:
            print(f"Trying to Download from {url}")
            image = requests.get(url)
            if image.status_code == 200:
                file.write(image.content)
                print(f"Downloaded From {url}")
            else:
                print(f"Unable to Download File, Status Code {image.status_code}")
    except requests.exceptions.RequestException as e:
        print("Unable to Download Image:", e)

def DlArrayImg(urlArray,userInputWebsiteUrl):
    for x in urlArray:
        DlImg(convertUrlForDlImg(x,userInputWebsiteUrl))

print("Check Config Folder For Settings")

#test

a = input("url")

DlArrayImg(getAllImgFromHtml(getDataInHtml(a)),a)
