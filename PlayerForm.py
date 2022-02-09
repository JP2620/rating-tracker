import ttkbootstrap as ttk
from typing import Callable


class PlayerForm(ttk.LabelFrame):
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
    self.lbl_nombre = ttk.Label(self, text="Nombre del jugador")
    self.lbl_rating = ttk.Label(self, text="Rating")
    self.lbl_nombre.grid(row=0, column=0)
    self.lbl_rating.grid(row=0, column=1)

    self.entry_nombre = ttk.Entry(self, width=20, justify="center")
    self.entry_rating = ttk.Entry(self, width=7, justify="center")
    self.entry_nombre.grid(row=1, column=0)
    self.entry_rating.grid(row=1, column=1)

    self.btn_add_jugador = ttk.Button(self, text="Agregar jugador",
      width=20, command=self.callback)
    self.btn_add_jugador.grid(row=1, column=3)
    return
  
  def get_player(self) -> str:
    """
    Retorna el nombre del jugador
    """
    return self.entry_nombre.get()
  
  def get_rating(self) -> int:
    """
    Retorna el rating del jugador
    """
    return int(self.entry_rating.get())

    