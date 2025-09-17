#Otra vez porque elimine mi archivo anterior por accidente
import tkinter as tk
from graphic_tools import Window, Page, PagePrincipal, ScrollFrame
from clases_internas.usuarios import Student
from data.data_base import data
from tkinter import PhotoImage

azul_claro = '#669BBC'
azul_marino = '#003949'
blanco_hueso = '#FDF0D5'

scroll_bg = '#2E2E39'
scroll = '#FFFFFF'
scroll_ac = '#C8D3E9'
wid = 600
font = 'Arial'
fg = '#FDF0D5'


root = Window("Menu Profesores", (1920,1080))

class MenuProfesores(PagePrincipal):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.__frame_profesor = tk.Frame(self, width=1920, height=1080, bg=blanco_hueso)
        self.__barra_profesor = tk.Frame(self, width=250, height=1080, bg=azul_claro)
        self.__barra_profesor.pack_propagate(False)
        self.__barra_profesor.pack(side='left')

        self.__barra_materia_boton = tk.Button(self.__barra_profesor, text="Curso", bg=azul_marino, fg=fg, font=font)
        self.__barra_materia_boton.pack(fill="x", pady='250')

        self.__frame_info = tk.Frame(self.__frame_profesor,  width=wid, height=250, bg=azul_marino)
        self.__frame_info.pack_propagate(False)
        self.__frame_info.pack()\





men = MenuProfesores(root)
root.mainloop()