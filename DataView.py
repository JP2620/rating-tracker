import ttkbootstrap as ttk
from ttkbootstrap.tableview import Tableview
import sqlite3 as sql
from typing import List


class DataView(ttk.Notebook):
    def __init__(self, parent, **kwargs) -> None:
        super().__init__(parent, **kwargs)
        self.parent = parent
        self.create_widgets()
        return

    def create_widgets(self) -> None:
        standings_tab = ttk.Frame(self)
        standings_canvas = ttk.Canvas(
            master=standings_tab,
            relief=ttk.FLAT,
            borderwidth=0,
            highlightthickness=0
        )
        standings_canvas.pack(side=ttk.LEFT, fill=ttk.BOTH,
                            expand=ttk.YES, padx=10, pady=(5, 15))
        standings_frame = ttk.Frame(standings_canvas)
        standings_canvas.create_window(
            (0, 0), window=standings_frame, anchor=ttk.NW)
        standings_frame.pack(fill=ttk.BOTH)
        self.standings_tv = Tableview(
            standings_frame, searchable=True, height=13)
        self.standings_tv.grid(row=0, column=0, sticky="NSEW")

        matches_tab = ttk.Frame(self)
        matches_canvas = ttk.Canvas(
            master=matches_tab,
            relief=ttk.FLAT,
            borderwidth=0,
            highlightthickness=0
        )
        matches_canvas.pack(side=ttk.LEFT, fill=ttk.BOTH,
                            expand=ttk.YES, padx=10, pady=(5, 15))
        matches_frame = ttk.Frame(matches_canvas)
        matches_canvas.create_window(
            (0, 0), window=matches_frame, anchor=ttk.NW)
        matches_frame.pack(fill=ttk.BOTH)
        self.matches_tv = Tableview(matches_frame, searchable=True, height=13)
        self.matches_tv.grid(row=0, column=0, sticky="NSEW")

        self.add(standings_tab, text="Posiciones")
        self.add(matches_tab, text="Partidos")

    def update_standings(self, standings: List) -> None:
        self.standings_tv.build_table_data(coldata=[
            {"text": "Posición", "stretch": True, "width": 60},
            {"text": "Nombre", "stretch": True},
            {"text": "Rating", "stretch": True},
        ], rowdata=standings)

        for column in self.standings_tv.get_columns():
            self.standings_tv.align_column_left(cid=column.cid)
            self.standings_tv.align_heading_left(cid=column.cid)
        self.standings_tv.pack(fill=ttk.BOTH)
        return

    def update_matches(self, matches: List) -> None:
        self.matches_tv.build_table_data(coldata=[
            {"text": "Jugador 1", "stretch": True},
            {"text": "Resultado", "stretch": True, "width": 60},
            {"text": "Jugador 2", "stretch": True},
        ], rowdata=matches)
        for column in self.matches_tv.get_columns():
            self.matches_tv.align_column_left(cid=column.cid)
            self.matches_tv.pack(fill=ttk.BOTH)
        self.matches_tv.pack(fill=ttk.BOTH)
        return
