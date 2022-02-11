import ttkbootstrap as ttk
import tkinter as tk
from typing import List, Callable
from ttkbootstrap.constants import *
from ttkbootstrap.tooltip import ToolTip


class ActionMenu(ttk.Frame):

    def __init__(self, parent, callbacks:List[Callable], **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent
        self.callbacks = callbacks
        self.create_widgets()
        return

    def create_widgets(self):
        self.undo_img = tk.PhotoImage(file='images/icons8-undo-30.png')
        self.btn_undo = ttk.Button(self,
                                   image=self.undo_img,
                                   command=self.callbacks[0],
                                   bootstyle="link")
        self.btn_undo.grid(row=0, column=0, padx=0, pady=(10, 0), sticky="N")
        ToolTip(self.btn_undo, text="Deshacer")

        self.redo_img = tk.PhotoImage(file='images/icons8-redo-30.png')
        self.btn_redo = ttk.Button(self,
                                   image=self.redo_img,  
                                   command=self.callbacks[1],
                                   bootstyle="link")
        self.btn_redo.grid(row=1, column=0, padx=0, pady=0, sticky="N")
        ToolTip(self.btn_redo, text="Rehacer")

        self.excel_img = tk.PhotoImage(file='images/icons8-microsoft-excel-30.png')
        self.btn_export_excel = ttk.Button(self,
                                image=self.excel_img,
                                command=lambda: print("hola"),
                                bootstyle="link")
        self.btn_export_excel.grid(row=2, column=0, padx=0, pady=0, sticky="N")
        ToolTip(self.btn_export_excel, text="Exportar a Excel")
