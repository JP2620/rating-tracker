import sqlite3 as sql
from typing import List
from constants import *


class Model():
    def __init__(self):
        try:
            self.conn = sql.connect('liga.db')
            self.cur = self.conn.cursor()
        except sql.Error as e:
            print(e)
            exit()
        return

    def create_database(self) -> sql.Connection:
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS Player (
                PlayerId INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT NOT NULL,
                Rating INTEGER NOT NULL,
                UNIQUE(Name)
            ) 
        """)
        self.cur.execute("""
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
                )
                """)
        self.conn.commit()
        return self.conn

    def get_players(self) -> List:
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
        for item in DIFF_RATINGS:
            if diff >= item:
                indice = DIFF_RATINGS.index(item)
                break

        # Ajusta delta segun modalidad
        modalidad = "Mejor de " + str(sets_a_jugar)
        PTS_GANA_MEJOR_aux = [int(puntaje * MULTIPLICADORES[modalidad])
                              for puntaje in PTS_GANA_MEJOR]
        PTS_GANA_PEOR_aux = [int(puntaje * MULTIPLICADORES[modalidad])
                             for puntaje in PTS_GANA_PEOR]

        if (mejor == rating_jug_1):
            return [(PTS_GANA_MEJOR_aux[indice], -PTS_GANA_PEOR_aux[indice]),
                    (PTS_GANA_PEOR_aux[indice], -PTS_GANA_MEJOR_aux[indice])]
        else:
            return [(PTS_GANA_PEOR_aux[indice], -PTS_GANA_MEJOR_aux[indice]),
                    (PTS_GANA_MEJOR_aux[indice], -PTS_GANA_PEOR_aux[indice])]