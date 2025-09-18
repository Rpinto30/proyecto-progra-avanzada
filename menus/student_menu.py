import tkinter as tk
from graphic_tools import Window, Page, PagePrincipal, ScrollFrame
from clases_internas.usuarios import Student
from clases_internas.cursos import Courses
from data.data_base import data
from tkinter import PhotoImage

root = Window('Test', (1920,1080))

CL_BG = '#669BBC'
CL_BG_L = '#669BBC'
CL_BG_R = '#003949'
CL_BG_LT = '#4F3A92'
CL_BG_LM = '#4D18B0'
CL_BD_LM = '#071E29'
CL_BG_SCR_L = '#4B73CE'
CL_BG_BT_C = '#8D6DB7'
CL_BG_RB = '#1A7789'

CL_SCROLL_BG = '#2E2E39'
CL_SCOLL = '#FFFFFF'
CL_SCOLL_AC = '#C8D3E9'

FONT = 'Arial'
FG_LT = '#FDF0D5'

WID_F_L = 480

class StudentMenu(PagePrincipal):
    def __init__(self, master, student:Student, parent, **kwargs):
        super().__init__(master, bg=CL_BG, **kwargs)
        #LEFT FRAME
        self.__f_info_left = tk.Frame(self, width=WID_F_L, height=1080, bg=CL_BG_L)
        self.__f_info_left.pack_propagate(False)
        self.__f_info_left.pack(side='left')

        #Frame para poner información del estudiante
        self.__f_info_top_left = tk.Frame(self.__f_info_left, width=WID_F_L, height=250, bg=CL_BG_LT)
        self.__f_info_top_left.pack_propagate(False)
        self.__f_info_top_left.pack()
        #PARA COLOCAR ESTUDIANTE Y SU NOMBRE
        f_top_top_left = tk.Frame(self.__f_info_top_left, bg=CL_BG_LT)
        f_top_top_left.pack(pady=50)
        tk.Label(f_top_top_left, text='Estudiante', font=(FONT, 60, 'bold'), anchor='w', bg=CL_BG_LT, fg=FG_LT).pack(padx=35, fill='x', pady=10)
        tk.Label(f_top_top_left, text=f'{student.name} ({student.user_id})', font=(FONT, 25,'bold'), anchor='w', bg=CL_BG_LT, fg=FG_LT).pack(padx=35, fill='x')

        self.__c_lable_courses = tk.Canvas(self.__f_info_left, width=WID_F_L, height=100, bg=CL_BG_LM, highlightthickness=0, bd=0)
        self.__c_lable_courses.create_line(10, 0, WID_F_L-10, 0, fill=CL_BD_LM, width=10)
        self.__c_lable_courses.create_line(10, 100, WID_F_L-10, 100, fill=CL_BD_LM, width=10)
        self.__c_lable_courses.pack()
        self.__c_lable_courses.create_window(WID_F_L//2, 100//2,
                                             window=tk.Label(self.__c_lable_courses, text='Cursos', bg=CL_BG_LM, fg='#ffffff', font=(FONT, 30, 'bold')))

        self.scr_courses = ScrollFrame(self.__f_info_left,
                                       width=WID_F_L, height=(1080-500), vbar_position='left', cl_bars_bg=CL_SCROLL_BG, cl_bars_des=CL_SCOLL, cl_bars_act=CL_SCOLL_AC, bg=CL_BG_SCR_L)
        self.scr_courses.pack()
        #BOTON ASIGNARSE
        tk.Button(self.__f_info_left, text='Asignarse a curso', font=(FONT, 37, 'bold')).pack(pady=15)
        #SCROLL BOTONES

        self.__f_info_right = tk.Frame(self, width=(1920 - WID_F_L), height=1080, bg=CL_BG_R)
        self.__f_info_right.pack_propagate(False)
        self.__f_info_right.pack(side='right')

        self.menu_c, self.id_in_course = None, ''
        def entry_menu_course(id_course):
            if self.id_in_course != id_course:
                if self.menu_c is not None: self.menu_c.pack_forget()
                self.menu_c = StudentMenuCourse(self.__f_info_right, id_course, student)
                self.menu_c.pack()
                self.id_in_course = id_course

        if len(data.students[student.user_id]['courses']) > 0:
            for courses_id in data.students[student.user_id]['courses']:
                f_course_scroll = tk.Frame(self.scr_courses.scr_frame, bg=CL_BG_SCR_L,highlightthickness=3, highlightbackground='#0D0C2D')
                self.scr_courses.pack_on_scroll(f_course_scroll, pady=10, fill='x',padx=2)
                b = tk.Button(f_course_scroll, text=str(data.courses[courses_id]['course_name']), font=(FONT,39), width=15, bg=CL_BG_BT_C)
                b.pack( fill='x')
                tk.Label(f_course_scroll, text=f"{str(courses_id)} - {str(data.instructors[data.courses[courses_id]['teacher']]['name'])}", font=(FONT, 17), anchor='center',bg=CL_BG_SCR_L).pack(fill='x')
                b.config(command = lambda c=courses_id: entry_menu_course(c))
        else:
            f_course_scroll = tk.Frame(self.scr_courses.scr_frame, bg=CL_BG_SCR_L, highlightthickness=3, highlightbackground='#0D0C2D')
            self.scr_courses.pack_on_scroll(f_course_scroll, fill='x', padx=7, pady=20)
            tk.Label(f_course_scroll, text='No hay cursos asignados :c\n¡Asignate a un curso\npara iniciar tu aventura!', font=(FONT,25,'bold')).pack()
        #RIGHT FRAME


        self.__f_top_right = tk.Frame(self.__f_info_right, width=(1920 - WID_F_L), height=200, bg=CL_BG_RB)
        self.__f_top_right.pack_propagate(False)
        self.__f_top_right.pack(side='top')

        def exit_(): print('Salir')#self.change_page(parent)
        tk.Button(self.__f_top_right, text='→', width=3, height=0, command=exit_, font=(FONT, 50, 'bold'), bg='#8292CB', relief='flat').pack(side="right", padx=50)

        logo = PhotoImage(file=r'sources/Logo_iso_stu.png', width=199, height=200)
        logo_photo = tk.Label(self.__f_top_right, image=logo, highlightthickness=0, bd=0)
        logo_photo.image = logo
        logo_photo.pack(side='left',padx=30)

