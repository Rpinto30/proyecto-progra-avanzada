import tkinter as tk
from clases_internas.usuarios import Student
from menus.graphic_tools import Page
from data.data_base import data
from tkinter import PhotoImage
from graphic_tools import Tabla




class StudentNotes(Page):
    def __init__(self, master, student:Student, parent,  **kwargs):
        super().__init__(master=master, bg='#FFE6CF', **kwargs)
        self.student = student

        self.f_top_der = tk.Frame(self, width=960, height=200, bg='#FFE6CF')
        self.f_top_der.pack_propagate(False)
        self.f_top_der.pack(side='top')

        self.f_main = tk.Frame(self, width=1920, height=900, bg='#FFE6CF')
        self.f_main.pack_propagate(False)
        self.f_main.pack(side="right")

        self.f_table = Tabla(self.f_main, matrix=self.check_note(), propagate_width=3, cell_width=50, cell_height=3,
                             color_table='white', color_header='#007CFF', vbar_position='left', bg='white')
        self.f_table.pack(side='left', fill='y')



        logo = PhotoImage(file=r'sources/Logo_iso_stu_NOTES2.png', width=400, height=400)
        logo_photo = tk.Label(self.f_main, image=logo, highlightthickness=0, bd=0)
        logo_photo.image = logo
        logo_photo.pack(side='top', padx=30, pady=30)

        self.l = tk.Label(self.f_main,
                          text='Los grandes esfuerzos\ntraen grandes\nrecompensas',
                          font=('Arial', 30, 'bold'), fg='#24105F', width=20, bg='#FFE6CF')
        self.l.pack(side="top", pady=50)

        def exit_notes(): self.change_page(parent)
        self.b_exit = tk.Button(self.f_main, text='Salir', font=('Arial', 30, 'bold'), fg='white', width=20, bg='#FF111D', activebackground='#FF0311', cursor='hand2', relief='solid', command=exit_notes)
        self.b_exit.pack(side="bottom")




    def check_note(self):
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

