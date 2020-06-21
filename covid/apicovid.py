import json
import os
import sys
import re
import requests
import copy
from bs4 import BeautifulSoup as bs
from base64 import b64encode
import pandas as pd
print("Get Data...")


def Reverse(lst):
    return [ele for ele in reversed(lst)]


def GetList(jsn, apa):
    return [x[apa] for x in jsn]


def GetNameCountry(jsn):
    lst = []
    for key in jsn.keys():
        lst.append(key)
    lst.sort()
    return lst


def GetSelisih(nama, i, x, jsn, ket=False):
    tmp = 0
    if not x[nama] == 0:
        tmp = int(x[nama]) - int(Reverse(jsn[reqion])[i][nama]
                                 ) if ket else int(x[nama]) - int(Reverse(jsn[reqion])[i+1][nama])
    return tmp


def PrintAll(df):
    pd.set_option('display.max_rows', len(df))
    print(df)
    pd.reset_option('display.max_rows')


def GetDataNow(now, nama):
    for i, x in enumerate(now["areas"]):
        if x["id"] == nama:
            return now["areas"][i]
# head = {
#     "authorization":"Basic ZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SnBaeUk2SWtVeFFrUXpNakF4UlRaQ056UXhNMFE1TVVKR01EVTFNemxGTVVJMk9FTXhJaXdpYzJsa0lqb2lNalF6UlVReFFVVkdRelJETmtVeE5ESTJSRE5FUmpBelJrUTROelpHTXpZaUxDSnBZWFFpT2pFMU9EWTVOVEV3TWpNc0ltVjRjQ0k2TVRVNE56QXpOelF5TTMwLnFGbU16WjdJTS12cDQtSXJwdW1MUXJOZ0xEdk5jdnJrS3pYUXN1SEhIWkU=",
#     "cookie":"_EDGE_S=F=1&SID=243ED1AEFC4C6E1426D3DF03FD876F36; _EDGE_V=1; MUID=2F0541A7A1F66C8B31FE4F0AA03D6DC0; SRCHD=AF=NOFORM; SRCHUID=V=2&GUID=849E5B4DAB6E48DBA2FC512AAB89C6C7&dmnchg=1; _SS=SID=243ED1AEFC4C6E1426D3DF03FD876F36; MUIDB=2F0541A7A1F66C8B31FE4F0AA03D6DC0; SRCHUSR=DOB=20200415&T=1586949644000; SRCHHPGUSR=WTS=63722546444; _clarity=42a86488a9d2450e9778dcec62658b9c",
#     "referer":"https://bing.com/covid",
#     "sec-fetch-dest": "empty",
#     "sec-fetch-mode": "cors",
#     "sec-fetch-site": "same-origin",
#     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36 OPR/67.0.3575.130"
# }


# rq = requests.get("https://bing.com/covid/graphdata?ig=E1BD3201E6B7413D91BF05539E1B68C1", headers=head)
# jsn = rq.json()

try:
    rq = requests.get("https://bing.com/covid", timeout=100)
except Exception as e:
    rq = requests.get("https://bing.com/covid", timeout=100)
head = rq.headers

regex = r'(<div id="main"><script type="text/javascript">var data=)(.*?)(</script></div>)'
matches = re.finditer(regex, rq.text, re.MULTILINE)
now = json.loads([str(x.group()).replace('<div id="main"><script type="text/javascript">var data=',
                                         "").replace("</script></div>", "").replace(";", "") for x in matches][0])

regex = r'(var ig=")\w+'
matches = re.finditer(regex, rq.text, re.MULTILINE)
ig = [str(x.group()).replace('var ig="', "") for x in matches][0]

regex = r"(token=)'(.*?)'"
matches = re.finditer(regex, rq.text, re.MULTILINE)
for x in matches:
    tmp = "{}".format(str(x.group()).replace("token=", "").replace("'", ""))
    token = "Basic {}".format(b64encode(bytes(tmp, "utf-8")).decode("utf-8"))

head = {
    "ept": "*/*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9",
    "authorization": token,
    "cookie": "_EDGE_S=F=1&SID=243ED1AEFC4C6E1426D3DF03FD876F36; _EDGE_V=1; MUID=2F0541A7A1F66C8B31FE4F0AA03D6DC0; SRCHD=AF=NOFORM; SRCHUID=V=2&GUID=849E5B4DAB6E48DBA2FC512AAB89C6C7&dmnchg=1; _SS=SID=243ED1AEFC4C6E1426D3DF03FD876F36; MUIDB=2F0541A7A1F66C8B31FE4F0AA03D6DC0; SRCHUSR=DOB=20200415&T=1586949644000; SRCHHPGUSR=WTS=63722546444; _clarity=42a86488a9d2450e9778dcec62658b9c",
    "referer": "https://bing.com/covid",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36 OPR/67.0.3575.130"
}

