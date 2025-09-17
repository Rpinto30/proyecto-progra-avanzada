import tkinter as tk
from clases_internas.usuarios import Student, Instructor
from menus.graphic_tools import Window, PagePrincipal, pack_create_line
from data.data_base import data
from tkinter import PhotoImage
from graphic_tools import Tabla


root = Window('Ventana', (1920, 1080))


class StudentNotes(PagePrincipal):
    def __init__(self, master, instructor:Instructor, parent,  **kwargs):
        super().__init__(master=master, bg='white', **kwargs)
        self.instructor = instructor

        self.f_izq = tk.Frame(self, width=1280, height=1080, bg='blue')
        self.f_izq.pack_propagate(False)
        self.f_izq.pack(side='left')

        self.f_der = tk.Frame(self, width=640, height=1080, bg='#FFD09F')
        self.f_der.pack_propagate(False)
        self.f_der.pack(side='right')

        self.b_exit = tk.Button(self.f_der, text='Salir', font=('Arial', 30, 'bold'), fg='black', width=20, bg='red',
                                activebackground='#FF9EA2', cursor='hand2', relief='solid')
        self.b_exit.pack(side="bottom", pady=30)

        def exit_notes():
            self.change_page(parent)

        matrix = self.check_note()



        self.f_table = Tabla(self.f_izq, matrix=matrix, propagate_width=4, cell_width=35, cell_height=3,
                             color_table='white', color_header='#FFAF8A', vbar_position='left')
        for n, row in enumerate(matrix):
            for n1, cell in enumerate(row):
                if n > 0 and n1 == len(matrix[0])-2:
                    print(cell)
                    if int(cell) < 65:
                        self.f_table.confi_cell((n, n1))


        self.f_table.pack(side='left', fill='y')



    def check_note(self):
        table = [['Estudiante', 'ID', 'Nota', 'Nota Acumulada']]
        for course_id in data.instructors[self.instructor.user_id]['courses']:
            for student_id in data.courses[course_id]['students']:
                name = data.students[student_id]['name']
                total, note = 0, 0
                for id_homework, homework in data.courses[course_id]['material'].items():
                    if data.students[student_id]['material'][id_homework]['course'] == course_id:
                        total += int(homework["points"])
                        note += int(data.students[student_id]['material'][id_homework]["obtained_points"])
                table.append([name, student_id, note, total])
        return table


student = StudentNotes(root, Instructor('Milton Nimatuj', '123', 'IST'), None)
root.mainloop()
