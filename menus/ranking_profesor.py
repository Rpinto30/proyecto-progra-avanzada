import tkinter as tk
from clases_internas.usuarios import  Instructor
from menus.graphic_tools import  Page
from data.data_base import data
from tkinter import PhotoImage
from graphic_tools import Tabla



class StudentNotes(Page):
    def __init__(self, master, instructor:Instructor, course_id, parent,  **kwargs):
        super().__init__(master=master, bg='white', **kwargs)
        self.course_id = course_id
        self.instructor = instructor

        self.f_izq = tk.Frame(self, width=1280, height=1080, bg='blue')
        self.f_izq.pack_propagate(False)
        self.f_izq.pack(side='left')

        self.f_der = tk.Frame(self, width=640, height=1080, bg='#FFD09F')
        self.f_der.pack_propagate(False)
        self.f_der.pack(side='right')

        def exit_notes():
            self.change_page(parent)
        self.b_exit = tk.Button(self.f_der, text='Salir', font=('Arial', 30, 'bold'), fg='black', width=20, bg='red',
                                activebackground='#FF9EA2', cursor='hand2', relief='solid', command=exit_notes)
        self.b_exit.pack(side="bottom", pady=30)

        logo = PhotoImage(file=r'sources/Logo_iso_stu_ranking.png', width=400, height=400)
        logo_photo = tk.Label(self.f_der, image=logo, highlightthickness=0, bd=0)
        logo_photo.image = logo
        logo_photo.pack(side='top', padx=30,pady=30)

        self.l = tk.Label(self.f_der, text='Los estudiantes con\nnota en rojo son\naquellos estudiantes que\naún no llegan a la\nzona mínima', font=('Arial', 30, 'bold'), fg='#24105F', width=20, bg='#FFD09F')
        self.l.pack(side="top", pady=50)



        matrix = self.check_note()


        self.f_table = Tabla(self.f_izq, matrix=matrix, propagate_width=4, cell_width=35, cell_height=3,
                             color_table='white', color_header='#FFAF8A', vbar_position='left', bg='#8989A8')
        for n, row in enumerate(matrix):
            for n1, cell in enumerate(row):
                if n > 0 and n1 == len(matrix[0])-2:
                    print(cell)
                    if int(cell) < 65:
                        self.f_table.confi_font_cell((n, n1))


        self.f_table.pack(side='left', fill='y')

    def check_note(self):
        table = [['Estudiante', 'ID', 'Nota', 'Nota Acumulada']]
        for student_id in data.courses[self.course_id]['students']:
            if self.course_id in data.students[student_id]['courses']:
                print(student_id)
                name = data.students[student_id]['name']
                total, note = 0, 0
                for id_homework, homework in data.courses[self.course_id]['material'].items():
                    if id_homework[:3] == 'HOM':
                        if data.students[student_id]['material'][id_homework]['course'] == self.course_id:
                            total += int(homework["points"])
                            note += int(data.students[student_id]['material'][id_homework]["obtained_points"])
                table.append([name, student_id, note, total])
        return table
