import tkinter as tk
from graphic_tools import Window, Page, PagePrincipal, ScrollFrame, Tabla
from clases_internas.usuarios import Student
from clases_internas.cursos import Courses
from data.data_base import data
from tkinter import PhotoImage
from tkinter import filedialog
from tkinter import messagebox
import os

root = Window('Test_send', (1920,1080))
CL_BG = '#eae2b7'
CL_BG_L = '#f77f00'
CL_BG_TOP_L = '#73232F'
CL_BG_R = '#7FA2D3'
CL_BG_LC = '#fcbf49'
FONT = 'Arial'

H_LEFT = 1000

class CheckHomework(PagePrincipal):
    def __init__(self, master, student:Student, course: Courses, material_id, parent, **kwargs):
        super().__init__(master, bg=CL_BG, **kwargs)

        self.f_left = tk.Frame(self, bg=CL_BG_L, width=1300, height=1080)
        self.f_left.pack_propagate(False)
        self.f_left.pack(side='left')

        self.f_lt = tk.Frame(self.f_left, bg=CL_BG_TOP_L, width=1300, height=(1080-H_LEFT))
        self.f_lt.pack_propagate(False)
        self.f_lt.pack(side='top')

        self.f_l_hom = tk.Frame(self.f_left, bg=CL_BG_LC, width=1300, height=H_LEFT)
        self.f_l_hom.pack_propagate(False)
        self.f_l_hom.pack(side='bottom')

        self.f_r = tk.Frame(self, bg=CL_BG_R, width=(1920-1300), height=1080)
        self.f_r.pack_propagate(False)
        self.f_r.pack()

        tk.Label(self.f_l_hom, text=f'Tarea de {student.name}:', font=(FONT, 70, 'bold'), anchor='w').pack(side='top', fill='x', pady=50,padx=50)

        self.t_hom = tk.Text(self.f_l_hom, height=40, width=70, font=(FONT, 20))
        self.t_hom.insert(tk.END, data.students[student.user_id]['material'][material_id]['homework'])
        self.t_hom.config(state='disabled')
        self.t_hom.pack()

        self.update_idletasks()

    def student_homework(self):
        table = [['Curso', 'Nota', 'Nota Acumulada']]
        for courses_id in data.students[self.student.user_id]['courses']:
            total, note = 0, 0
            for id_homework,  homework in data.courses[courses_id]['material'].items():
                if id_homework[:3] == 'HOM':
                    if data.students[self.student.user_id]['material'][id_homework]['course'] == courses_id:
                        total += int(homework["points"])
                        note += int(data.students[self.student.user_id]['material'][id_homework]["obtained_points"])
            table.append([data.courses[courses_id]["course_name"], note, total])
        return table

s = CheckHomework(root, Student('Pepito', '123', 'STU123'), Courses('Programación', 'SUB4354'), 'HOM4', parent= None)
root.mainloop()