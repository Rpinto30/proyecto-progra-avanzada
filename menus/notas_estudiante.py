import tkinter as tk
from clases_internas.usuarios import Student
from menus.graphic_tools import Window, PagePrincipal, pack_create_line
from data.data_base import data
from tkinter import PhotoImage
from tkinter.ttk import Scrollbar
from graphic_tools import Tabla

root = Window('Ventana', (1920, 1080))


class StudentNotes(PagePrincipal):
    def __init__(self, master, student:Student, parent,  **kwargs):
        super().__init__(master=master, bg='#007CFF', **kwargs)
        self.student = student

        self.f_top_der = tk.Frame(self, width=960, height=200, bg='#4A49FF')
        self.f_top_der.pack_propagate(False)
        self.f_top_der.pack(side='top')

        self.f_main = tk.Frame(self, width=1920, height=900, bg='#F2EEED')
        self.f_main.pack_propagate(False)
        self.f_main.pack(side="right")

        self.f_table = Tabla(self.f_main, matrix=self.check_note(), propagate_width=3, cell_width=50, cell_height=3,
                             color_table='white', color_header='#8EE7FF', vbar_position='left')
        #self.f_table.confi_colum(index=0, width_=30)
        #self.f_table.confi_colum(index=1, width_=30)
        #self.f_table.confi_colum(index=2, width_=30)
        self.f_table.pack(side='left', fill='y')


        photo = PhotoImage(file=r"sources/logo_notas.png", width=960, height=200)
        logo = tk.Label(self.f_top_der, image=photo, highlightthickness=0, bd=0)
        logo.image = photo
        logo.pack()

        self.b_exit = tk.Button(self.f_main, text='Salir', font=('Arial', 30, 'bold'), fg='black', width=20, bg='red', activebackground='#FF9EA2', cursor='hand2', relief='solid')
        self.b_exit.pack(side="bottom")

        def exit_notes():
            self.change_page(parent)


    def check_note(self):
        table = [['Curso', 'Nota', 'Nota Acumulada']]
        for courses_id in data.students[self.student.user_id]['courses']:
            total, note = 0, 0
            for id_homework,  homework in data.courses[courses_id]['material'].items():
                if data.students[self.student.user_id]['material'][id_homework]['course'] == courses_id:
                    total += int(homework["points"])
                    note += int(data.students[self.student.user_id]['material'][id_homework]["obtained_points"])
            table.append([data.courses[courses_id]["course_name"], note, total])
        return table





student = StudentNotes(root, Student('Pepito', '123', 'STU123'), None)
root.mainloop()



