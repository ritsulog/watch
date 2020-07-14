from tkinter import * 
import tkinter as tk
from datetime import datetime
from PIL import Image,ImageTk
import json
import pprint
import get_weather


#X_DIVIDE_block = WIN_X / 10
#Y_DIVIDE_block = WIN_Y / 3

class Application(tk.Frame):
    def __init__(self,master):
        super().__init__(master, bg="black")
        self.pack(anchor=tk.NW) #左寄せ

        self.WIN_X = 1024
        self.WIN_Y = 600
        self.WIN_GEOMETRY = "{}x{}".format(self.WIN_X, self.WIN_Y)

        self.master.geometry(self.WIN_GEOMETRY)
        self.master.title("Watch")


        self.load_weather()
        self.create_initial_widgets()

        #常に最前面に表示
        self.master.attributes("-topmost", True)

        #コールバック関数を登録
        self.after(100, self.cupdate)

    def load_weather(self):
        with open("forecast.json") as f:
            self.fore_dict = json.load(f)

    def create_initial_widgets(self):  
        #Canvas作成
        self.canvas = Canvas(self, bg="#000", width=1024, height=600)
        #オプション設定
        self.canvas.pack(expand=True, fill=BOTH)
        #更新。winfo_xxが反映されないため。
        self.update_idletasks()

        #時計と天気の間の線
        line_y1 = (self.WIN_Y / 3 * 2)
        self.canvas.create_line(0,line_y1,self.WIN_X,line_y1, fill="white")
        #時計と温度・湿度の間の線
        line_x1 = (self.WIN_X / 10 * 8)
        self.canvas.create_line(line_x1,0,line_x1,self.WIN_Y, fill="white")

        #天気欄の境界線
        line_x2 = (int)(self.WIN_X / 10)
        for w_line_x in range(line_x2,line_x2 * 8,line_x2) :
            self.canvas.create_line(w_line_x,line_y1,w_line_x,self.WIN_Y, fill="white")
            
        #温度・湿度の境界線
        line_y2 = (self.WIN_Y / 3)
        self.canvas.create_line(line_x1,line_y2,self.WIN_X,line_y2, fill="white")

        #cd->Canvas Day
        #ct->Canvas Time
        #fill->内部の色,outline->枠の色,font=("",大きさ,""bold"->太さ)
        self.cd = self.canvas.create_text(50, 50, font=("", 50,"bold"), fill="white",anchor="nw")
        self.ct = self.canvas.create_text(100, 150, font=("", 130,"bold"), fill="white",anchor="nw")

        #天気画面作成
        png_x = 0
        text_x = self.WIN_X / 20

        #時間用リスト
        self.canvas_time_list = []
        #画像用リスト
        self.canvas_img_list = []
        #天気テキスト用リスト
        self.canvas_weather_list = []

        for i in range(0,8):
            self.canvas_time_list.append(self.canvas.create_text(text_x,425, font=("", 20), fill="white",anchor="center"))
            self.canvas_img_list.append(self.canvas.create_image(png_x,450,anchor="nw"))
            self.canvas_weather_list.append(self.canvas.create_text(text_x,575, font=("", 20), fill="white",anchor="center"))
            png_x += (int)(self.WIN_X / 10)
            text_x = png_x + (int)(self.WIN_X / 20)

        #温度
        temp_x = (line_x1 + self.WIN_X) / 2
        temp_y1 = line_y2 / 2
        temp_y2 = line_y2 + temp_y1
        hum_y = line_y1 + temp_y1
        self.temp_max = self.canvas.create_text(temp_x,temp_y1, font=("", 50,"bold"), fill="red",anchor="center")
        self.temp_min = self.canvas.create_text(temp_x,temp_y2, font=("", 50,"bold"), fill="blue",anchor="center")
        self.canvas_hum = self.canvas.create_text(temp_x,hum_y, font=("", 50,"bold"), fill="white",anchor="center")

        #png貼り付け
        self.forecasts = self.fore_dict["forecasts"]

        #天気更新初回
        self.weather_img_list = []
        self.weather_update("{0:0>2d}".format(datetime.now().hour))
        print("a")

        self.time_flag = 0

    def weather_img_set(self,weather):
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

    def weather_update(self,hour):
        """
        天気の更新(一時間ごとに実施)
        hour(現在時間)を引数とし、3時間おきの時間、天気、画像を取得し、
        画面を更新
        """
        #list初期化
        self.weather_img_list.clear()
        
        #辞書から現在時間のデータの場所を取得。
        for f in self.forecasts:
            if f["hour"] == hour:
                f_index = self.forecasts.index(f)
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
            img = self.weather_img_set(self.forecasts[f_index]["weather"])
            t_int = (int)(self.forecasts[f_index]["hour"])
            t_text = "{0}時".format(t_int)
            w_text = self.forecasts[f_index]["weather"]
            #画像をリストに追加(GC対策)
            self.weather_img_list.append(img)
            #天気画像の更新
            self.canvas.itemconfigure(self.canvas_time_list[i], text=t_text)
            self.canvas.itemconfigure(self.canvas_img_list[i], image=img)
            self.canvas.itemconfigure(self.canvas_weather_list[i], text=w_text)
            #辞書を3個進める(3時間後)
            f_index += 3
        
        #温度
        hum_sum = 0
        for i in range(0,24):
            temp = (float)(self.forecasts[i]["temperature"])
            hum = (int)(self.forecasts[i]["humidity"])
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
        
        self.canvas.itemconfigure(self.temp_max, text=temp_max_text)
        self.canvas.itemconfigure(self.temp_min, text=temp_min_text)
        self.canvas.itemconfigure(self.canvas_hum, text=hum_ave_text)

    def cupdate(self):
        """
        現在時刻を更新
        """
        #現在時刻取得
        now = datetime.now()
        #年月日(曜)をフォーマット
        d = "{0:0>4d}/{1:0>2d}/{2:0>2d} ({3}.)".format(now.year, now.month, now.day, now.strftime("%a"))
        #現在時間をフォーマット
        t = "{0:0>2d}:{1:0>2d}:{2:0>2d}".format(now.hour, now.minute, now.second)
        
        #hourが変わったとき/flag変更
        if now.minute == 0 and (now.second == 0 or now.second == 1):
            if now.second == 0 and self.time_flag == 0:
                #天気を更新
                self.weather_update("{0:0>2d}".format(now.hour))
                #time_flag更新
                self.time_flag = 1
                
            elif now.second == 1 and self.time_flag == 1:
                if now.hour == 0:
                    get_weather.main('https://tenki.jp/forecast/3/14/4310/11237/1hour.html')
                self.time_flag = 0

        #時間更新
        self.canvas.itemconfigure(self.cd, text=d)
        self.canvas.itemconfigure(self.ct, text=t)
        self.canvas.update()

        #1秒間隔で繰り返す
        self.after(100,self.cupdate)


def main():
    root = tk.Tk()
    app = Application(master=root)  #Inherit
    app.mainloop()

if __name__ == "__main__":
    main()    