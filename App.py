from PlayerForm import PlayerForm
from MatchForm import MatchForm
from DataView import DataView
import tkinter as tk
import ttkbootstrap as ttk
import json


class App(ttk.Window):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
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
        self.create_widgets()


    def set_icon(self, icon_path: str) -> None:
      self.iconphoto(False, tk.PhotoImage(file=icon_path))
      return
    
    def create_widgets(self) -> None:
      self.player_form = PlayerForm(self, lambda: print("Jugador agregado"), text="Agregar jugador")
      self.match_form = MatchForm(self, lambda: print("Partida agregada"), text="Agregar resultado")
      self.data_view = DataView(self)
      self.match_form.grid(row=0, column=0, sticky="EW")
      self.player_form.grid(row=1, column=0, sticky="EW")
      self.data_view.grid(row=2, column=0, sticky="EW")