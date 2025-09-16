import tkinter as tk
from clases_internas.usuarios import Instructor, Student
from clases_internas.cursos import Courses
from menus.graphic_tools import Window, PagePrincipal, pack_create_line
from data.data_base import data
from tkinter import PhotoImage


root = Window('Ventana', (1920, 1080))

class Login(PagePrincipal):
    def __init__(self, master,   **kwargs):
        super().__init__(master=master, bg='red', **kwargs)
        self.f_der = tk.Frame
        self.f_top = tk.Frame
        self.f_izq = tk.Frame

        self.f_der = tk.Frame(self, width=1120, height=1080, bg='green')
        self.f_der.pack_propagate(False)
        self.f_der.pack(side="right")

        self.f_top = tk.Frame(self, width=800, height=200, bg='red')
        self.f_top.pack_propagate(False)
        self.f_top.pack(side="top")

        self.f_izq = tk.Frame(self, width=800, height=1080, bg='white')
        self.f_izq.pack_propagate(False)
        self.f_izq.pack(side="left")

        photo = PhotoImage(file=r'sources/imagen_universidad.png', width=1120, height=1080)
        l_photo = tk.Label(self.f_der, image=photo)
        l_photo.image = photo
        l_photo.pack()

        logo = PhotoImage(file=r'sources/Logo.png', width=800, height=200)
        logo_photo = tk.Label(self.f_top, image=logo)
        logo_photo.image = logo
        logo_photo.pack()

        #Labels
        l_front, e_front = ('Arial', 12, 'bold'), ('Arial', 30)
        tk.Label(self.f_izq, text="Login", fg='black', font=('Arial', 50, 'bold'), bg='white').pack(side="top")
        l_user = tk.Label( text="Usuario:", fg='black', font=('Arial', 30, 'bold'), bg='white')
        l_password = tk.Label(text="Contraseña:", fg='black', font=('arial', 30, 'bold'), bg='white')
        #Entry
        e_user = tk.Entry(width=20, font=e_front, relief="solid")
        e_password = tk.Entry(width=20, font=e_front, relief="solid")
        #Buttons
        b_forgot = tk.Button( text='Olvido de contraseña', font=('Arial',15, 'bold'), fg='red', width=20, highlightthickness=0, bd=0, bg='white', cursor='hand2')
        b_creaete = tk.Button(text='Crear Cuenta', font=('Arial',15, 'bold'), fg='red', width=20, highlightthickness=0, bd=0, bg='white', cursor='hand2')
        b_login = tk.Button(self.f_izq,text='Log In', font=('Arial', 30, 'bold'), fg='black', width=20, bg='red', activebackground='#FF9EA2', cursor='hand2', relief='solid')


        pack_create_line(self.f_izq, l_user, e_user, _pady=100 , _padx=42, width=450,  bg='white')
        pack_create_line(self.f_izq, l_password, e_password, _padx=10, width=450,  bg='white' )
        pack_create_line(self.f_izq, b_forgot, b_creaete, width=720, height=40, _pady=20,  bg='white')
        b_login.pack(pady=80, padx=30)
        tk.Label(self.f_izq, text='Portal academico de Universidad RAR de Quetzaltenango', font=('Arial', 15, 'bold'), fg='gray', bg='white').pack(pady=10, padx=30)


log = Login(root)
root.mainloop()