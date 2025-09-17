import tkinter as tk
from turtledemo.penrose import inflatedart
from clases_internas.usuarios import Instructor, Student
from student_menu import StudentMenu
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

        #COMMANDS
        def log_in():
            def show_error(text='Error: No se pudo iniciar sesión'):
                def exit_error():
                    self.l_inf.config(text=self.inf_text, fg='gray')
                    self.b_login.config(state='normal')
                self.b_login.config(state='disabled')
                self.l_inf.config(text=text, fg='red')
                self.l_inf.after(1500, exit_error)

            def init_student(): #PARA INICIAR COMO ESTUDIANTE
                self.e_user.config(state='normal')
                self.e_password.config(state='normal')
                self.b_login.config(state='normal')
                self.l_inf.config(text=self.inf_text)

                self.change_page(StudentMenu(self.master, parent=self,
                                             student=Student(data.students[str(self.e_user.get())]['name'],self.e_password.get(), str(self.e_user.get()))))

            if str(self.e_user.get())[:3] == 'IST':
                if str(self.e_user .get()) in data.instructors:
                    if data.instructors[str(self.e_user .get())]['password'] == str(self.e_password.get()):
                        pass#self.after()
                    else: show_error()
                else: show_error()
            elif str(self.e_user.get())[:3] == 'STU':
                if str(self.e_user .get()) in data.students:
                    if data.students[str(self.e_user .get())]['password'] == str(self.e_password.get()):
                        self.e_user.config(state='disabled')
                        self.e_password.config(state='disabled')
                        self.b_login.config(state='disabled')
                        self.l_inf.config(text='Iniciando sesión...')
                        self.b_login.after(1300, init_student)
                    else: show_error()
                else: show_error()

            else: show_error('Error: No se pudo iniciar sesión\nCódigo no valido')


        def create_user():

            self.top_level = tk.Toplevel(self.master, width=900, height=700, bg='white')
            self.top_level.pack_propagate(False)  # PARA EVITAR QUE SE DEFORME AL HACER UN PACK
            txt = tk.Label(self.top_level, text='Crear usuario', font=('Arial', 25, 'bold'), fg='black', bg='red')
            txt.pack()


            v = tk.StringVar(value='1')  # Variable global de los RadioButton
            tk.Radiobutton(self.top_level, text='Estudiante', value='1', variable=v, font=('Arial', 17, 'bold'), bg='white').pack(ipady=5)
            tk.Radiobutton(self.top_level, text='Instructor', value='2', variable=v, font=('Arial', 17, 'bold'), bg='white').pack(ipady=5)

            self.f_toplevel = tk.Frame(self.top_level, bg='white')
            self.f_toplevel.pack()

            e_name = tk.Entry(state='normal')
            e_password = tk.Entry(state='normal')

            if v.get() == '1': #Estudiante
                i = Student(e_name.get(), e_password.get())
                i.create_student(e_name.get(), e_password.get())
                #self.inf.config(text=f'Se agregó {e_name.get()}, su codigo de estudiante es {i.user_id}')
            elif v.get() == '2': #Instructor
                i =Instructor(e_name.get(), e_password.get())
                i.create_instructor(e_name.get(), e_password.get())
                #self.inf.config(text=f'Se agregó {e_name.get()}, su codigo de docente es {i.user_id}')

            l_name, e_name = pack_create_line(self.f_toplevel, tk.Label, {'text': 'Nombre:      ',  'fg':'black', 'font':('Arial', 30, 'bold'), 'justify':'left','bg':'white'},
                                               tk.Entry, {'width':20, 'font':e_front, 'relief':"solid", 'bg':'white'},
                                               _pady=60 , _padx=42,  bg='white')

            l_passw, e_password = pack_create_line(self.f_toplevel, tk.Label, {'text': 'Contraseña:',  'fg':'black', 'font':('Arial', 30, 'bold'), 'justify':'left','bg':'white'},
                                               tk.Entry, {'width':20, 'font':e_front, 'relief':"solid"},
                                               _pady=60 , _padx=42,  bg='white')

            self.button_login = tk.Button(self.f_toplevel, text='Log In', font=('Arial', 30, 'bold'), fg='black', width=20,
                                     bg='red', activebackground='#FF9EA2', cursor='hand2', relief='solid',)

            self.button_login.pack(pady=80, padx=30)




        # Labels
        l_front, e_front = ('Arial', 12, 'bold'), ('Arial', 30)
        tk.Label(self.f_izq, text="Login", fg='black', font=('Arial', 50, 'bold'), bg='white').pack(side="top")

        #Buttons
        #self.b_forgot = tk.Button()
        #self.b_creaete = tk.Button(text='Crear Cuenta', font=('Arial',15, 'bold'), fg='red', width=20, highlightthickness=0, bd=0, bg='white', cursor='hand2')
        self.b_login = tk.Button(self.f_izq,text='Log In', font=('Arial', 30, 'bold'), fg='black', width=20, bg='red', activebackground='#FF9EA2', cursor='hand2', relief='solid', command=log_in)
        #USUARIO
        l_user, self.e_user = pack_create_line(self.f_izq,
                                               tk.Label, {'text':"Codigo\nde usuario:", 'fg':'black', 'font':('Arial', 30, 'bold'), 'justify':'left','bg':'white'},
                                               tk.Entry, {'width':20, 'font':e_front, 'relief':"solid"},
                                               _pady=60 , _padx=42, width=450,  bg='white')
        #CONTRASEÑA
        l_password, self.e_password = pack_create_line(self.f_izq,
                                                  tk.Label, {'text': "Contraseña", 'fg': 'black', 'font': ('Arial', 30, 'bold'),'bg': 'white'},
                                                  tk.Entry, {'width': 20, 'font': e_front, 'relief': "solid"},
                                                  _padx=40, width=450,  bg='white')

        self.b_forgot,self.b_creaete = pack_create_line(self.f_izq,
                                                        tk.Button, {'text':'Olvido de contraseña', "font":('Arial',15, 'bold'), "fg":'red', "width":20, "highlightthickness":0, "bd":0, "bg":'white', "cursor":'hand2'},
                                                        tk.Button,
                                                        {'text': 'Crear Cuenta', "font": ('Arial', 15, 'bold'), "fg": 'red', "width": 20, "highlightthickness": 0, "bd": 0,"bg": 'white', "cursor": 'hand2', 'command': create_user},
                                                        width=720, height=40, _pady=60, bg='white')

        self.b_login.pack(pady=80, padx=30)
        self.inf_text = 'Portal academico de Universidad RAR de Quetzaltenango'
        self.l_inf = tk.Label(self.f_izq, text=self.inf_text, font=('Arial', 15, 'bold'), fg='gray', bg='white')
        self.l_inf.pack(pady=10, padx=30)

        self.clear_widgest = [self.e_password, self.e_user]

log = Login(root)
root.mainloop()