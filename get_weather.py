#!/usr/bin/env python
# coding: utf-8

# Request -> HTTPライブラリでwebページを取得<br>
# Beautiful soup -> HTMLから情報をスクレイピング

# In[1]:


import re
import requests
from bs4 import BeautifulSoup
import json
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import json


# In[2]:


def main(url):
    # soup関数呼び出し
    s = soup(url)

    #辞書dict
    f_dict = {}

    # 予測地点
    #正規表現。. -> 改行以外の文字。r -> エスケープ無効。+ -> 前の文字が1つ以上
    l_pattern = r"(.+)の1時間天気"
    #htmlのtitle
    l_src = s.title.text
    
    #l_patternとl_srcの一致する文字列を代入(ここでは市名)
    f_dict['location'] = re.findall(l_pattern, l_src)[0]
    #print(f_dict['location'] + "の天気")

    #s.find() -> 最初に合致した結果を返す
    soup_tdy = s.find(id='forecast-point-1h-today')
    soup_tmr = s.find(id='forecast-point-1h-tomorrow')
    #明後日。今回は使わんな
    #soup_dat = s.find(id='forecast-point-1h-dayaftertomorrow')

    data["forecasts"] = []
    forecast2dict(soup_tdy)
    forecast2dict(soup_tmr)
    #
    #f_dict["today"] = forecast2dict(soup_tdy)
    #f_dict["tomorrow"] = forecast2dict(soup_tmr)
    #dict["dayaftertomorrow"] = forecast2dict(soup_dat)

    # JSON形式で出力
    #print(json.dumps(dict, ensure_ascii=False))
    
    #jsonファイルを書き込み権限でオープン
    json_file = open("forecast.json", "w")
    
    json.dump(data, json_file, indent=2,ensure_ascii=False)

def soup(url):
    """html読み込み+BeautifulSoupにセット"""
    r = requests.get(url)
    #r.text -> htmlのコード。r.encoding -> 文字コード(UTF-8)
    #bite列変換
    html = r.text.encode(r.encoding)
    #BSにhtmlと解析器をセット
    #lxml -> C言語の高速実装な解析器。複雑な構造や動的なものに弱い
    return BeautifulSoup(html, 'lxml')

def forecast2dict(soup):
    #辞書data

    # 日付処理
    d_pattern = r"(\d+)年(\d+)月(\d+)日"
    #soup.select -> cssセレクタでタグを探す。今回はclass=head以下のpタグ
    d_src = soup.select('.head p')
    date = re.findall(d_pattern, d_src[0].text)[0]
    #data["date"] = "%s-%s-%s" % (date[0], date[1], date[2])
    #print("=====" + data["date"] + "=====")

    # 一時間ごとのデータ
    ## 取得 class=.*直下のtd全て
    hour          = soup.select('.hour > td')
    weather       = soup.select('.weather > td')
    temperature   = soup.select('.temperature > td')
    prob_precip   = soup.select('.prob-precip > td')
    #precipitation = soup.select('.precipitation > td')
    humidity      = soup.select('.humidity > td')
    #wind_blow     = soup.select('.wind-blow > td')
    #wind_speed    = soup.select('.wind-speed > td')

    ## 格納
    #data["forecasts"] = []
    for itr in range(0, 24):
        forecast = {}
        if hour[itr].text.strip() == "24":
            forecast["hour"] = "00"
        else:
            forecast["hour"] = hour[itr].text.strip()
        forecast["weather"] = weather[itr].text.strip()
        forecast["temperature"] = temperature[itr].text.strip()
        forecast["prob-precip"] = prob_precip[itr].text.strip()
        #forecast["precipitation"] = precipitation[itr].text.strip()
        forecast["humidity"] = humidity[itr].text.strip()
        #forecast["wind-blow"] = wind_blow[itr].text.strip()
        #forecast["wind-speed"] = wind_speed[itr].text.strip()
        
        #画像
        #forecast["png"] = weather_png(forecast["weather"])
        
        data["forecasts"].append(forecast)

#         print(
#             "時刻         ： " + forecast["hour"] + "時" + "\n"
#             "天気         ： " + forecast["weather"] + "\n"
#             "気温(C)      ： " + forecast["temperature"] + "\n"
#             "降水確率(%)  ： " + forecast["prob-precip"] + "\n"
#             #"降水量(mm/h) ： " + forecast["precipitation"] + "\n"
#             "湿度(%)      ： " + forecast["humidity"] + "\n"
#             #"風向         ： " + forecast["wind-blow"] + "\n"
#             #"風速(m/s)    ： " + forecast["weather"] + "\n"
#         )
        #貼り付け
        #plt.imshow(np.array(forecast["png"]))
        #表示
        #plt.show()

    #return data

# def weather_png(weather):
    
#     if "晴" in weather:
#         img = Image.open("w_sunny.png")
#     elif "曇" in weather:
#         img = Image.open("w_cloudy.png")
#     elif "雨" in weather:
#         img = Image.open("w_rainy.png")
#     elif "雪" in weather:
#         img = Image.open("w_snowy.png")
    
#     return img


# In[3]:


if __name__ == '__main__':
    # 三郷市の一時間ごとの気象情報URL
    URL = 'https://tenki.jp/forecast/3/14/4310/11237/1hour.html'
    data = {}
    main(URL)
data = {}


# In[ ]:




