import tkinter as tk

WIN_X = 1024
WIN_Y = 600
WIN_GEOMETRY = "{}x{}".format(WIN_X, WIN_Y)
X_DIVIDE_block = WIN_X / 10
Y_DIVIDE_block = WIN_Y / 3

class Application(tk.Frame):
    def __init__(self,master):
        super().__init__(master, bg="black")
        self.pack(anchor=tk.NW) #左寄せ

        self.master.geometry(WIN_GEOMETRY)
        self.master.title("Watch")

        self.create_widgets()

    def create_widgets(self):
        watch_frame = tk.Frame(self, bg="white", width=8*X_DIVIDE_block, height=2*Y_DIVIDE_block, bd=0, relief="flat")
        watch_frame.pack()

        weather_frame = tk.Frame(self, bg="blue", width=8*X_DIVIDE_block, height=Y_DIVIDE_block, bd=0, relief="flat")
        weather_frame.pack()

        temp_frame = tk.Frame(self, bg="red", width=2*X_DIVIDE_block, height=Y_DIVIDE_block, bd=0, relief="flat")
        temp_frame.pack()

    def callBack(self):
        pass

def main():
    root = tk.Tk()
    app = Application(master=root)  #Inherit
    app.mainloop()

if __name__ == "__main__":
    main()    