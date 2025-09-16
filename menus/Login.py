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

        f_der = tk.Frame(self, width=1120, height=1080, bg='green')
        f_der.pack_propagate(False)
        f_der.pack(side="right")

        f_top = tk.Frame(self, width=800, height=200, bg='red')
        f_top.pack_propagate(False)
        f_top.pack(side="top")

        f_izq = tk.Frame(self, width=800, height=1080, bg='white')
        f_izq.pack_propagate(False)
        f_izq.pack(side="left")





        photo = PhotoImage(file=r'sources/imagen_universidad.png', width=1120, height=1080)
        l_photo = tk.Label(f_der, image=photo)
        l_photo.image = photo
        l_photo.pack()

        logo = PhotoImage(file=r'sources/Logo.png', width=800, height=200)
        logo_photo = tk.Label(f_top, image=logo)
        logo_photo.image = logo
        logo_photo.pack()

        tk.Label(f_izq, text="Login", fg='black', font=('arial', 50, 'bold'), bg='white').pack(side="top")
        tk.Label(f_izq, text="Usuario", fg='black', font=('arial', 20, 'bold')).pack(side='left')
        tk.Label(f_izq, text="Contraseña", fg='black', font=('arial', 20, 'bold')).pack(side="left")


        l_front = ('Arial',14)
        tk.Entry(width=25, font=l_front)








log = Login(root)
root.mainloop()