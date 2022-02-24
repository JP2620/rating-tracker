import ttkbootstrap as ttk
import tkinter as tk
from typing import List, Callable
from ttkbootstrap.tooltip import ToolTip


class ActionMenu(ttk.Frame):

    def __init__(self, parent, callbacks: List[Callable], **kwargs):
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
                                   bootstyle="link")  # type:ignore
        self.btn_undo.grid(row=0, column=0, padx=0, pady=(10, 0), sticky="N")
        ToolTip(self.btn_undo, text="Deshacer")

        self.redo_img = tk.PhotoImage(file='images/icons8-redo-30.png')
        self.btn_redo = ttk.Button(self,
                                   image=self.redo_img,
                                   command=self.callbacks[1],
                                   bootstyle="link")  # type:ignore
        self.btn_redo.grid(row=1, column=0, padx=0, pady=0, sticky="N")
        ToolTip(self.btn_redo, text="Rehacer")

        self.excel_img = tk.PhotoImage(
            file='images/icons8-microsoft-excel-30.png')
        self.btn_export_excel = ttk.Button(self,
                                           image=self.excel_img,
                                           command=self.callbacks[2],
                                           bootstyle="link")  # type:ignore
        self.btn_export_excel.grid(row=2, column=0, padx=0, pady=0, sticky="N")
        ToolTip(self.btn_export_excel, text="Exportar a Excel")

        self.charts_img = tk.PhotoImage(file='images/icons8-line-chart-30.png')
        self.btn_charts = ttk.Button(self,
                                     image=self.charts_img,
                                     command=self.callbacks[3],
                                     bootstyle="link")  # type:ignore
        self.btn_charts.grid(row=3, column=0, padx=0, pady=0, sticky="N")
        ToolTip(self.btn_charts, text="Ver gráficas")
