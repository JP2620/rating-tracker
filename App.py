from PlayerForm import PlayerForm
from MatchForm import MatchForm
from DataView import DataView
from typing import List
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
        self.MULTIPLICADORES = config["multipliers"]
        self.DIFF_RATINGS = config["rating_deltas"]
        self.PTS_GANA_MEJOR = config["points_better_wins"]
        self.PTS_GANA_PEOR = config["points_worse_wins"]
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
        self.match_form = MatchForm(self, text="Agregar resultado",
                                    callbacks=[
                                        lambda: print("Partido agregado"),
                                        self.callback_show_deltas
                                    ])
        self.data_view = DataView(self, conn=self.conn)
        self.data_view.update_standings()
        self.match_form.grid(row=0, column=0, sticky="EW")
        self.player_form.grid(row=1, column=0, sticky="EW")
        self.data_view.grid(row=2, column=0, sticky="EW")

        self.match_form.update_player_opt(self.get_players())

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

    def callback_add_player(self) -> None:
        try:
            self.cur = self.conn.cursor()
            self.cur.execute('''
          INSERT INTO Player (Name, Rating)
          VALUES (?, ?)
          ''', (self.player_form.get_player().upper(), self.player_form.get_rating()))
            self.conn.commit()
        except sql.Error as e:
            print(e)
            return
        self.data_view.update_standings()

        try:
            self.match_form.update_player_opt(self.get_players())
        except:
            pass
        return

    def get_deltas(self, rating_jug_1: int, rating_jug_2: int, sets_a_jugar: int) -> List[tuple]:
        """
          retorna dos tuplas con los delta de victoria/derrota de cada
          jugador
        """
        mejor = 0
        peor = 0
        if rating_jug_1 >= rating_jug_2:
            mejor = rating_jug_1
            peor = rating_jug_2
        else:
            mejor = rating_jug_2
            peor = rating_jug_1

        diff = mejor - peor

        # Quiero el indice del numero mas grande de los menores/iguales a diff
        indice = -1
        for item in self.DIFF_RATINGS:
            if diff >= item:
                indice = self.DIFF_RATINGS.index(item)
                break

        # Ajusta delta segun modalidad
        modalidad = "Mejor de " + str(sets_a_jugar)
        PTS_GANA_MEJOR_aux = [int(puntaje * self.MULTIPLICADORES[modalidad])
                              for puntaje in self.PTS_GANA_MEJOR]
        PTS_GANA_PEOR_aux = [int(puntaje * self.MULTIPLICADORES[modalidad])
                             for puntaje in self.PTS_GANA_PEOR]

        if (mejor == rating_jug_1):
            return [(PTS_GANA_MEJOR_aux[indice], -PTS_GANA_PEOR_aux[indice]),
                    (PTS_GANA_PEOR_aux[indice], -PTS_GANA_MEJOR_aux[indice])]
        else:
            return [(PTS_GANA_PEOR_aux[indice], -PTS_GANA_MEJOR_aux[indice]),
                    (PTS_GANA_MEJOR_aux[indice], -PTS_GANA_PEOR_aux[indice])]
    
    def get_players(self) -> List[str]:
        try:
            self.cur.execute(
                '''
                SELECT Name FROM Player
                '''
            )
        except sql.Error as e:
            print(e)
            raise e
        except Exception as e:
            print(e)
            raise e
        return [x[0] for x in self.cur.fetchall()]

    def callback_show_deltas(self) -> None:
        jug1 = self.match_form.get_player_1()
        jug2 = self.match_form.get_player_2()
        self.cur.execute('''
          SELECT Name, Rating FROM Player
          WHERE Name = ? OR Name = ?
          ''', (jug1, jug2))
        players = self.cur.fetchall()
        if len(players) != 2:
            print("Error: jugadores no encontrados")
            return
        deltas = None
        if players[0][0] == jug1:
            deltas = self.get_deltas(players[0][1], players[1][1],
                                     self.match_form.get_modalidad())
        else:
            deltas = self.get_deltas(players[1][1], players[0][1],
                                     self.match_form.get_modalidad())

        self.match_form.set_deltas(
            "+" + str(deltas[0][0]) + "/" + str(deltas[0][1]),
            "+" + str(deltas[1][0]) + "/" + str(deltas[1][1]))
        return
