import ttkbootstrap as ttk
from typing import Callable

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
    self.jug_1_name = ttk.Combobox(self, textvariable=self.names_1, values= [
      "John Doe", "Jane Doe", "Jack Doe", "Jill Doe"
    ])
    self.jug_1_sets = ttk.Combobox(self, textvariable=self.sets_1,
     values=[0,1])
    self.jug_1_delta = ttk.Label(self, text="+10/-10")

    self.names_2 = ttk.StringVar(self)
    self.sets_2 = ttk.IntVar(self)
    self.jug_2_name = ttk.Combobox(self, textvariable=self.names_2, values= [
      "John Doe", "Jane Doe", "Jack Doe", "Jill Doe"
      ])
    self.jug_2_sets = ttk.Combobox(self, textvariable=self.sets_2,
      values=[0,1])
    self.jug_2_delta = ttk.Label(self, text="+10/-10")

    self.btn_save_match = ttk.Button(self, text="Guardar resultado",
      width=20, command=self.callback, bootstyle="primary")
    self.btn_check_deltas = ttk.Button(self, text="Chequear +/-",
      width=20, command=lambda: print("delta chequeado"),
       bootstyle="outline")

    self.jug_1_name.grid(row=0, column=0)
    self.jug_1_sets.grid(row=0, column=1)
    self.jug_1_delta.grid(row=0, column=2)
    self.btn_save_match.grid(row=0, column=3)
    self.jug_2_name.grid(row=1, column=0)
    self.jug_2_sets.grid(row=1, column=1)
    self.jug_2_delta.grid(row=1, column=2)
    self.btn_check_deltas.grid(row=1, column=3) 
    return