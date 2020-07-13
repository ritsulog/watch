#!/usr/bin/env python
# coding: utf-8

# watch_base

# In[1]:



#Library

from tkinter import *
from datetime import datetime
from PIL import Image,ImageTk
import json
import pprint
import get_weather


# In[2]:


def weather_img_set(weather):
    """
    天気と画像の同期
    weater(天気)を引数として受け取り、その天気の画像を返す。
    """
    
    if "晴" in weather:
        img = ImageTk.PhotoImage(file="weather/w_sunny.png")
    elif "曇" in weather:
        img = ImageTk.PhotoImage(file="weather/w_cloudy.png")
    elif "雨" in weather:
        img = ImageTk.PhotoImage(file="weather/w_rainy.png")
    elif "雪" in weather:
        img = ImageTk.PhotoImage(file="weather/w_snowy.png")
    
    return img


# In[3]:


def weather_update(hour):
    """
    天気の更新(一時間ごとに実施)
    hour(現在時間)を引数とし、3時間おきの時間、天気、画像を取得し、
    画面を更新
    """
    #list初期化
    weather_img_list.clear()
    
    #辞書から現在時間のデータの場所を取得。
    for f in forecasts:
        if f["hour"] == hour:
            f_index = forecasts.index(f)
            break
    #画面の更新
#     for canvas_img in canvas_img_list:
#         #指定時刻の天気の画像を代入
#         img = weather_img_set(forecasts[f_index]["weather"])
#         #画像をリストに追加(GC対策)
#         weather_img_list.append(img)
#         #天気画像の更新
#         canvas.itemconfigure(canvas_img, image=img)
#         #辞書を3個進める(3時間後)
#         f_index += 3
        
    for i in range(0,8):
        #指定時刻の天気の画像を代入
        img = weather_img_set(forecasts[f_index]["weather"])
        t_int = (int)(forecasts[f_index]["hour"])
        t_text = "{0}時".format(t_int)
        w_text = forecasts[f_index]["weather"]
        #画像をリストに追加(GC対策)
        weather_img_list.append(img)
        #天気画像の更新
        canvas.itemconfigure(canvas_time_list[i], text=t_text)
        canvas.itemconfigure(canvas_img_list[i], image=img)
        canvas.itemconfigure(canvas_weather_list[i], text=w_text)
        #辞書を3個進める(3時間後)
        f_index += 3
    
    #温度
    hum_sum = 0
    for i in range(0,24):
        temp = (float)(forecasts[i]["temperature"])
        hum = (int)(forecasts[i]["humidity"])
        if i == 0:
            t_max = temp
            t_min = temp
        if temp > t_max:
            t_max = temp
        if temp < t_min:
            t_min = temp
        hum_sum += hum
    temp_max_text = "{0}℃".format(t_max)
    temp_min_text = "{0}℃".format(t_min)
    hum_ave = (int)(hum_sum/24)
    hum_ave_text = "{0}%".format(hum_ave)
    
    canvas.itemconfigure(temp_max, text=temp_max_text)
    canvas.itemconfigure(temp_min, text=temp_min_text)
    canvas.itemconfigure(canvas_hum, text=hum_ave_text)
    


# In[4]:


def cupdate():
    """
    現在時刻を更新
    """
    #現在時刻取得
    now = datetime.now()
    #年月日(曜)をフォーマット
    d = "{0:0>4d}/{1:0>2d}/{2:0>2d} ({3}.)".format(now.year, now.month, now.day, now.strftime("%a"))
    #現在時間をフォーマット
    t = "{0:0>2d}:{1:0>2d}:{2:0>2d}".format(now.hour, now.minute, now.second)
    
    global time_flag
    
    #hourが変わったとき/flag変更
    if now.minute == 0 and (now.second == 0 or now.second == 1):
        if now.second == 0 and time_flag == 0:
            #天気を更新
            weather_update("{0:0>2d}".format(now.hour))
            #time_flag更新
            time_flag = 1
            
        elif now.second == 1 and time_flag == 1:
            if now.hour == 0:
                get_weather.main('https://tenki.jp/forecast/3/14/4310/11237/1hour.html')
            time_flag = 0

    #時間更新
    canvas.itemconfigure(cd, text=d)
    canvas.itemconfigure(ct, text=t)
    canvas.update()

    #1秒間隔で繰り返す
    root.after(100,cupdate)


# In[5]:


#def main():
#ウィンドウ作成
root = Tk()
root.title("watch") #title
root.geometry("1024x600") #size

#Canvas作成
canvas = Canvas(root, bg="#000", width=1024, height=600)
#オプション設定
canvas.pack(expand=True, fill=BOTH)
#更新。winfo_xxが反映されないため。
root.update_idletasks()

#x軸長さ
win_x_max = root.winfo_width()

#y軸長さ
win_y_max = root.winfo_height()

#線描画

#時計と天気の間の線
line_y1 = (win_y_max / 3 * 2)
canvas.create_line(0,line_y1,win_x_max,line_y1, fill="white")
#時計と温度・湿度の間の線
line_x1 = (win_x_max / 10 * 8)
canvas.create_line(line_x1,0,line_x1,win_y_max, fill="white")

#天気欄の境界線
line_x2 = (int)(win_x_max / 10)
for w_line_x in range(line_x2,line_x2 * 8,line_x2) :
    canvas.create_line(w_line_x,line_y1,w_line_x,win_y_max, fill="white")
    
#温度・湿度の境界線
line_y2 = (win_y_max / 3)
canvas.create_line(line_x1,line_y2,win_x_max,line_y2, fill="white")


#cd->Canvas Day
#ct->Canvas Time
#fill->内部の色,outline->枠の色,font=("",大きさ,""bold"->太さ)
cd = canvas.create_text(50, 50, font=("", 50,"bold"), fill="white",anchor="nw")
ct = canvas.create_text(100, 150, font=("", 130,"bold"), fill="white",anchor="nw")

#forecast_test

#json_load
with open("forecast.json") as f:
    fore_dict = json.load(f)

#天気画面作成
png_x = 0
text_x = win_x_max / 20

#時間用リスト
canvas_time_list = []
#画像用リスト
canvas_img_list = []
#天気テキスト用リスト
canvas_weather_list = []

for i in range(0,8):
    canvas_time_list.append(canvas.create_text(text_x,425, font=("", 20), fill="white",anchor="center"))
    canvas_img_list.append(canvas.create_image(png_x,450,anchor="nw"))
    canvas_weather_list.append(canvas.create_text(text_x,575, font=("", 20), fill="white",anchor="center"))
    png_x += (int)(win_x_max / 10)
    text_x = png_x + (int)(win_x_max / 20)

#温度
temp_x = (line_x1 + win_x_max) / 2
temp_y1 = line_y2 / 2
temp_y2 = line_y2 + temp_y1
hum_y = line_y1 + temp_y1
temp_max = canvas.create_text(temp_x,temp_y1, font=("", 50,"bold"), fill="red",anchor="center")
temp_min = canvas.create_text(temp_x,temp_y2, font=("", 50,"bold"), fill="blue",anchor="center")
canvas_hum = canvas.create_text(temp_x,hum_y, font=("", 50,"bold"), fill="white",anchor="center")

#png貼り付け
forecasts = fore_dict["forecasts"]

#天気更新初回
weather_img_list = []
weather_update("{0:0>2d}".format(datetime.now().hour))
print("a")

time_flag = 0

#常に最前面に表示
root.attributes("-topmost", True)

#コールバック関数を登録
root.after(100, cupdate)

#ウィンドウを動かす
root.mainloop()


# In[6]:


# if __name__ == '__main__':
#     main()

