import ttkbootstrap as ttk
from typing import Callable
from typing import List

class MatchForm(ttk.LabelFrame):
  """
  Formulario para crear un jugador
  """
  def __init__(self, parent, callback: Callable, **kwargs) -> None:
    super().__init__(parent, **kwargs)
    self.parent = parent
    self.callback = callback
    self.create_widgets()
    return
  
  def create_widgets(self) -> None:
    """
    Crea los controles del formulario
    """
    self.names_1 = ttk.StringVar(self)
    self.sets_1 = ttk.IntVar(self)
    self.jug_1_name = ttk.Combobox(self, textvariable=self.names_1)
    self.jug_1_sets = ttk.Combobox(self, textvariable=self.sets_1,
     values=[0,1])
    self.jug_1_delta = ttk.Label(self, text="+10/-10")

    self.names_2 = ttk.StringVar(self)
    self.sets_2 = ttk.IntVar(self)
    self.jug_2_name = ttk.Combobox(self, textvariable=self.names_2)
    self.jug_2_sets = ttk.Combobox(self, textvariable=self.sets_2,
      values=[0,1])
    self.jug_2_delta = ttk.Label(self, text="+10/-10")

    self.btn_save_match = ttk.Button(self, text="Guardar resultado",
      width=20, command=self.callback, bootstyle="primary")
    self.btn_check_deltas = ttk.Button(self, text="Chequear +/-",
      width=20, command=lambda: print("delta chequeado"),
       bootstyle="outline")
    
    self.modalidad = ttk.IntVar(self)
    self.modalidad.set(1)
    modalidades_frame = ttk.Frame(self)
    modalidades_frame.grid(row=0, column=0, sticky="EW")
    modalidades = {
      "Mejor de 1": 1,
      "Mejor de 3": 3,
      "Mejor de 5": 5,
      "Mejor de 7": 7
    }
    for i, item in enumerate(modalidades):
      ttk.Radiobutton(self, text=item, variable=self.modalidad,
        value=modalidades[item], command=None).grid(
        row=0, column=i)
      modalidades_frame.columnconfigure(i, weight=1, uniform="group1")

    self.jug_1_name.grid(row=1, column=0)
    self.jug_1_sets.grid(row=1, column=1)
    self.jug_1_delta.grid(row=1, column=2)
    self.btn_save_match.grid(row=1, column=3)
    self.jug_2_name.grid(row=2, column=0)
    self.jug_2_sets.grid(row=2, column=1)
    self.jug_2_delta.grid(row=2, column=2)
    self.btn_check_deltas.grid(row=2, column=3) 
    return
  
  def update_player_opt(self, players: List[str]) -> None:
    self.jug_1_name["values"] = players
    self.jug_2_name["values"] = players
    return