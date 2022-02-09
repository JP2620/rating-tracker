import ttkbootstrap as ttk
import ttkbootstrap.tableview as ttv
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
    standings_frame.pack(fill=BOTH)
    standings_canvas.create_window((0, 0), window=standings_frame, anchor=NW)

    matches_tab = ttk.Frame(self)
    matches_canvas = ttk.Canvas(
      master=matches_tab,
      relief=FLAT,
      borderwidth=0,
      highlightthickness=0
    )
    matches_canvas.pack(side=LEFT, fill=BOTH)
    matches_frame = ttk.Frame(matches_canvas)
    matches_frame.pack(fill=BOTH)
    matches_canvas.create_window((0, 0), window=matches_frame, anchor=NW)

    self.add(standings_tab, text="Posiciones")
    self.add(matches_tab, text="Partidos")
