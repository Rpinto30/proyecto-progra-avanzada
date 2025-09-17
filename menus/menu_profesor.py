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

        self.scr_courses = ScrollFrame(self.__barra_profesor,
                                       width=wid, height=(1080 - 450), vbar_position='left',
                                       cl_bars_bg=scroll_bg, cl_bars_des=scroll, cl_bars_act=scroll_ac,
                                       bg=blanco_hueso)
        self.scr_courses.pack()

        self.__barra_materia_boton = tk.Button(self.__barra_profesor, text="Curso", bg=azul_marino, fg=fg, font=font)
        self.__barra_materia_boton.pack(fill="x", pady='250')

        self.__frame_info = tk.Frame(self.__frame_profesor,  width=1920 - 400, height=150, bg=azul_marino)
        self.__frame_info.pack_propagate(False)
        self.__frame_info.pack()

        for course_id in data.instructors[user.user_id]['courses']:
            scroll_curso = tk.Frame(self.scr_courses.scr_frame, bg= 'yellow', highlightthickness=2, highlightbackground='pink')
            self.scr_courses.pack_on_scroll(scroll_curso, pady=10, fill='x',padx=2)
            tk.Button(scroll_curso, text=f"{str(data.courses[course_id]['course_name'])} \n {str(course_id)}" , font=(font, 35), anchor='center', width=14, bg='white').pack(fill='x')

            '''
            tk.Label(scroll_curso, text=str(data.courses[course_id]['course_name']), font=(font, 39), anchor='center', width=14, bg='black').pack(fill='x', padx=10)
            tk.Label(scroll_curso, text=f'{str(course_id)} - {str(data.instructors[data.courses[course_id]['teacher']]['name'])}', font=(font, 14), anchor='center', width=39, bg='black').pack(fill='x', padx=10)
            '''


        def exit_(): print('Salir')#self.change_page(parent)
        tk.Button(self.__frame_info, text='x', width=3, height=1, command=exit_, font=(font, 20, 'bold'), bg=azul_claro, relief='flat').pack(side="right", padx=50)




men = MenuProfesores(root, user=Instructor('Milton Nimatuj', '123', 'IST'))
root.mainloop()