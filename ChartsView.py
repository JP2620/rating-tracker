from typing import List, Callable
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import ttkbootstrap as ttk
import matplotlib
matplotlib.use('TkAgg')
import traceback


class ChartsView(ttk.Toplevel):
    def __init__(self, parent, model, **kwargs):
        super().__init__(parent, **kwargs)
        self.model = model
        self.parent = parent
        self.create_widgets()
        return

    def create_widgets(self):
        self.title("Charts")
        self.geometry("750x450")
        self.player = ttk.StringVar(self)
        form_frame = ttk.Frame(self)
        self.players_cb = ttk.Combobox(form_frame,
                                        textvariable=self.player)
        label = ttk.Label(form_frame, text="Jugador:")
        label.grid(row=0, column=0, padx=0, pady=0, sticky="NW")
        self.player.trace("w", self.callback_player_chart)
        self.fig = Figure()
        self.fig.set_size_inches(5,4)
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.players_cb.grid(row=1, column=0, padx=0, pady=0, sticky="NW")
        form_frame.grid(row=0, column=1, sticky="NW", pady=35)
        self.canvas.get_tk_widget().grid(row=0, column=0, padx=(20,0), pady=0, sticky="N")
        return

    def set_player_opt(self, players: List[str]) -> None:
        self.players_cb['values'] = players
        return

    def callback_player_chart(self, *args):
        try:
            self.fig.delaxes(ax=self.fig.axes[0])
        except Exception:
            print(traceback.format_exc())
            pass

        player = self.player.get()
        df = self.model.get_player_history(player)
        df_aux = self.model.get_players()[["Name", "Rating"]]
        df_aux = df_aux.loc[df_aux['Name'] == player]
        df_aux.rename(columns={"Name": "Jugador 1", "Rating": "Rating 1"}, inplace=True)
        df = df.append(df_aux, ignore_index=True)


        ax1 = self.fig.add_subplot()
        ax1.plot([x for x in range(len(df["Rating 1"]))], df["Rating 1"], marker="o", color="#EB6864")
        ax1.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax1.set_xlabel("Partidos")
        ax1.set_ylabel("Rating")
        ax1.set_title(player + ": Rating vs Partidos")
        ax1.grid(True)
        self.canvas.draw()
        return