CL_BG_C = "#9DCBBD"
CL_BG_C_T = '#FFFFFF'

class StudentMenuCourse(tk.Frame):
    def __init__(self, master, course_id:str, student:Student, **kwars):
        super().__init__(master=master, width=(1920 - WID_F_L), height=(1080-200),bg=CL_BG_C,**kwars)
        self.pack_propagate(False)
        self.f_top = tk.Frame(self, width=(1920 - WID_F_L), height=(1080-200-700), bg=CL_BG_C_T)
        self.f_top.pack_propagate(False)
        self.f_top.pack()
        tk.Label(self.f_top, text=f'{data.courses[course_id]['course_name']}', font=(FONT, 60, 'bold')).pack(side='left', padx=50)
        tk.Label(self.f_top, text=f'{course_id}  -  {data.instructors[data.courses[course_id]['teacher']]['name']}', font=(FONT, 35, 'bold')).pack(side='right', padx=50)

        self.f_down = ScrollFrame(self, width=(1920 - WID_F_L), height=(1080-200), bg=CL_BG_C, vbar_position='right')
        self.f_down.pack_propagate(False)
        self.f_down.pack()

        for id_publish, publish in reversed(list(data.courses[course_id]['material'].items())): #Invierto para tener lo más 'reciente'
            frame_publish = tk.Frame(self.f_down.scr_frame, width=(1920 - WID_F_L-100), height=200)
            frame_publish.pack_propagate(False)
            print(id_publish)
            match id_publish[:3]:
                case 'HOM':
                    f_top = tk.Frame(frame_publish)
                    f_top.pack(side='top', fill='x')
                    tk.Button(f_top, text=f"{publish['tittle']}", font=(FONT,50,'bold'), anchor='w', relief='flat', highlightthickness=0, bd=0, cursor='hand2', width=28).pack(fill='x', anchor='w', expand=1, side='left', padx=30)
                    tk.Label(f_top, text=f"{id_publish}", font=(FONT,10,'bold'), anchor='e').pack(fill='x', anchor='e', expand=1, side='right', padx=30)
                    l = tk.Frame(frame_publish, borderwidth=10, width=(1920 - WID_F_L-100), height=2, bg='black')
                    l.pack_propagate(False)
                    l.pack(side='top')
                    e = tk.Text(frame_publish, font=(FONT,20,'bold'), height=3)
                    e.insert(tk.END, f"{publish['description']}")
                    e.config(state='disabled')
                    e.pack(fill='x', anchor='w', expand=1, side='bottom', padx=20)
                case 'PLH':
                    frame_publish.pack_propagate(True)
                    f_top = tk.Frame(frame_publish)
                    f_top.pack(side='top', fill='x')
                    tk.Label(f_top, text=f"{publish['tittle']}", font=(FONT, 50, 'bold'), anchor='w').pack(fill='x', anchor='w', expand=1,side='left', padx=30)
                    tk.Label(f_top, text=f"{id_publish}", font=(FONT, 10, 'bold'), anchor='e').pack(fill='x', anchor='e',expand=1, side='right',padx=30)
                    l = tk.Frame(frame_publish, borderwidth=10, width=(1920 - WID_F_L - 100), height=2, bg='black')
                    l.pack(side='top')
                    e = tk.Text(frame_publish, font=(FONT, 20, 'bold'), height=3)
                    e.insert(tk.END, f"{publish['description']}")
                    e.config(state='disabled', height= int(e.index('end-1c').split('.')[0]))
                    e.pack(fill='x', anchor='w', expand=1, side='bottom', padx=20)
            self.f_down.pack_on_scroll(frame_publish, padx=50, pady=30)




S = StudentMenu(root, Student('Pepito', '123', 'STU123'), None)

root.mainloop()