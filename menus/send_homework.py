import tkinter as tk
from graphic_tools import Window, Page, PagePrincipal, ScrollFrame, Tabla
from clases_internas.usuarios import Student
from clases_internas.cursos import Courses
from clases_internas.material import Homework
from data.data_base import data
from tkinter import PhotoImage
from tkinter import filedialog
from tkinter import messagebox
import os

root = Window('Test_send', (1920,1080))
CL_BG = '#eae2b7'
CL_BG_TOP = '#f77f00'
CL_BG_SEND = '#fcbf49'
FONT = 'Arial'

class SendHomework(PagePrincipal):
    def __init__(self, master, student:Student, course: Courses, material_id, parent, **kwargs):
        super().__init__(master, bg=CL_BG, **kwargs)

        self.file, self.homw = None, data.students[student.user_id]['material'][material_id]['homework']
        print(self.homw)
        self.f_top = tk.Frame(self, width=1920, height=200, bg=CL_BG_TOP)
        self.f_top.pack_propagate(False)
        self.f_top.pack(side='top')
        self.f_down = tk.Frame(self, width=1920, height=(1080-200), bg=CL_BG)
        self.f_down.pack_propagate(False)
        self.f_down.pack(side='bottom')
        def exit_(): self.change_page(parent)
        tk.Button(self.f_top, text='←', width=3, height=1, command=exit_, font=(FONT,70, 'bold'), bg=CL_BG_TOP, relief='flat', fg='white').pack(side="left", padx=20)

        #TOP
        self.f_top_info = tk.Frame(self.f_top, bg=CL_BG_TOP)
        self.f_top_info.pack(side="left")
        tk.Label(self.f_top_info, text=f'{course.course_name} - {course.course_id}', anchor='w', font=(FONT, 50, 'bold'), bg=CL_BG_TOP, fg='white').pack(anchor='w')
        tk.Label(self.f_top_info, text=f'Primer Semestre  -  {data.instructors[data.courses[course.course_id]["teacher"]]['name']}', anchor='w', font=(FONT, 20, 'bold'), bg=CL_BG_TOP, justify='left', fg='white').pack(pady=20,anchor='w')
        logo = PhotoImage(file=r'sources/Logo_iso_stu_send.png', width=199, height=200)
        logo_photo = tk.Label(self.f_top, image=logo, highlightthickness=0, bd=0)
        logo_photo.image = logo
        logo_photo.pack(side='right',padx=70)

        self.f_left_info = tk.Frame(self.f_down,   width=1020, height=815, bg=CL_BG)
        self.f_left_info.pack_propagate(False)
        self.f_left_info.pack(side='left', pady=20, padx=25)

        tk.Label(self.f_left_info, text=f'{data.courses[course.course_id]['material'][material_id]['tittle']}', font=(FONT, 50, 'bold'), anchor='w', bg=CL_BG).pack(side='top', fill='x', padx=30)
        desc = tk.Text(self.f_left_info,  font=(FONT, 27, 'bold'), bg=CL_BG, width=50, height=10, highlightthickness=0, bd=2)
        desc.insert(tk.END,f"{data.courses[course.course_id]['material'][material_id]['description']}")
        desc.config(state='disabled')
        desc.pack()
        self.update_idletasks()


        self.matri = [['Estado de entrega', ''],['Estado de calificación', '']]
        #No entregado
        if data.students[student.user_id]['material'][material_id]['homework'] == '': self.matri[0][1] = 'No entregado'
        else: self.matri[0][1] = 'Entregado'

        if data.students[student.user_id]['material'][material_id]['obtained_points'] == 0: self.matri[1][1] = 'No calificado'
        else: self.matri[1][1] = 'Calificado'

        self.table = Tabla(self.f_left_info, self.matri, font_size=25,cell_width=18, cell_height=2, color_table='#CFE4EC', color_header='#669BBC', borderwidth=3)
        self.table.pack(pady=50)

        self.f_right_info = tk.Frame(self.f_down, width=800, height=700, bg=CL_BG)
        self.f_right_info.pack_propagate(False)
        self.f_right_info.pack(side='right', padx=30)

        self.f_right_info_top = tk.Frame(self.f_right_info, width=800, height=550, bg= CL_BG_SEND)
        self.f_right_info_top.pack_propagate(False)
        self.f_right_info_top.pack(side='top')

        tk.Label(self.f_right_info_top, text='Sube tu trabajo', anchor='w', bg=CL_BG_SEND, font=(FONT,45,'bold')).pack(fill='x', pady=20,padx=30)

        def valid_file(homework):
            self.select.config(state='disabled')
            self.send.config(state='normal')
            self.cancel.pack(pady=5)
            self.erro_text.pack_forget()
            self.homw = homework

        def denegate(text):
            self.select.config(state='normal')
            self.send.config(state='disabled', text='Enviar')
            self.cancel.pack_propagate()
            self.erro_text.config(text=text, fg='red')
            self.erro_text.pack(pady=25)
            self.erro_text.after(2500, func=lambda:self.erro_text.pack_forget())

        def process_file(ruta):
            try:
                homework = ''
                with open(ruta, 'r', encoding='UTF-8') as archivo:
                    for line in archivo:
                        homework += line
                valid_file(homework)
            except UnicodeDecodeError: denegate('Solo se aceptan txt!!')
            except FileNotFoundError: denegate('Lo siento, no encontramos el archivo')
            except Exception as e: denegate('No sé, pero pasó un error')

        def select_file():
            ruta_archivo = filedialog.askopenfilename(
                initialdir="/",
                title="Selecciona un archivo",
                filetypes=(("Documento de texto", "*.txt"), ("Todos los archivos", "*.*"))
            )
            if ruta_archivo:
                self.file = ruta_archivo
                process_file(ruta_archivo)

        self.select = tk.Button(self.f_right_info_top, text='Seleccionar Archivo', width=20, height=2, font=(FONT,30, 'bold'), borderwidth=2, command=select_file)
        self.select.pack(pady=25)

        def cancel_():
            yn = messagebox.askyesno('Cancelar envio', '¿Deseas cancelar el envio?')
            if yn:
                student.send_homework(material_id, '')
                self.cancel.pack_forget()
                denegate('')
                self.homw = ''
                self.matri[0][1] = 'No entregado'
                self.table.reload(self.matri)

        def send():
            yn = messagebox.askyesno('Cancelar envio', f'¿Deseas enviar el archivo {os.path.basename(self.file)}?')
            if yn:
                student.send_homework(material_id, self.homw)
                self.matri[0][1] = 'Entregado'
                self.table.reload(self.matri)
                self.send.config(state='disabled', text='Enviado')


        self.cancel = tk.Button(self.f_right_info_top, text='Cancelar', width=24, height=2, font=(FONT, 25, 'bold'), borderwidth=2, command=cancel_)
        self.erro_text= tk.Label(self.f_right_info_top, text='', font=(FONT, 30, 'bold'), bg=CL_BG_SEND)

        self.send = tk.Button(self.f_right_info_top, text='Enviar', width=24, height=2, font=(FONT,25, 'bold'), borderwidth=2, command=send, state='disabled')
        self.send.pack(pady=10)

        if self.homw != '':
            valid_file(self.homw)
            self.send.config(state='disabled')

s = SendHomework(root, Student('Pepito', '123', 'STU123'), Courses('Programación','SUB4354'), 'HOM4',parent= None)
root.mainloop()