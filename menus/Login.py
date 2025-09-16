import tkinter as tk
from clases_internas.usuarios import Instructor, Student
from clases_internas.cursos import Courses
from menus.graphic_tools import Window, PagePrincipal, Page, Tabla
from data.data_base import data
from tkinter import PhotoImage

root = Window('Ventana', (1920, 1080))

class Login(PagePrincipal):
    def __init__(self, master,   **kwargs):
        super().__init__(master=master, bg='red', **kwargs)

        f_izq = tk.Frame(self, width=800, height=1080, bg='gray')
        f_izq.pack_propagate(False)
        f_izq.pack(side="left")

        f_der = tk.Frame(self, width=1120, height=1080, bg='green')
        f_der.pack_propagate(False)
        f_der.pack(side="right")



log = Login(root)
root.mainloop()