import tkinter as tk
from clases_internas.usuarios import Instructor, Student
from menus.graphic_tools import Window, PagePrincipal, pack_create_line
from student_menu import StudentMenu
from menu_profesor import  MenuProfesores
from data.data_base import data
from tkinter import PhotoImage


class Login(PagePrincipal):
    def __init__(self, master,  **kwargs):
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
                self.b_creaete.config(state='disabled')
                self.b_forgot.config(state='disabled')
                self.l_inf.config(text=text, fg='red')
                self.l_inf.after(1500, exit_error)

            def init_student(): #PARA INICIAR COMO ESTUDIANTE
                self.e_user.config(state='normal')
                self.e_password.config(state='normal')
                self.b_login.config(state='normal')
                self.b_creaete.config(state='normal')
                self.b_forgot.config(state='normal')
                self.l_inf.config(text=self.inf_text)

                self.change_page(StudentMenu(self.master, parent=self,
                                             student=Student(data.students[str(self.e_user.get())]['name'],self.e_password.get(), str(self.e_user.get()))))

            def init_instruc(): #PARA INICIAR COMO ESTUDIANTE
                self.e_user.config(state='normal')
                self.e_password.config(state='normal')
                self.b_login.config(state='normal')
                self.b_creaete.config(state='normal')
                self.b_forgot.config(state='normal')
                self.l_inf.config(text=self.inf_text)

                self.change_page(MenuProfesores(self.master, Instructor(data.instructors[self.e_user.get()]['name'], self.e_password.get(), self.e_user.get()), self))

            if str(self.e_user.get())[:3] == 'IST':
                if str(self.e_user .get()) in data.instructors:
                    if data.instructors[str(self.e_user .get())]['password'] == str(self.e_password.get()):
                        self.e_user.config(state='disabled')
                        self.e_password.config(state='disabled')
                        self.b_login.config(state='disabled')
                        self.b_creaete.config(state='disabled')
                        self.b_forgot.config(state='disabled')
                        self.l_inf.config(text='Iniciando sesión...')
                        self.b_login.after(1300, init_instruc)
                    else: show_error()
                else: show_error()
            elif str(self.e_user.get())[:3] == 'STU':
                if str(self.e_user .get()) in data.students:
                    if data.students[str(self.e_user .get())]['password'] == str(self.e_password.get()):
                        self.e_user.config(state='disabled')
                        self.e_password.config(state='disabled')
                        self.b_login.config(state='disabled')
                        self.b_creaete.config(state='disabled')
                        self.b_forgot.config(state='disabled')
                        self.l_inf.config(text='Iniciando sesión...')
                        self.b_login.after(1300, init_student)
                    else: show_error()
                else: show_error()

            else: show_error('Error: No se pudo iniciar sesión\nCódigo no valido')

        def create_user():
            self.shut_down()
            self.top_level = tk.Toplevel(self.master, width=1000, height=700, bg='white')
            self.top_level.resizable(False,False)
            self.top_level.pack_propagate(False)  # PARA EVITAR QUE SE DEFORME AL HACER UN PACK
            self.top_level.grab_set()
            txt = tk.Label(self.top_level, text='Crear usuario', font=('Arial', 30, 'bold'), fg='white', bg='red')
            txt.pack(fill='x')
            v = tk.StringVar(value='1')  # Variable global de los RadioButton
            self.top_top_frame = tk.Frame(self.top_level, bg='white')
            self.top_top_frame.pack()
            tk.Radiobutton(self.top_top_frame, text='Estudiante', value='1', variable=v, font=('Arial', 17, 'bold'), bg='white').pack(ipady=5, padx=10, side='right')
            tk.Radiobutton(self.top_top_frame, text='Instructor', value='2', variable=v, font=('Arial', 17, 'bold'), bg='white').pack(ipady=5, padx=10, side='left')
            self.f_toplevel = tk.Frame(self.top_level, bg='white')
            self.f_toplevel.pack()

            l_name, e_name = pack_create_line(self.f_toplevel, tk.Label, {'text': 'Nombre:      ',  'fg':'black', 'font':('Arial', 30, 'bold'), 'justify':'left','bg':'white'},
                                               tk.Entry, {'width':20, 'font':e_front, 'relief':"solid", 'bg':'white'},
                                               _pady=60 , _padx=42,  bg='white')

            l_passw, e_password = pack_create_line(self.f_toplevel, tk.Label, {'text': 'Contraseña:',  'fg':'black', 'font':('Arial', 30, 'bold'), 'justify':'left','bg':'white'},
                                               tk.Entry, {'width':20, 'font':e_front, 'relief':"solid"},
                                               _pady=60 , _padx=42,  bg='white')
            self.top_info_add = tk.Label(self.f_toplevel, text='', font=('Arial', 30, 'bold'), fg='blue')

            def create_user_json():
                if e_name.get().strip() != '' and e_password.get().strip() != '':
                    if v.get() == '1':  # Estudiante

                            stu = Student(e_name.get(), e_password.get())
                            stu.create_student(e_name.get(), e_password.get())
                            self.top_info_add.config(text=f'Se agregó {e_name.get()}, su código es {stu.user_id}', bg='white')
                            self.button_login.config(state='disabled')
                    elif v.get() == '2':  # Instructor
                        inst = Instructor(e_name.get(), e_password.get())
                        inst.create_instructor(e_name.get(), e_password.get())
                        self.top_info_add.config(text=f'Se agregó {e_name.get()}, su código es {inst.user_id}', bg='white')
                elif e_name.get().strip() == '' and e_password.get().strip() == '': self.top_info_add.config(text=f'Ambos estan vacios!! Así no papito...')
                elif e_name.get().strip() == '': self.top_info_add.config(text=f'El nombre no puede estar vacío!!')
                elif e_password.get().strip() == '': self.top_info_add.config(text=f'La contraseña no puede estar vacía!!')
                else: self.top_info_add.config(text=f'No sé, algo no está bien...')
                self.top_info_add.pack(pady=10)
                self.shut_down('normal')

            self.button_login = tk.Button(self.f_toplevel, text='Crear', font=('Arial', 30, 'bold'), fg='white', width=20,
                                     bg='red', activebackground='#FF9EA2', cursor='hand2', relief='solid', command=create_user_json)

            self.button_login.pack(pady=30, padx=30)

            def exit_top():
                self.shut_down('normal')
                self.top_level.destroy()
            self.top_level.protocol("WM_DELETE_WINDOW", exit_top)

        def forgot_password():
            self.forgot_level = tk.Toplevel(self.master, width=900, height=700, bg='blue')
            self.forgot_level.resizable(False, False)
            self.forgot_level.pack_propagate(False)

            forgot = PhotoImage(file=r'sources/olvido_de_contras.gif', width=900, height=700)
            forgot_photo = tk.Label(self.forgot_level, image=forgot)
            forgot_photo.image = forgot
            forgot_photo.pack()

        def show_creators():
            self.show_level = tk.Toplevel(self.master, width=1300, height=900, bg='blue')
            self.show_level.resizable(False, False)
            self.show_level.pack_propagate(False)


        # Labels
        l_front, e_front = ('Arial', 12, 'bold'), ('Arial', 30)
        tk.Label(self.f_izq, text="Login", fg='black', font=('Arial', 50, 'bold'), bg='white').pack(side="top")

        #Buttons
        self.b_login = tk.Button(self.f_izq,text='Log In', font=('Arial', 30, 'bold'), fg='white', width=20, bg='red', activebackground='#FF9EA2', cursor='hand2', relief='solid', command=log_in)
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
                                                        tk.Button, {'text':'Olvido de contraseña', "font":('Arial',15, 'bold'), "fg":'red', "width":20, "highlightthickness":0, "bd":0, "bg":'white', "cursor":'hand2', 'command':forgot_password},
                                                        tk.Button,
                                                        {'text': 'Crear Cuenta', "font": ('Arial', 15, 'bold'), "fg": 'red', "width": 20, "highlightthickness": 0, "bd": 0,"bg": 'white', "cursor": 'hand2', 'command': create_user},
                                                        width=720, height=40, _pady=60, bg='white')

        self.b_login.pack(pady=80, padx=30)
        self.inf_text = 'Portal academico de Universidad RAR de Quetzaltenango'
        self.l_inf = tk.Label(self.f_izq, text=self.inf_text, font=('Arial', 15, 'bold'), fg='gray', bg='white')
        self.l_inf.pack(pady=10, padx=30)
        #self.meet = tk.Button(self.f_izq,text='Empresarios', font=('Arial', 30, 'bold'), fg='white', width=20, bg='white', activebackground='white', cursor='hand2', command=show_creators)
        #self.meet.pack(pady=20, padx=30)

        self.clear_widgest = [self.e_password, self.e_user]

    def shut_down(self, state_='disabled'):
        self.b_login.config(state=state_)
        self.e_user.config(state=state_)
        self.e_password.config(state=state_)
        self.b_forgot.config(state=state_)
        self.b_creaete.config(state=state_)
