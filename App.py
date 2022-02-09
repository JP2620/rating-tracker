import tkinter as tk
import ttkbootstrap as ttk
import json


class App(ttk.Window):
    def __init__(self, master=None, **kwargs):
        super().__init__(master)
        try:
          with open('conf.json', 'r') as f:
              config = json.load(f)
        except Exception as e:
          print(e)
          exit()
        self.geometry(
            str(config["resolution"]["width"]) + "x" +
            str(config["resolution"]["height"])
        )
        self.resizable(False, False)
        self.title("Rating Tracker")
        self.set_icon('images/Table-Tennis-1.png')


    def set_icon(self, icon_path: str) -> None:
      self.iconphoto(False, tk.PhotoImage(file=icon_path))
      return