hit = f"https://bing.com/covid/graphdata?ig={ig}"
# news = f"https://bing.com/covid/bingapi?ig={ig}&q=coronavirus Indonesia&api=news&count=20"
# video = f"https://bing.com/covid/bingapi?ig={ig}&q=coronavirus Indonesia&api=video&count=20"
# print(hit, token)
try:
    rq = requests.get(hit, headers=head, timeout=100)
except Exception as e:
    rq = requests.get(hit, headers=head, timeout=100)

jsn = rq.json()

def DataNow():
    global now
    return now


def DataLast():
    global jsn
    return jsn


def GetRegion():
    global now
    dt = {"data": []}
    for x in now["areas"]:
        tmp = {}
        tmp["id"] = x["id"]
        tmp["country"] = x["displayName"]
        dt["data"].append(tmp)
    return dt


def GetDataNow(nama):
    global now
    for i, x in enumerate(now["areas"]):
        if x["id"] == nama:
            return now["areas"][i]


def GetChart(idreg):
    global jsn, now
    # print(GetDataNow(idreg))
    tmpjsn = copy.deepcopy(jsn[idreg])
    dtNow = GetDataNow(idreg) if not idreg == "world" else now
    # dt = {
    #     "confirmed": [],
    #     "recovered": [],
    #     "deaths": [],
    #     "date": []
    # }
    # for i, x in enumerate(jsn[idreg]):
    #     dt["confirmed"].append(x["confirmed"])
    #     dt["recovered"].append(x["recovered"])
    #     dt["deaths"].append(x["fatal"])
    #     dt["date"].append(x["date"])
    tmpdt = {
        "confirmed": dtNow["totalConfirmed"],
        "fatal": dtNow["totalDeaths"],
        "recovered": dtNow["totalRecovered"],
        "date": dtNow["lastUpdated"],
    }
    tmpjsn.append(tmpdt)
    return {"data": tmpjsn}


def GetRegionCity(idreg):
    global now
    dtNow = copy.deepcopy(GetDataNow(
        idreg)) if not idreg == "world" else copy.deepcopy(now)
    if idreg == "world":
        for x in dtNow["areas"]:
            x["areas"] = []
    return dtNow


def GetNewsVideos(name):
    # sys.setrecursionlimit(10**6)
    # head = {
    #     "ept": "*/*",
    #     "accept-encoding": "gzip, deflate, br",
    #     "accept-language": "en-US,en;q=0.9",
    #     "authorization": token,
    #     "cookie": "_EDGE_S=F=1&SID=243ED1AEFC4C6E1426D3DF03FD876F36; _EDGE_V=1; MUID=2F0541A7A1F66C8B31FE4F0AA03D6DC0; SRCHD=AF=NOFORM; SRCHUID=V=2&GUID=849E5B4DAB6E48DBA2FC512AAB89C6C7&dmnchg=1; _SS=SID=243ED1AEFC4C6E1426D3DF03FD876F36; MUIDB=2F0541A7A1F66C8B31FE4F0AA03D6DC0; SRCHUSR=DOB=20200415&T=1586949644000; SRCHHPGUSR=WTS=63722546444; _clarity=42a86488a9d2450e9778dcec62658b9c",
    #     "referer": "https://bing.com/covid",
    #     "sec-fetch-dest": "empty",
    #     "sec-fetch-mode": "cors",
    #     "sec-fetch-site": "same-origin",
    #     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36 OPR/67.0.3575.130"
    # }
    head = {
        "Authorization": token,
        "Referer": "https://bing.com/covid",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 OPR/68.0.3618.142",
        "X-Search-Location": "lat:-6.1754;long:106.828;re:18000"
    }
    try:
        news = f"https://bing.com/covid/bingapi?ig={ig}&q=coronavirus {name}&api=news&count=20"
        videos = f"https://bing.com/covid/bingapi?ig={ig}&q=coronavirus {name}&api=videos&count=20"

        rqnews = requests.get(news, headers=head)
        rqvideos = requests.get(videos, headers=head, timeout=100)
    except Exception as e:
        print(e)
        rqnews = requests.get(news, headers=head, timeout=100)
        rqvideos = requests.get(videos, headers=head, timeout=100)
    jsnews = rqnews.json()
    jsnvideos = rqvideos.json()
    # print(jsnews["value"])
    # print(jsnvideos["value"])
    dt = {
        "news":jsnews["value"],
        "videos":jsnvideos["value"]
    }
    return dt
# print(GetRegionCity("world"))
# print(GetChart("indonesia"))
# print(GetRegion())
