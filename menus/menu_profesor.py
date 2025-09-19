#Otra vez porque elimine mi archivo anterior por accidente
import tkinter as tk

from clases_internas.cursos import Courses
from graphic_tools import Window, Page, ScrollFrame
from clases_internas.usuarios import Instructor, Student
from data.data_base import data

from menus.graphic_tools import pack_create_line
from check_homework import CheckHomework

# Distribución de colores con variables

blanco_gris_azul = '#cdc9c9'
blanco_gris_azul_clarito = '#d1c9c9'
azul_claro = '#4f88ab'
azul_marino = '#002442'
blanco_hueso = '#E1E2D5'

scroll_bg = '#2E2E39'
scroll = '#FFFFFF'
scroll_ac = '#C8D3E9'
wid = 800
font = 'Arial'
fg = '#FDF0D5'


class MenuProfesores(Page):
    def __init__(self, master, instructor:Instructor, parent, **kwargs):
        super().__init__(master, **kwargs)

        self.__barra_profesor = tk.Frame(self, width=500, height=1080, bg=azul_claro)
        self.__barra_profesor.pack_propagate(False)
        self.__barra_profesor.pack(side='left')
        self.__frame_profesor = tk.Frame(self, width=1920-500, height=1080, bg=blanco_hueso)
        self.__frame_profesor.pack_propagate(False)
        self.__frame_profesor.pack(side='right')

        frame__colocar_info = tk.Frame(self.__barra_profesor, bg=azul_claro)
        frame__colocar_info.pack(pady=10)
        tk.Label(frame__colocar_info, text='Profesor', font=(font, 60, 'bold'), anchor='w', bg=azul_claro, fg=fg).pack(padx=35,
                                                                                                               fill='x',
                                                                                                               pady=10)
        tk.Label(frame__colocar_info, text=f'{instructor.name} ({instructor.user_id})', font=(font, 25, 'bold'), anchor='w', bg=azul_claro,
                 fg=fg).pack(padx=35, fill='x')

        self.c_lable_courses = tk.Canvas(self.__barra_profesor, width=wid, height=100, bg=azul_marino, highlightthickness=0,
                                         bd=0)
        self.c_lable_courses.create_line(10, 0, wid - 10, 0, fill='black', width=10)
        self.c_lable_courses.create_line(10, 100, wid - 10, 100, fill='black', width=10)
        self.c_lable_courses.pack(fill='x')
        self.c_lable_courses.create_window((wid // 2)-150, 100 // 2,
                                           window=tk.Label(self.c_lable_courses, text='Cursos', bg=azul_marino,
                                                           fg='white', font=(font, 30, 'bold')))
        # Boton de crear curso

        def create_course():
            self.top_level = tk.Toplevel(self.master, width=1000, height=700, bg='white')
            self.top_level.resizable(False,False)
            #self.top_level.pack_propagate(False)  # PARA EVITAR QUE SE DEFORME AL HACER UN PACK
            self.top_level.grab_set()

            tk.Label(self.top_level, text='Ingresa un nombre para tu curso:', font=('Arial', 30, 'bold'), bg='white').pack(pady=30)
            inf = tk.Label(self.top_level, text='', font=('Arial', 15, 'bold'), bg='white')
            inf.pack(pady=10)
            e_ = tk.Entry(self.top_level,  font=('Arial', 45, 'bold'))
            e_.pack(pady=20, padx=20)

            def asing():
                if e_.get().strip() != '':
                    instructor.create_course(str(e_.get()))
                    a.config(state='disabled')
                    inf.config(text='El curso ha sido creado correctamente')

                else:
                    inf.config(text='La entrada no puede estar vacía!!')

                if len(data.instructors[instructor.user_id]['courses']) > 0:
                    for w in self.scr_courses.scr_frame.winfo_children(): w.pack_forget()
                    for courses_id in data.instructors[instructor.user_id]['courses']:
                        scroll_curso = tk.Frame(self.scr_courses.scr_frame, bg=blanco_hueso, highlightthickness=3,
                                                highlightbackground=blanco_gris_azul)
                        self.scr_courses.pack_on_scroll(scroll_curso, fill="x", pady=10, padx=2)
                        # BOTON CURSOS
                        boton_scroll = tk.Button(scroll_curso, text=str(data.courses[courses_id]['course_name']),
                                                 cursor='hand2', width=15,
                                                 font=(font, 39), bg=blanco_gris_azul_clarito)
                        boton_scroll.pack(fill='x')
                        tk.Label(scroll_curso,
                                 text=f"{str(courses_id)} - {str(data.instructors[data.courses[courses_id]['teacher']]['name'])}",
                                 font=(font, 17), anchor='center', bg=blanco_gris_azul_clarito).pack(fill='x')
                        boton_scroll.config(command=lambda c=courses_id: entrada_menu(c))


            a = tk.Button(self.top_level, text='Crear curso!', bg='red', fg='white',font=('Arial', 30, 'bold'), command=asing)
            a.pack(pady=10)

            def exit_top():
                self.top_level.destroy()
            self.top_level.protocol("WM_DELETE_WINDOW", exit_top)

        tk.Button(self.__barra_profesor, text='Crear curso', font=(font, 30), anchor='center', width=14, fg=fg, command=create_course, cursor='hand2',
                  bg=azul_claro).pack(fill='x', side='bottom')

        self.scr_courses = ScrollFrame(self.__barra_profesor,
                                       width=wid, height=(1080 - 200), vbar_position='left',
                                       cl_bars_bg=scroll_bg, cl_bars_des=scroll, cl_bars_act=scroll_ac,
                                       bg=blanco_hueso)
        self.scr_courses.pack()


        self.__barra_materia_boton = tk.Button(self.__barra_profesor, text="Curso", bg=azul_marino, fg=fg, font=font, cursor='hand2')
        self.__barra_materia_boton.pack(fill="x", pady='250')

        # Frame de arriba
        self.__frame_info = tk.Frame(self.__frame_profesor,  width=1920 - 400, height=150, bg=azul_marino)
        self.__frame_info.pack_propagate(False)
        self.__frame_info.pack()


        self.menu, self.id_curso = None, ''
        def entrada_menu(id_curso):
            if self.id_curso != id_curso:
                if self.menu is not None: self.menu.pack_forget()
                self.menu = CursoProfesorMenu(self.__frame_profesor, id_curso, instructor)
                self.menu.pack()
                self.id_curso = id_curso
        # Verifica que hayan cursos asignados
        if len(data.instructors[instructor.user_id]['courses']) > 0:
            for courses_id in data.instructors[instructor.user_id]['courses']:
                scroll_curso = tk.Frame(self.scr_courses.scr_frame, bg=blanco_hueso, highlightthickness=3,
                                           highlightbackground=blanco_gris_azul)
                self.scr_courses.pack_on_scroll(scroll_curso,  fill="x", pady=10, padx=2)
                # BOTON CURSOS
                boton_scroll = tk.Button(scroll_curso, text=str(data.courses[courses_id]['course_name']),cursor='hand2', width=15,
                                         font=(font, 39), bg=blanco_gris_azul_clarito)
                boton_scroll.pack(fill='x')
                tk.Label(scroll_curso,
                         text=f"{str(courses_id)} - {str(data.instructors[data.courses[courses_id]['teacher']]['name'])}",
                         font=(font, 17), anchor='center', bg=blanco_gris_azul_clarito).pack(fill='x')
                boton_scroll.config(command=lambda c=courses_id: entrada_menu(c))
        else:
            scroll_curso = tk.Frame(self.scr_courses.scr_frame, bg=blanco_hueso, highlightthickness=3, highlightbackground=blanco_hueso)
            self.scr_courses.pack_on_scroll(scroll_curso, fill='x', padx=7, pady=20)
            tk.Label(scroll_curso,
                     text='No hay cursos asignados ☹ \n ¡Recuerda crear un curso!',
                     font=(font, 25, 'bold')).pack()

        def crear_curso():
            self.create_curse = tk.Toplevel(self.master, width=1000, height=750, bg=azul_claro)
            self.create_curse.resizable(False)
            self.create_curse.pack_propagate(False)
            texto_crear_curso = tk.Label(self.create_curse, text='Crear curso', font=(font, 20, 'bold'), fg='white', bg=azul_claro)
            texto_crear_curso.pack()

            nombre_curso = tk.Entry(state= 'normal')
            nombre_curso = pack_create_line(self.create_curse, tk.Label, {'text': 'Nombre:      ',  'fg':'black', 'font':(font, 25, 'bold'), 'justify':'left','bg':'white'})

            self.boton_crear = tk.Button(self.create_curse, text='Crear curso', font=(font, 25, 'bold'), fg= fg, width=wid, bg='red', activebackground='blue')
            self.boton_crear.pack(pady=50)

        def exit_(): self.change_page(parent)
        tk.Button(self.__frame_info, text='x', width=3, height=1, command=exit_, font=(font, 20, 'bold'), bg=azul_claro, relief='flat', cursor='hand2').pack(side="right", padx=50)

    # Me hace falta poner el logo
class CursoProfesorMenu(tk.Frame):
    def __init__(self, master, course_id, user: Instructor, **kwargs):
        super().__init__(master=master, width=(1920 - 50), height=(1080 - 10), **kwargs)
        self.course_id = course_id
        self.total_puntos_curso = 0
        self.pack_propagate(False)
        self.frame_curso = tk.Frame(self, width=(1920 - 50), height=(1080 - 200 - 700), bg='#A0503B')
        self.frame_curso.pack_propagate(False)
        self.frame_curso.pack()
        tk.Label(self.frame_curso, text=f"{data.courses[course_id]['course_name']}",bg='#A0503B', fg='white',
                 font=(font, 60, 'bold')).pack(side='left', padx=50)
        tk.Label(self.frame_curso, text=f'{course_id}', font=(font, 35, 'bold'),bg='#A0503B',fg='white').pack(side='right', padx=50)

        self.frame_portal = tk.Frame(self, width=(1920 - 50), height=(1080 - 200 - 700), bg='#AB9784')
        self.frame_portal.pack_propagate(False)
        self.frame_portal.pack()

        def examen(): pass

        def tarea():
            self.top_level = tk.Toplevel(self.master, width=1000, height=700, bg=blanco_hueso)
            self.top_level.resizable(False, False)
            self.top_level.grab_set()

            tk.Label(self.top_level, text='Ingresa un nombre a la tarea', font=('Arial', 30, 'bold'), width=35,bg=blanco_hueso).pack(pady=20)
            inf = tk.Label(self.top_level, text='',
                           font=('Arial', 15, 'bold'), bg=blanco_hueso)
            inf.pack(pady=10)
            e_tit = tk.Entry(self.top_level, font=('Arial', 30))
            e_tit.pack(pady=5, padx=20)

            tk.Label(self.top_level, text='Ingresa una descripción', font=('Arial', 20, 'bold'),
                     bg=blanco_hueso).pack(pady=10)
            e_desc = tk.Text(self.top_level, font=('Arial', 16), width=40, height=10)
            e_desc.pack(pady=10)

            def solo_numeros(event):
                if event.char.isdigit() or event.keysym in ('BackSpace', 'Delete', 'Left', 'Right'):
                    return None
                else:
                    return "break"

            tk.Label(self.top_level, text='Ingresa un punteo', font=('Arial', 12, 'bold'),bg=blanco_hueso).pack(pady=10)
            e_pu = tk.Entry(self.top_level, font=('Arial', 20, 'bold'), width=5)
            e_pu.pack(pady=10)
            e_pu.bind("<KeyPress>", solo_numeros)

            def crear_t():
                c = Courses(data.courses[course_id]['course_name'], course_id)
                if e_tit.get().strip() != '' and e_desc.get('1.0', tk.END).strip() != '' and e_pu.get().strip() != '' and int(e_pu.get())+self.total_puntos_curso<=100 and int(e_pu.get()) >0:
                    c.assign_homework(e_tit.get(), e_desc.get('1.0', tk.END), e_pu.get())
                    self.portal()
                    self.top_level.destroy()

                elif e_tit.get().strip() == '': inf.config(text='EL título no puede estar vacio')
                elif e_desc.get('1.0', tk.END).strip() == '': inf.config(text='La descripcion no puede estar vacia')
                elif e_pu.get().strip() == '': inf.config(text='No hay punteo')
                elif int(e_pu.get())+self.total_puntos_curso>100:inf.config(text='Sobrepasaste el punteo maximo de 100!!')
                elif  int(e_pu.get()) < 0:inf.config(text='Punteo negativo!!!')

            n = tk.Button(self.top_level, text='Crear', font=('Arial', 20), command=crear_t)
            n.pack(pady=10)

        def publi():

            self.top_level = tk.Toplevel(self.master, width=1000, height=700, bg=blanco_hueso)
            self.top_level.resizable(False, False)
            self.top_level.grab_set()

            tk.Label(self.top_level, text='Ingresa un nombre a la tarea', font=('Arial', 30, 'bold'), width=35,
                     bg=blanco_hueso).pack(pady=20)
            inf = tk.Label(self.top_level, text='',
                           font=('Arial', 15, 'bold'), bg=blanco_hueso)
            inf.pack(pady=10)
            e_tit = tk.Entry(self.top_level, font=('Arial', 30))
            e_tit.pack(pady=5, padx=20)

            tk.Label(self.top_level, text='Ingresa una descripción', font=('Arial', 20, 'bold'),
                     bg=blanco_hueso).pack(pady=10)
            e_desc = tk.Text(self.top_level, font=('Arial', 16), width=40, height=10)
            e_desc.pack(pady=10)

            def crear_t():
                c = Courses(data.courses[course_id]['course_name'], course_id)
                if e_tit.get().strip() != '' and e_desc.get('1.0',
                                                            tk.END).strip() != '':
                    c.assign_publish(e_tit.get(), e_desc.get('1.0', tk.END))
                    self.portal()
                    self.top_level.destroy()

                elif e_tit.get().strip() == '':
                    inf.config(text='EL título no puede estar vacio')
                elif e_desc.get('1.0', tk.END).strip() == '':
                    inf.config(text='La descripcion no puede estar vacia')

            n = tk.Button(self.top_level, text='Crear', font=('Arial', 20), command=crear_t)
            n.pack(pady=10)

        def check():
            self.master.master.change_page(CheckHomework(self.master.master.master, Courses(data.courses[course_id]['course_name'], course_id), user, self.master.master))

        tk.Button(self.frame_portal, text='Crear\ntarea', font=(font, 30, 'bold'), bg='#242182', fg='white', width=10, cursor='hand2', command=tarea).pack(side='left', padx=160)
        stu = tk.Button(self.frame_portal, text='Calificar', font=(font, 30, 'bold'), bg='#24822C', fg='white', width=10, disabledforeground='#B4BCB1', command=check)
        stu.pack(side='left', padx=20)
        #if data.courses[course_id]['students']: stu.config(state='normal')
        #else: stu.config(state='disabled')
        tk.Button(self.frame_portal, text='Añadir una\npublicación', font=(font, 30, 'bold'), bg='#823735', fg='white', width=10, cursor='hand2', command=publi).pack(side='right', padx=160)

        self.scroll_curso = ScrollFrame(self, width=(1920 - 50), height=500, bg=blanco_hueso, vbar_position='right')
        self.scroll_curso.pack_propagate(False)
        self.scroll_curso.pack()

        self.portal()
    def portal(self):
        self.total_puntos_curso = 0
        course_material = data.courses[self.course_id]['material']
        for id_,hw in course_material.items():
            if id_[:3] == 'HOM':
                self.total_puntos_curso += int(hw['points'])
        print(self.total_puntos_curso)
        for w in self.scroll_curso.scr_frame.winfo_children():
            w.pack_forget()

        if len(list(data.courses[self.course_id]['material'].items())) > 0:
            for id_publish, publish in reversed(list(data.courses[self.course_id]['material'].items())):
                frame_hmw = tk.Frame(self.scroll_curso.scr_frame, width=(1920 - wid - 100), height=1000)
                frame_hmw.pack_propagate(False)
                match id_publish[:3]:
                    case 'HOM':
                        f_top = tk.Frame(frame_hmw, bg='#9E9AE9')
                        f_top.pack(side='top', fill='x')
                        tk.Button(f_top, text=f"{publish['tittle']}", font=(font, 50, 'bold'),bg='#9E9AE9', anchor='w',
                                  relief='flat', highlightthickness=0, bd=0, width=10).pack(fill='x', anchor='w',
                                                                                            expand=1, side='left',
                                                                                            padx=30)
                        tk.Label(f_top, text=f"{id_publish} - {publish['points']}pts", font=(font, 10, 'bold'), bg='#9E9AE9',
                                 anchor='e').pack(fill='x', anchor='e', expand=1, side='right', padx=30)
                        l = tk.Frame(frame_hmw, borderwidth=10, width=(1920 - 10), height=3, bg='black')
                        l.pack_propagate(False)
                        l.pack(side='top')
                        e = tk.Text(frame_hmw, font=(font, 20, 'bold'), height=3)
                        e.insert(tk.END, f"{publish['description']}")
                        e.config(state='disabled')
                        e.pack(fill='both', anchor='w', expand=1, side='top', padx=20)
                    case 'PLH':
                        frame_hmw.pack_propagate(True)
                        f_top = tk.Frame(frame_hmw)
                        f_top.pack(side='top', fill='x')
                        tk.Label(f_top, text=f"{publish['tittle']}", font=(font, 50, 'bold'), anchor='w').pack(fill='x',
                                                                                                               anchor='w',
                                                                                                               expand=1,
                                                                                                               side='left',
                                                                                                               padx=30)
                        tk.Label(f_top, text=f"{id_publish}", font=(font, 10, 'bold'), anchor='e').pack(fill='x',
                                                                                                        anchor='e',
                                                                                                        expand=1,
                                                                                                        side='right',
                                                                                                        padx=30)
                        l = tk.Frame(frame_hmw, borderwidth=10, width=(1920 - wid - 100), height=2, bg='black')
                        l.pack(side='top')
                        e = tk.Text(frame_hmw, font=(font, 20, 'bold'), height=3, width=10)
                        e.insert(tk.END, f"{publish['description']}")
                        e.config(state='disabled', height=int(e.index('end-1c').split('.')[0]))
                        e.pack(fill='x', anchor='w', expand=1, side='bottom', padx=20)

                self.scroll_curso.pack_on_scroll(frame_hmw, padx=50, pady=30)
        else:
            frame_no = tk.Frame(self.scroll_curso.scr_frame, width=1920, height=500, bg=blanco_hueso)
            frame_no.pack_propagate(False)
            self.scroll_curso.pack_on_scroll(frame_no, pady=80)

            tk.Label(frame_no, text='Sin tareas por ahora...', font=(font, 55, 'bold'), bg=blanco_hueso).pack(
                fill='both')
