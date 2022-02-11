from PlayerForm import PlayerForm
from MatchForm import MatchForm
from DataView import DataView
from ActionMenu import ActionMenu
from typing import List
from datetime import datetime
import tkinter as tk
import sqlite3 as sql
import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.constants import *
from ttkbootstrap.tooltip import ToolTip
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
        self.actions = []
        self.actions_index = -1
        return

    def set_icon(self, icon_path: str) -> None:
        self.iconphoto(False, tk.PhotoImage(file=icon_path))
        return

    def create_widgets(self) -> None:
        self.player_form = PlayerForm(self, callback=lambda: self.callback_add_player
                                      (
                                          self.player_form.get_player(),
                                          self.player_form.get_rating()
                                      ),
                                      text="Agregar jugador")
        self.match_form = MatchForm(self, text="Agregar resultado",
                                    callbacks=[
                                        lambda: self.callback_add_match(
                                            self.match_form.get_player_1(),
                                            self.match_form.get_player_2(),
                                            self.match_form.get_sets_1(),
                                            self.match_form.get_sets_2(),
                                            self.match_form.get_modalidad()
                                        ),
                                        self.callback_show_deltas
                                    ])
        self.data_view = DataView(self)
        self.btns_frame = ActionMenu(self,
                                     callbacks=[
                                         self.callback_undo,
                                         self.callback_redo
                                     ])

        self.match_form.grid(row=0, column=0, sticky="EW",
                             padx=(20, 0), pady=10)
        self.player_form.grid(
            row=1, column=0, sticky="EW", padx=(20, 0), pady=10)
        self.data_view.grid(row=2, column=0, sticky="EW",
                            padx=(20, 0), pady=10)
        self.btns_frame.grid(row=0, column=1, rowspan=3,
                             padx=5, pady=10, sticky="N")

        self.match_form.update_player_opt(self.get_players())
        self.data_view.update_matches(self.get_matches())
        self.data_view.update_standings(self.get_standings())

        return

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
        Player1Rating INTEGER NOT NULL,
        Player2Rating INTEGER NOT NULL,
        Player1Score INTEGER NOT NULL,
        Player2Score INTEGER NOT NULL,
        Date TEXT,
        FOREIGN KEY(Player1Id) REFERENCES Player(PlayerId),
        FOREIGN KEY(Player2Id) REFERENCES Player(PlayerId)
      ); '''
                         )
        conn.commit()
        self.cur.close()
        return conn

    def callback_add_player(self, jug: str, rating: int) -> None:
        try:
            self.cur = self.conn.cursor()
            self.cur.execute('''
          INSERT INTO Player (Name, Rating)
          VALUES (?, ?)
          ''', (jug.upper(), int(rating)))
            self.conn.commit()
        except sql.Error as e:
            print(e)
            Messagebox.show_info(
                message="Fallo al agregar jugador", title="Error")
            return

        self.actions = self.actions[:self.actions_index + 1]
        self.actions.append(
            {
                "action": "add_player",
                "player": jug.upper(),
                "rating": int(rating)
            }
        )
        self.actions_index += 1
        self.data_view.update_standings(self.get_standings())

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

    def get_standings(self) -> List:
        self.cur.execute('''
        SELECT ROW_NUMBER() OVER(ORDER BY Rating DESC) AS Standing, Name, Rating
        FROM Player
        ''')
        standings = self.cur.fetchall()
        return standings

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

    def callback_add_match(self, jug1: str, jug2: str, sets_1: int, sets_2: int, modalidad: int) -> None:
        players = self.get_players()

        max_sets = modalidad // 2 + 1
        error_msg = ""
        if jug1 == jug2:
            error_msg = "Error: jugadores iguales"
        elif (sets_1 == sets_2):
            error_msg = "Error: sets iguales"
        elif (sets_1 < 0 or sets_2 < 0):
            error_msg = "Error: sets negativos"
        elif ((not (jug1 in players)) or (not (jug2 in players))):
            error_msg = "Error: jugadores no encontrados"
        elif (sets_1 > max_sets or sets_2 > max_sets):
            error_msg = "Error: cantidad de sets mayor a la permitida"
        elif (sets_1 != max_sets and sets_2 != max_sets):
            error_msg = "Error: Tienen que llegar a " + str(max_sets) + " sets"
        if error_msg != "":
            Messagebox.show_info(title="Error", message=error_msg)
            return

        self.cur.execute('''
            SELECT PlayerId, Name, Rating FROM Player
            WHERE Name = ? OR Name = ?
            ''', (jug1, jug2))
        players = self.cur.fetchall()
        jug1, jug2 = (players[0], players[1]) if players[0][1] == jug1 \
            else (players[1], players[0])

        time = datetime.now()
        self.cur.execute('''
            INSERT INTO Match (Player1Id, Player2Id, Player1Rating,
             Player2Rating, Player1Score, Player2Score, Date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (jug1[0], jug2[0], jug1[2], jug2[2], sets_1,
              sets_2, time))

        deltas = self.get_deltas(jug1[2], jug2[2], modalidad)
        new_rating1 = None
        new_rating2 = None
        if (sets_1 > sets_2):
            new_rating1 = jug1[2] + deltas[0][0]
            new_rating2 = jug2[2] + deltas[1][1]
        else:
            new_rating1 = jug1[2] + deltas[0][1]
            new_rating2 = jug2[2] + deltas[1][0]

        self.cur.execute('''
            UPDATE Player
            SET Rating = ?
            WHERE PlayerId = ?
        ''', (new_rating1, jug1[0]))
        self.cur.execute('''
            UPDATE Player
            SET Rating = ?
            WHERE PlayerId = ?
        ''', (new_rating2, jug2[0]))

        self.conn.commit()
        self.data_view.update_standings(self.get_standings())
        self.data_view.update_matches(self.get_matches())
        self.actions = self.actions[:self.actions_index + 1]
        self.actions.append(
            {
                "action": "add_match",
                "match": self.cur.lastrowid,
                "jug1": jug1[0],
                "jug2": jug2[0],
                "jug1_name": jug1[1],
                "jug2_name": jug2[1],
                "sets_1": sets_1,
                "sets_2": sets_2,
                "old_rating1": jug1[2],
                "old_rating2": jug2[2],
                "new_rating1": new_rating1,
                "new_rating2": new_rating2,
                "time": time
            }
        )
        self.actions_index += 1
        return

    def get_matches(self) -> List:
        self.cur.execute('''
        SELECT t2.JUG1, t2.SETS1 || " - " || t2.SETS2 AS RESULTADO, t2.JUG2
        FROM
        (
        	(
        	SELECT Match.MatchId, Player.Name as JUG1, Match.Player1Score AS SETS1  
        	FROM 
        	(
        		Match JOIN Player
        		ON Match.Player1Id = Player.PlayerId
        	)
        	)
        	AS t0
        	JOIN
        	(
        	SELECT Match.MatchId, Player.Name AS JUG2, Match.Player2Score AS SETS2
        	FROM
        	(
        		Match JOIN Player
        		ON Match.Player2Id = Player.PlayerId
        	)
        	)
        	AS t1
        	ON t0.MatchId = t1.MatchId
        ) AS t2
        ''')
        matches = self.cur.fetchall()
        matches.reverse()   # Most recent first
        return matches

    def callback_undo(self) -> None:
        if self.actions_index < 0:
            return
        last_action = self.actions[self.actions_index]
        if last_action["action"] == "add_match":
            try:
                self.cur.execute('''
                    SELECT Player1Id, Player1Rating, Player2Id, Player2Rating
                    FROM Match
                    WHERE MatchId = ?
                ''', (last_action["match"],))

                old_ratings = self.cur.fetchone()

                self.cur.execute('''
                    UPDATE Player
                    SET Rating = CASE PlayerId
                        WHEN ? THEN ?
                        WHEN ? THEN ?
                        ELSE Rating
                    END
                ''', (old_ratings[0], old_ratings[1], old_ratings[2], old_ratings[3]))

                self.cur.execute('''
                    DELETE FROM Match
                    WHERE MatchId = ?
                ''', (last_action["match"],))
            except sql as e:
                print(e)
            except Exception as e:
                print(e)
        elif last_action["action"] == "add_player":
            try:
                self.cur.execute('''
                    DELETE FROM Player
                    WHERE Name = ?
                ''', (last_action["player"],))
            except sql.Error as e:
                print(e)
            except Exception as e:
                print(e)

        self.conn.commit()
        self.data_view.update_standings(self.get_standings())
        self.data_view.update_matches(self.get_matches())
        self.actions_index -= 1
        return

    def callback_redo(self) -> None:
        if self.actions_index >= len(self.actions) - 1:
            return
        next_action = self.actions[self.actions_index + 1]

        if next_action["action"] == "add_player":
            self.cur.execute('''
                INSERT INTO Player (Name, Rating)
                VALUES (?, ?)
            ''', (next_action["player"], next_action["rating"]))
            self.conn.commit()
        elif next_action["action"] == "add_match":
            try:
                self.cur.execute('''
                    SELECT PlayerId
                    FROM Player
                    WHERE Name = ?
                ''', (next_action["jug1_name"],))
                jug1 = self.cur.fetchone()[0]
                self.cur.execute('''
                    SELECT PlayerId
                    FROM Player
                    WHERE Name = ?
                ''', (next_action["jug2_name"],))
                jug2 = self.cur.fetchone()[0]

                self.cur.execute('''
                    INSERT INTO Match (Player1Id, Player1Rating, Player2Id, Player2Rating, Player1Score, Player2Score, Date)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (jug1, next_action["old_rating1"], jug2, next_action["old_rating2"],
                      next_action["sets_1"], next_action["sets_2"], next_action["time"]))
                self.cur.execute('''
                    UPDATE Player
                    SET Rating = CASE PlayerId
                        WHEN ? THEN ?
                        WHEN ? THEN ?
                        ELSE Rating
                    END
                ''', (jug1, next_action["new_rating1"], jug2, next_action["new_rating2"]))
                self.conn.commit()
                self.actions[self.actions_index + 1]["match"] = self.cur.lastrowid

            except sql.Error as e:
                print(e.with_traceback())
                print(e)


        self.data_view.update_standings(self.get_standings())
        self.data_view.update_matches(self.get_matches())
        self.actions_index += 1
        return
