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

def checkAndCombineRepeatedUrl(urlA,urlB):
    #output urlB(website) -> urlA(img)
    urlArrayA =urlA.split("/")
    urlArrayB = urlB.split("/")
    returnArray = []
    for x in urlArrayA:
        for y in urlArrayB:
            if x == y and x != "http:" and x != "https:":
                returnArray.append(x)
    if returnArray == []:
        return None
    else:
        for z in returnArray:
            urlArrayA.remove(z)
        returnUrl = urlB
        if returnUrl.endswith("/"):
            returnUrl = returnUrl[1:]
        for i in urlArrayA:
            returnUrl= returnUrl+"/"+i
        return returnUrl        
        

def convertUrlForDlImg(imgUrl,websiteUrl):
    if imgUrl.startswith("https://") or imgUrl.startswith("http://") :
        return imgUrl
    elif imgUrl.startswith("//"):
        return "http:"+imgUrl
    else :
        checkResults = checkAndCombineRepeatedUrl(imgUrl,websiteUrl)
        if checkResults == None:
            if (imgUrl.startswith("/") and websiteUrl.endswith("/") == False) or (imgUrl.startswith("/") == False and websiteUrl.endswith("/")) :
                    return websiteUrl+imgUrl
            elif imgUrl.startswith("/") == False and websiteUrl.endswith("/") == False:
                    return websiteUrl+"/"+imgUrl
            elif imgUrl.startswith("/") and websiteUrl.endswith("/") :
                    return websiteUrl[1:]+imgUrl
        else:
            return checkResults
            
            



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
        image = requests.get(url)
        if image.status_code == 200:
            print(f"Downloaded From {url}")
            with open(f"{settingsJsonData["downloadDirectory"]}/{url.split("/")[-1]}","wb") as file:
                print(f"Trying to Download from {url}")
                file.write(image.content)
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
