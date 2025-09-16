import tkinter as tk
from graphic_tools import Window, PagePrincipal, ScrollFrame
from clases_internas.usuarios import Student
from data.data_base import data

root = Window('Test', (1920,1080))

CL_BG = '#669BBC'
CL_BG_L = '#669BBC'
CL_BG_R = '#003949'
CL_BG_LT = '#4F3A92'
CL_BG_LM = '#4D18B0'
CL_BD_LM = '#071E29'
CL_BG_SCR_L = '#4B73CE'


CL_SCROLL_BG = '#0F0E38'
CL_SCOLL = '#FFFFFF'

FONT = 'Arial'
FG_LT = '#FDF0D5'

WID_F_L = 480



class StudentMenu(PagePrincipal):
    def __init__(self, master:Window, student:Student, **kwargs):
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
                                       width=WID_F_L, height=(1080-590), vbar_position='left', cl_bars_bg=CL_SCROLL_BG, cl_bars_tro=CL_SCOLL, bg=CL_BG_SCR_L)
        self.scr_courses.pack()

        for courses_id in data.students[student.user_id]['courses']:
            f_course_scroll = tk.Frame(self.scr_courses.scr_frame, bg=CL_BG_SCR_L,highlightthickness=3, highlightbackground='#0D0C2D')
            self.scr_courses.pack_on_scroll(f_course_scroll, pady=10)
            tk.Label(f_course_scroll, text=str(data.courses[courses_id]['course_name']), font=(FONT, 40), anchor='center', width=14, bg=CL_BG_SCR_L).pack( fill='x',padx=10)
            tk.Label(f_course_scroll, text=str(courses_id), font=(FONT, 10), anchor='center', width=14, bg=CL_BG_SCR_L).pack(fill='x',padx=10)

        #RIGHT FRAME
        self.__f_info_right = tk.Frame(self, width=(1920 - WID_F_L), height=1080, bg=CL_BG_R)
        self.__f_info_right.pack_propagate(False)
        self.__f_info_right.pack(side='right')




S = StudentMenu(root, Student('Pepito', '123', 'STU123'))

root.mainloop()