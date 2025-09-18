#Otra vez porque elimine mi archivo anterior por accidente
import tkinter as tk
from graphic_tools import Window, Page, PagePrincipal, ScrollFrame
from clases_internas.usuarios import Instructor
from data.data_base import data
from tkinter import PhotoImage

azul_claro = '#669BBC'
azul_marino = '#003949'
blanco_hueso = '#E1E2D5'

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

        self.__barra_profesor = tk.Frame(self, width=400, height=1080, bg=azul_claro)
        self.__barra_profesor.pack_propagate(False)
        self.__barra_profesor.pack(side='left')
        self.__frame_profesor = tk.Frame(self, width=1920-400, height=1080, bg=blanco_hueso)
        self.__frame_profesor.pack_propagate(False)
        self.__frame_profesor.pack(side='right')

        frame__colocar_info = tk.Frame(self.__barra_profesor, bg=azul_claro)
        frame__colocar_info.pack(pady=10)
        tk.Label(frame__colocar_info, text='Profesor', font=(font, 60, 'bold'), anchor='w', bg=azul_claro, fg=fg).pack(padx=35,
                                                                                                               fill='x',
                                                                                                               pady=10)
        tk.Label(frame__colocar_info, text=f'{user.name} ({user.user_id})', font=(font, 25, 'bold'), anchor='w', bg=azul_claro,
                 fg=fg).pack(padx=35, fill='x')

        self.c_lable_courses = tk.Canvas(self.__barra_profesor, width=wid, height=100, bg=azul_marino, highlightthickness=0,
                                         bd=0)
        self.c_lable_courses.create_line(10, 0, wid - 10, 0, fill='black', width=10)
        self.c_lable_courses.create_line(10, 100, wid - 10, 100, fill='black', width=10)
        self.c_lable_courses.pack(fill='x')
        self.c_lable_courses.create_window((wid // 2)-100, 100 // 2,
                                           window=tk.Label(self.c_lable_courses, text='Cursos', bg=azul_marino,
                                                           fg='white', font=(font, 30, 'bold')))
        # Boton de crear curso
        tk.Button(self.__barra_profesor, text='Crear curso', font=(font, 30), anchor='center', width=14, fg=fg,
                  bg=azul_claro).pack(fill='x', side='bottom')

        self.scr_courses = ScrollFrame(self.__barra_profesor,
                                       width=wid, height=(1080 - 200), vbar_position='left',
                                       cl_bars_bg=scroll_bg, cl_bars_des=scroll, cl_bars_act=scroll_ac,
                                       bg=blanco_hueso)
        self.scr_courses.pack()


        self.__barra_materia_boton = tk.Button(self.__barra_profesor, text="Curso", bg=azul_marino, fg=fg, font=font)
        self.__barra_materia_boton.pack(fill="x", pady='250')

        # Frame de arriba
        self.__frame_info = tk.Frame(self.__frame_profesor,  width=1920 - 400, height=150, bg=azul_marino)
        self.__frame_info.pack_propagate(False)
        self.__frame_info.pack()


        self.menu, self.id_curso = None, ''
        def entrada_menu(id_curso):
            if self.id_curso != id_curso:
                if self.menu is not None: self.menu.pack_forget()
                self.menu = CursoProfesorMenu(self.__frame_profesor, id_curso, user)
                self.menu.pack()
                self.id_curso = id_curso
        # Verifica que hayan cursos asignados
        if len(data.instructors[user.user_id]['courses']) > 0:
            for courses_id in data.instructors[user.user_id]['courses']:

                scroll_curso = tk.Frame(self.scr_courses.scr_frame, bg=blanco_hueso, highlightthickness=3,
                                           highlightbackground='white')
                self.scr_courses.pack_on_scroll(scroll_curso, pady=10, fill='x', padx=2)
                boton_scroll = tk.Button(scroll_curso, text=str(data.courses[courses_id]['course_name']),
                                         font=(font, 39),
                                         width=12, bg=blanco_hueso)
                boton_scroll.pack(fill='x')
                tk.Label(scroll_curso,
                         text=f"{str(courses_id)} - {str(data.instructors[data.courses[courses_id]['teacher']]['name'])}",
                         font=(font, 17), anchor='center', bg='white').pack(fill='x')
                boton_scroll.config(command=lambda c=courses_id: entrada_menu(c))
        else:
            scroll_curso = tk.Frame(self.scr_courses.scr_frame, bg=blanco_hueso, highlightthickness=3, highlightbackground='white')
            self.scr_courses.pack_on_scroll(scroll_curso, fill='x', padx=7, pady=20)
            tk.Label(scroll_curso,
                     text='No hay cursos asignados ☹ \n ¡Recuerda crear un curso!',
                     font=(font, 25, 'bold')).pack()
#
        def exit_():
            print('Salir')
        tk.Button(self.__frame_info, text='x', width=3, height=1, command=exit_, font=(font, 20, 'bold'), bg=azul_claro, relief='flat').pack(side="right", padx=50)

    # Me hace falta poner el logo
class CursoProfesorMenu(tk.Frame):
    def __init__(self, master, course_id, user: Instructor, **kwargs):
        super().__init__(master=master, width=(1920 - wid), height=(1080 - 500), bg='white', **kwargs)
        self.pack_propagate(False)
        self.frame_curso = tk.Frame(self, width=(1920 - wid), height=(1080 - 200 - 700), bg='red')
        self.frame_curso.pack_propagate(False)
        self.frame_curso.pack()
        tk.Label(self.frame_curso, text=f"{data.courses[course_id]['course_name']}",
                 font=(font, 60, 'bold')).pack(side='left', padx=50)
        tk.Label(self.frame_curso, text=f'{course_id} - {data.courses[course_id]['teacher']} ', font=(font, 35, 'bold')).pack(side='right', padx=50)

        self.scroll_curso = ScrollFrame(self, width=(1920 - wid), height=(1080-200), bg='black', vbar_position='right')
        self.scroll_curso.pack_propagate(False)
        self.scroll_curso.pack()

        for id_publish, publish in reversed(list(data.courses[course_id]['material'].items())):
            frame_hmw = tk.Frame(self.scroll_curso.scr_frame, width=(1920 - wid -100), height=200)
            frame_hmw.pack_propagate(False)
            print(id_publish)
            match id_publish[:3]:
                case 'HOM':
                    f_top = tk.Frame(frame_hmw)
                    f_top.pack(side='top', fill='x')
                    tk.Button(f_top, text=f"{publish['tittle']}", font=(font,50,'bold'), anchor='w', relief='flat', highlightthickness=0, bd=0, cursor='hand2', width=28).pack(fill='x', anchor='w', expand=1, side='left', padx=30)
                    tk.Label(f_top, text=f"{id_publish}", font=(font,10,'bold'), anchor='e').pack(fill='x', anchor='e', expand=1, side='right', padx=30)
                    l = tk.Frame(frame_hmw, borderwidth=10, width=(1920 - wid -100), height=2, bg='black')
                    l.pack_propagate(False)
                    l.pack(side='top')
                    e = tk.Text(frame_hmw, font=(font,20,'bold'), height=3)
                    e.insert(tk.END, f"{publish['description']}")
                    e.config(state='disabled')
                    e.pack(fill='x', anchor='w', expand=1, side='bottom', padx=20)
                case 'PLH':
                    frame_hmw.pack_propagate(True)
                    f_top = tk.Frame(frame_hmw)
                    f_top.pack(side='top', fill='x')
                    tk.Label(f_top, text=f"{publish['tittle']}", font=(font, 50, 'bold'), anchor='w').pack(fill='x', anchor='w', expand=1,side='left', padx=30)
                    tk.Label(f_top, text=f"{id_publish}", font=(font, 10, 'bold'), anchor='e').pack(fill='x', anchor='e',expand=1, side='right',padx=30)
                    l = tk.Frame(frame_hmw, borderwidth=10, width=(1920 - wid - 100), height=2, bg='black')
                    l.pack(side='top')
                    e = tk.Text(frame_hmw, font=(font, 20, 'bold'), height=3)
                    e.insert(tk.END, f"{publish['description']}")
                    e.config(state='disabled', height= int(e.index('end-1c').split('.')[0]))
                    e.pack(fill='x', anchor='w', expand=1, side='bottom', padx=20)

        self.scroll_curso.pack_on_scroll(frame_hmw, padx=50, pady=30)

men = MenuProfesores(root, user=Instructor('Milton Nimatuj', '123', 'IST'))
root.mainloop()