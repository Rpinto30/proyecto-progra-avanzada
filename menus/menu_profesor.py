#Otra vez porque elimine mi archivo anterior por accidente
import tkinter as tk
from graphic_tools import Window, Page, PagePrincipal, ScrollFrame
from clases_internas.usuarios import Instructor
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
    def __init__(self, master, user:Instructor  ,**kwargs):
        super().__init__(master, **kwargs)

        self.__barra_profesor = tk.Frame(self, width=700, height=1080, bg=azul_claro)
        self.__barra_profesor.pack_propagate(False)
        self.__barra_profesor.pack(side='left')
        self.__frame_profesor = tk.Frame(self, width=1920-700, height=1080, bg=blanco_hueso)
        self.__frame_profesor.pack_propagate(False)
        self.__frame_profesor.pack(side='right')

        frame__colocar_info = tk.Frame(self.__barra_profesor, bg='black')
        frame__colocar_info.pack(pady=10)
        tk.Label(frame__colocar_info, text='Profesor', font=(font, 60, 'bold'), anchor='w', bg='black', fg=fg).pack(padx=35,
                                                                                                               fill='x',
                                                                                                               pady=10)
        tk.Label(frame__colocar_info, text=f'{user.name} ({user.user_id})', font=(font, 25, 'bold'), anchor='w', bg='black',
                 fg=fg).pack(padx=35, fill='x')

        self.__barra_materia_boton = tk.Button(self.__barra_profesor, text="Curso", bg=azul_marino, fg=fg, font=font)
        self.__barra_materia_boton.pack(fill="x", pady='250')

        self.__frame_info = tk.Frame(self.__frame_profesor,  width=wid, height=250, bg=azul_marino)
        self.__frame_info.pack_propagate(False)
        self.__frame_info.pack()

        # frame colocar info






men = MenuProfesores(root, user=Instructor('Milton Nimatuj', '123', 'IST'))
root.mainloop()