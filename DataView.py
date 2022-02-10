import ttkbootstrap as ttk
from ttkbootstrap.tableview import *
import sqlite3 as sql
from ttkbootstrap.constants import *


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
            relief=FLAT,
            borderwidth=0,
            highlightthickness=0
        )
        standings_canvas.pack(side=LEFT, fill=BOTH)
        standings_frame = ttk.Frame(standings_canvas)
        standings_canvas.create_window(
            (0, 0), window=standings_frame, anchor=NW)
        standings_frame.pack(fill=BOTH)
        self.standings_tv = Tableview(standings_frame, searchable=True)
        self.standings_tv.grid(row=0, column=0, sticky="NSEW")

        matches_tab = ttk.Frame(self)
        matches_canvas = ttk.Canvas(
            master=matches_tab,
            relief=FLAT,
            borderwidth=0,
            highlightthickness=0
        )
        matches_canvas.pack(side=LEFT, fill=BOTH)
        matches_frame = ttk.Frame(matches_canvas)
        matches_canvas.create_window((0, 0), window=matches_frame, anchor=NW)
        matches_frame.pack(fill=BOTH)
        self.matches_tv = Tableview(matches_frame, searchable=True)
        self.matches_tv.grid(row=0, column=0, sticky="NSEW")

        self.add(standings_tab, text="Posiciones")
        self.add(matches_tab, text="Partidos")

    def update_standings(self, standings: List) -> None:
        self.standings_tv.build_table_data(coldata=[
            {"text": "Posición", "stretch": True},
            {"text": "Nombre", "stretch": True},
            {"text": "Rating", "stretch": True}
        ], rowdata=standings)
        return

    def update_matches(self, matches: List) -> None:
        self.matches_tv.build_table_data(coldata=[
            {"text": "Jugador 1", "stretch": True},
            {"text": "Resultado", "stretch": True},
            {"text": "Jugador 2", "stretch": True}
        ], rowdata=matches)
        return
