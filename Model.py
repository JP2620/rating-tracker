import sqlite3 as sql
import pandas as pd
import traceback
from typing import List
from constants import *


class Model():
    def __init__(self):
        try:
            self.conn = sql.connect('ligatest2.db')
            self.cur = self.conn.cursor()
            self.create_database()
        except sql.Error as e:
            print(traceback.format_exc())
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
        self.save_changes()
        return self.conn

    def get_players(self) -> pd.DataFrame:
        try:
            query = pd.read_sql_query(
                '''
                SELECT PlayerId, Name, Rating
                FROM Player
                ORDER BY Rating DESC
                ''', self.conn
            )
            df = pd.DataFrame(query, columns=['PlayerId', 'Name', 'Rating'])
        except sql.Error as e:
            print(traceback.format_exc())
            raise e
        except Exception as e:
            print(traceback.format_exc())
            raise e
        return df

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
                    Match JOIN Player
                    ON Match.Player1Id = Player.PlayerId                    
            ) AS t0
            JOIN
            (
                SELECT Match.MatchId, Player.Name AS JUG2, Match.Player2Score AS SETS2
                FROM
                    Match JOIN Player
                    ON Match.Player2Id = Player.PlayerId
            ) AS t1 ON t0.MatchId = t1.MatchId
        ) AS t2
        ''')
        matches = self.cur.fetchall()
        matches.reverse()   # Most recent first
        return matches

    def get_deltas(self, rating_jug_1: int, rating_jug_2: int, sets_a_jugar: int) -> List[tuple]:
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

    def add_player(self, name: str, rating: int, id=None) -> int:
        try:
            self.cur.execute('''
            INSERT INTO Player (PlayerId, Name, Rating)
            VALUES (?, ?, ?)
            ''', (id, name, rating))

        except sql.Error as e:
            raise e
        return self.cur.lastrowid

    def add_match(self, p1_id: int, p2_id: int, p1_rating: int, p2_rating: int,
                  p1_score: int, p2_score: int, date) -> int:
        try:
            self.cur.execute('''
            INSERT INTO Match (Player1Id, Player2Id, Player1Rating, Player2Rating, Player1Score, Player2Score, Date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (p1_id, p2_id, p1_rating, p2_rating, p1_score, p2_score, date))
        except sql.Error as e:
            raise e
        return self.cur.lastrowid

    def update_player(self, fields: List[str], values: List, player_id: int) -> None:
        try:
            update_str = "UPDATE Player SET "
            for i in range(len(fields)):
                update_str += fields[i] + " = '" + str(values[i]) + "'"
                if i < len(fields) - 1:
                    update_str += ", "
            update_str += " WHERE PlayerId = " + str(player_id)
            self.cur.execute(update_str)
        except sql.Error as e:
            raise e
        return

    def undo_match(self, match_id: int) -> None:
        try:
            self.cur.execute('''
                    SELECT Player1Id, Player1Rating, Player2Id, Player2Rating
                    FROM Match
                    WHERE MatchId = ?
                ''', (match_id,))
            old_ratings = self.cur.fetchone()
            self.update_player(["Rating"], [old_ratings[1]], old_ratings[0])
            self.update_player(["Rating"], [old_ratings[3]], old_ratings[2])
            self.delete_match(match_id)
        except sql.Error as e:
            raise e
        return

    def delete_match(self, match_id: int) -> None:
        try:
            self.cur.execute('''
                    DELETE FROM Match
                    WHERE MatchId = ?
                ''', (match_id,))
        except sql.Error as e:
            raise e
        return

    def delete_player(self, name: str) -> None:
        try:
            self.cur.execute('''
                    DELETE FROM Player
                    WHERE Name = ?
                ''', (name,))
        except sql.Error as e:
            raise e
        return

    def save_changes(self) -> None:
        try:
            self.conn.commit()
        except sql.Error as e:
            raise e
        return

    def get_player_history(self, name: str) -> pd.DataFrame:
        sql_query = """
            SELECT
                CASE WHEN t0.Name = '{}' THEN t0.Name ELSE t1.name2 END AS "Jugador 1",
                CASE WHEN t0.Name = '{}' THEN Match.Player1Rating ELSE Match.Player2Rating END AS "Rating 1",
                CASE WHEN t0.Name = '{}' THEN Match.Player1Score ELSE Match.Player2Score END AS "Sets 1",
                CASE WHEN t0.Name = '{}' THEN Match.Player2Score ELSE Match.Player1Score END AS "Sets 2",
                CASE WHEN t0.Name = '{}' THEN Match.Player2Rating ELSE Match.Player1Rating END AS "Rating 2",
                CASE WHEN t0.Name = '{}' THEN t1.name2 ELSE t0.Name END AS "Jugador 2"
            FROM
                Match
                JOIN Player AS t0 ON Match.Player1Id = t0.PlayerId
                JOIN (
                SELECT
                    Player.Name AS name2,
                    Player.PlayerId AS id2
                FROM
                    Player
            ) AS t1 ON Match.Player2Id = t1.id2
            WHERE
                t1.name2 = "{}"
                OR t0.Name = "{}"
        """
        df = pd.read_sql_query(sql_query.format(
            name, name, name, name, name, name, name, name), self.conn)
        return df
