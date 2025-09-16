import tkinter as tk
from menus.graphic_tools import Window, PagePrincipal, pack_create_line, Image
#from data.data_base import data
from tkinter import PhotoImage


root = Window('Ventana')

class Login(PagePrincipal):
    def __init__(self, master,   **kwargs):
        super().__init__(master=master, bg='red', **kwargs)

        self.f_izq = tk.Frame(self, width=int(master.w*0.42), height=1080, bg='white')
        self.f_izq.pack_propagate(False)
        self.f_izq.pack(side="left")

        self.f_top = tk.Frame(self.f_izq, width=int(master.w*0.42), height=180, bg='red')
        self.f_top.pack_propagate(False)
        self.f_top.pack(side="top")

        logo = PhotoImage(file=r'sources/Logo.png', width=int(master.w*0.42), height=200)
        logo_photo = tk.Label(self.f_top, image=logo)
        logo_photo.image = logo
        logo_photo.pack()

        self.f_der = tk.Frame(self, width=int(master.w*0.48), height=1080, bg='green')
        self.f_der.pack_propagate(False)
        self.f_der.pack(side="left", fill="both", expand=True)

        photo = Image(self.f_der,r'sources/imagen_universidad.png', master.w, master.h)
        photo.pack(fill='both', expand=True)
        #photo = PhotoImage(file=r'sources/imagen_universidad.png').subsample(1,1)
        #l_photo = tk.Label(self.f_der, image=photo)
        #l_photo.image = photo
        #l_photo.pack(fill='both', expand=True)

        # Labels
        l_front, e_front = ('Arial', 12, 'bold'), ('Arial', 30)
        tk.Label(self.f_izq, text="Login", fg='black', font=('Arial', 40, 'bold'), bg='white').pack(side="top")
        l_user = tk.Label(text="Usuario:", fg='black', font=('Arial', 30, 'bold'), bg='white')
        l_password = tk.Label(text="Contraseña:", fg='black', font=('arial', 30, 'bold'), bg='white')
        # Entry
        e_user = tk.Entry(width=20, font=e_front, relief="solid")
        e_password = tk.Entry(width=20, font=e_front, relief="solid")
        # Buttons
        b_forgot = tk.Button(text='Olvido de contraseña', font=('Arial', 15, 'bold'), fg='red', width=20,
                             highlightthickness=0, bd=0, bg='white', cursor='hand2')
        b_creaete = tk.Button(text='Crear Cuenta', font=('Arial', 15, 'bold'), fg='red', width=20, highlightthickness=0,
                              bd=0, bg='white', cursor='hand2')
        b_login = tk.Button(self.f_izq, text='Log In', font=('Arial', 30, 'bold'), fg='black', width=20, bg='red',
                            activebackground='#FF9EA2', cursor='hand2', relief='solid')

        pack_create_line(self.f_izq, l_user, e_user, _pady=50, _padx=42, width=450, bg='white')
        pack_create_line(self.f_izq, l_password, e_password, _padx=10, width=450, bg='white')
        pack_create_line(self.f_izq, b_forgot, b_creaete, width=720, height=40, _pady=40, bg='white')
        b_login.pack(pady=40, padx=30)
        tk.Label(self.f_izq, text='Portal academico de Universidad RAR de Quetzaltenango', font=('Arial', 15, 'bold'),
                 fg='gray', bg='white').pack(pady=10, padx=30)


log = Login(root)
root.mainloop()