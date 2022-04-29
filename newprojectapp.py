import pathlib
import pygubu
import tkinter as tk
import tkinter.ttk as ttk
from FER import analyze_face

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "newproject"


class NewprojectApp:
    def __init__(self, master=None):
        # build ui
        self.frame1 = ttk.Frame(master)
        self.button1 = ttk.Button(self.frame1)
        self.button1.configure(text='Browse')
        self.button1.place(anchor='nw', x='400', y='100')
        self.__tkvar = tk.StringVar(value='')
        __values = []
        self.optionmenu1 = tk.OptionMenu(self.frame1, self.__tkvar, None, *__values, command=None)
        self.optionmenu1.place(anchor='nw', x='50', y='80')
        self.frame1.configure(height='400', width='600')
        self.frame1.grid(column='0', row='0')

        # Main widget
        self.mainwindow = self.frame1
    
    def run(self):
        self.mainwindow.mainloop()


if __name__ == '__main__':
    root = tk.Tk()
    app = NewprojectApp(root)
    app.run()


