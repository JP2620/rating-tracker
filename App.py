from PlayerForm import PlayerForm
from MatchForm import MatchForm
from DataView import DataView
import tkinter as tk
import sqlite3 as sql
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
        self.conn = self.create_database()
        self.cur = self.conn.cursor()
        self.create_widgets()

    def set_icon(self, icon_path: str) -> None:
        self.iconphoto(False, tk.PhotoImage(file=icon_path))
        return

    def create_widgets(self) -> None:
        self.player_form = PlayerForm(self, callback=self.callback_add_player,
                                      text="Agregar jugador")
        self.match_form = MatchForm(self, lambda: print(
            "Partida agregada"), text="Agregar resultado")
        self.data_view = DataView(self, conn=self.conn)
        self.data_view.update_standings()
        self.match_form.grid(row=0, column=0, sticky="EW")
        self.player_form.grid(row=1, column=0, sticky="EW")
        self.data_view.grid(row=2, column=0, sticky="EW")

    def create_database(self) -> sql.Connection:
        conn = None
        try:
            conn = sql.connect('torneo.db')
            self.cur = conn.cursor()
        except Error as e:
            print(e)
            exit()
        self.cur.execute('''
      CREATE TABLE IF NOT EXISTS Player (
        PlayerId INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        Rating INTEGER NOT NULL,
        UNIQUE(Name)
      ); '''
                    )
        self.cur.execute('''
      CREATE TABLE IF NOT EXISTS Match (
        MatchId INTEGER PRIMARY KEY AUTOINCREMENT,
        Player1Id INTEGER NOT NULL,
        Player2Id INTEGER NOT NULL,
        Player1Score INTEGER NOT NULL,
        Player2Score INTEGER NOT NULL,
        Date TEXT NOT NULL,
        FOREIGN KEY(Player1Id) REFERENCES Player(PlayerId),
        FOREIGN KEY(Player2Id) REFERENCES Player(PlayerId)
      ); '''
                    )
        conn.commit()
        self.cur.close()
        return conn

    def callback_add_player(self):
        try:
            self.cur = self.conn.cursor()
            self.cur.execute('''
          INSERT INTO Player (Name, Rating)
          VALUES (?, ?)
          ''', (self.player_form.get_player(), self.player_form.get_rating()))
            self.conn.commit()
        except sql.Error as e:
            print(e)
            return
        self.data_view.update_standings()

        try:
            self.cur = self.conn.cursor()
            self.cur.execute('''
          SELECT Name FROM Player
          ''')
            players = list(self.cur.fetchall())
            self.match_form.update_player_opt(players)
        except sql.Error as e:
            print(e)
            return
        except Exception as e:
            print(e)
            return
        return
