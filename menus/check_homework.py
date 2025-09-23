import tkinter as tk

from clases_internas.usuarios import Instructor
from graphic_tools import Page, Tabla
from clases_internas.cursos import Courses
from data.data_base import data
from tkinter import PhotoImage
from ranking_profesor import StudentNotes
from tkinter import messagebox

CL_BG = '#eae2b7'
CL_BG_L = '#f77f00'
CL_BG_TOP_L = '#d62828'
CL_BG_R = '#4a9b57'
CL_BG_LC = '#fcbf49'

CL_B_EXIT = '#f77f00'
CL_B_TOP_AC = '#eae2b7'
CL_B_TOP_DC = '#c48430'

FONT = 'Arial'
FG_B_TOP_AC = '#926f59'
FG_B_TOP_DC = '#eae2b7'

H_LEFT = 990

class CheckHomework(Page):
    def __init__(self, master, course: Courses, instructor:Instructor, parent, **kwargs):
        super().__init__(master, bg=CL_BG, **kwargs)
        self.course = course
        self.select_ = True
        self.material_id, self.student_id = '',''

        self.f_left = tk.Frame(self, bg=CL_BG, width=1300, height=1080)
        self.f_left.pack_propagate(False)
        self.f_left.pack(side='left')

        self.f_top = tk.Frame(self.f_left, bg=CL_BG_TOP_L, width=1300, height=(1080 - H_LEFT))
        self.f_top.pack_propagate(False)
        self.f_top.pack(side='top')

        def exit_(): self.change_page(parent)

        tk.Button(self.f_top, text='←', width=4, height=1, command=exit_, font=(FONT, 50, 'bold'), bg=CL_B_EXIT,relief='flat', fg='white').pack(side="left")

        self.canvas_top = tk.Canvas(self.f_top, width=1122, height=(1080 - H_LEFT), bg=CL_BG_TOP_L, highlightthickness=0,bd=0, relief='flat')
        self.canvas_top.pack_propagate(False)
        self.canvas_top.pack(side="right")

        self.canvas_top.create_rectangle(0,0,330,(1080 - H_LEFT), fill=CL_B_TOP_AC, outline='')
        self.canvas_top.create_text(165, 45, font=(FONT, 30, 'bold'), fill=FG_B_TOP_AC, text='ESTUDIANTES')
        self.canvas_top.create_rectangle(330,0,660,(1080 - H_LEFT), fill=CL_B_TOP_DC, outline='')
        self.canvas_top.create_text(495, 45, font=(FONT, 30, 'bold'), fill=FG_B_TOP_DC, text='SUBIR NOTA')

        self.canvas_top.create_polygon(0,0,20,0,0,(1080 - H_LEFT), fill=CL_BG_TOP_L)
        self.canvas_top.create_polygon(310,0,350,0,330,(1080 - H_LEFT), fill=CL_BG_TOP_L) #Del vertice al centro hay 10, total de base =20px
        self.canvas_top.create_polygon(640,0,680,0,660,(1080 - H_LEFT), fill=CL_BG_TOP_L) #Del vertice al centro hay 10, total de base =20px

        self.f_r = tk.Frame(self, bg=CL_BG_R, width=(1920-1300), height=1080)
        self.f_r.pack_propagate(False)
        self.f_r.pack()


        #FRAME DE SELECCIONAR
        self.f_r_select = tk.Frame(self.f_r, bg=CL_BG_R, width=(1920 - 1300), height=1080)
        self.f_r_select.pack()

        self.f_r_select_top = tk.Frame(self.f_r_select, bg=CL_BG_R, width=(1920-1300), height=230)
        self.f_r_select_top.pack_propagate(False)
        self.f_r_select_top.pack()

        logo = PhotoImage(file=r'sources/Logo_iso_check.png', width=199, height=200)
        logo_photo = tk.Label(self.f_r_select_top, image=logo, highlightthickness=0, bd=0)
        logo_photo.image = logo
        logo_photo.pack(side='right', padx=30)

        self.f_r_select_acum = tk.Frame(self.f_r_select, bg='#4b56bd', width=(1920-1300-60), height=200)
        self.f_r_select_acum.pack_propagate(False)
        self.f_r_select_acum.pack(pady=40)
        total_point = 0
        for material_id in data.courses[course.course_id]['material']:
            if material_id[:3] == 'HOM': total_point += int(data.courses[course.course_id]['material'][material_id]['points'])
        tk.Label(self.f_r_select_acum, text='Puntos acumulados', bg='#4b56bd', fg='white', font=(FONT, 40, 'bold')).pack(pady=25)
        tk.Label(self.f_r_select_acum, text=f'{total_point}', bg='#4b56bd', fg='white', font=(FONT, 39, 'bold')).pack(pady=5)

        self.f_r_select_asing = tk.Frame(self.f_r_select, bg='#4b56bd', width=(1920 - 1300 - 60), height=200)
        self.f_r_select_asing.pack_propagate(False)
        self.f_r_select_asing.pack(pady=50)

        tk.Label(self.f_r_select_asing, text='Estudiantes asignados', bg='#4b56bd', fg='white',font=(FONT, 35, 'bold')).pack(pady=25)
        tk.Label(self.f_r_select_asing, text=f'{len(data.courses[course.course_id]['students'])}', bg='#4b56bd', fg='white', font=(FONT, 39, 'bold')).pack(pady=10)

        def set_info():
            if self.select_: #ir al informe general
                self.change_page(StudentNotes(self.master, instructor, course.course_id,self))
                self.cancel_select()
            else:
                if 0 <= int(self.entry_note.get()) <= int(data.courses[course.course_id]['material'][self.material_id]['points']):
                    course.qualification(self.student_id, self.material_id, self.entry_note.get())
                    self.cancel_select()
                    messagebox.showinfo("Nota subida",
                                         f'La nota de {data.students[self.student_id]['name']} fue subida correctamente!!')

                else:
                    messagebox.showerror("Más de la nota máxima!!!",f'¡Cuidado! la nota maxima es {data.courses[course.course_id]['material'][self.material_id]['points']}')

        self.b_inf = tk.Button(self, text='Informe General', bg='#5ddb75', fg='white', font=(FONT, 30, 'bold'),command=set_info, width=20)
        self.b = tk.Button(self, text='Cancelar', bg='#B8444F', fg='white', font=(FONT, 30, 'bold'), width=20, command=self.cancel_select)
        self.b_inf.pack(in_=self.f_r_select, pady=10)
        self.b.pack(in_=self.f_r_select, pady=10)

        # FRAME DE SELECCIONAR
        self.f_r_note = tk.Frame(self.f_r, bg=CL_BG_R, width=(1920 - 1300), height=1080)
        #self.f_r_note.pack()

        self.f_r_note_top = tk.Frame(self.f_r_note, bg=CL_BG_R, width=(1920 - 1300), height=230)
        self.f_r_note_top.pack_propagate(False)
        self.f_r_note_top.pack()

        logo = PhotoImage(file=r'sources/Logo_iso_check.png', width=199, height=200)
        logo_photo = tk.Label(self.f_r_note_top, image=logo, highlightthickness=0, bd=0)
        logo_photo.image = logo
        logo_photo.pack(side='right', padx=30)

        self.f_r_note_entry = tk.Frame(self.f_r_note, bg=CL_BG_R, width=(1920 - 1300 - 60), height=200)
        self.f_r_note_entry.pack_propagate(False)
        self.f_r_note_entry.pack(pady=40)

        def solo_numeros(event):
            if event.char.isdigit() or event.keysym in ('BackSpace', 'Delete', 'Left', 'Right'): return None
            else: return "break"

        tk.Label(self.f_r_note_entry, text='Ingesar Nota: ', bg=CL_BG_R, fg='white', font=(FONT,30)).pack()
        self.entry_note = tk.Entry(self.f_r_note_entry, font=(FONT,50), width=5)
        self.entry_note.pack(pady=45)
        self.entry_note.bind("<KeyPress>", solo_numeros)


        #self.b_0 = tk.Button(self.f_r_note, text='Calificar con 0', font=(FONT,40), bg='#4b56bd', fg='white', )
        #self.b_0.pack(pady=10)

        self.f_left_info = CheckNotes(self.f_left, course, parent_hw=self)
        self.f_left_info.pack()

    def change_stu(self):
        self.canvas_top.create_rectangle(0, 0, 330, (1080 - H_LEFT), fill=CL_B_TOP_DC, outline='')
        self.canvas_top.create_text(165, 45, font=(FONT, 30, 'bold'), fill=FG_B_TOP_DC, text='ESTUDIANTES')
        self.canvas_top.create_rectangle(330, 0, 660, (1080 - H_LEFT), fill=CL_B_TOP_AC, outline='')
        self.canvas_top.create_text(495, 45, font=(FONT, 30, 'bold'), fill=FG_B_TOP_AC, text='SUBIR NOTA')

        self.canvas_top.create_polygon(0, 0, 20, 0, 0, (1080 - H_LEFT), fill=CL_BG_TOP_L)
        self.canvas_top.create_polygon(310, 0, 350, 0, 330, (1080 - H_LEFT),
                                       fill=CL_BG_TOP_L)  # Del vertice al centro hay 10, total de base =20px
        self.canvas_top.create_polygon(640, 0, 680, 0, 660, (1080 - H_LEFT),
                                       fill=CL_BG_TOP_L)  # Del vertice al centro hay 10, total de base =20px

        self.f_r_select.pack_forget()
        self.f_r_note.pack()
        self.b.pack_forget()
        self.b_inf.pack_forget()
        self.b_inf.config(text='subir nota')
        self.b_inf.pack(in_=self.f_r_note, pady=10)
        self.b.pack(in_=self.f_r_note, pady=10)
        self.select_ = False


    def cancel_select(self):
        if self.select_:
            self.f_left_info.table_students.pack_forget()
            self.f_left_info.text_students.pack_forget()

class CheckNotes(tk.Frame):
    def __init__(self, master, course, parent_hw, **kwargs):
        super().__init__(master=master,  width=1300, height=H_LEFT,bg=CL_BG,**kwargs)
        self.parent_hw = parent_hw
        self.course = course
        self.pack_propagate(False)
        tk.Label(self, text='Selecciona una fila de tarea para calificar', font=(FONT, 30,'bold'),bg=CL_BG).pack(pady=30)

        def select_student(row, colum, value):
            if row > 0:
                self.parent_hw.select_ = False
                self.pack_forget()
                self.check = SendNoteMenu(self.master, self.course.course_id, value[0], self.material_select)
                self.check.pack()
                self.parent_hw.b.config(command=self.check.cancel_)
                self.text_students.pack_forget()
                self.table_students.pack_forget()
                self.parent_hw.change_stu()
                self.parent_hw.student_id = value[0]
        def selec_course(row, colum, value):
            if row > 0:
                self.master.master.material_id = value[0]
                self.material_select = value[0]
                self.table_students.reload(self.student_homework(value[0]))
                self.text_students.pack(pady=30)
                self.table_students.pack(pady=10)


        self.material_select = None
        self.table_notes = Tabla(self, self.material_course(), font_size=15, cell_width=25, cell_height=3, cell_command=selec_course, select_mode='row', propagate_height=3, cursor='hand2', bg='#97836D')
        self.table_notes.pack()

        self.text_students = tk.Label(self, text='Selecciona una fila de estudiante para calificar', font=(FONT, 30,'bold'),bg=CL_BG)
        self.table_students = Tabla(self, matrix = [['Estudiante', 'Estado', 'Nota', 'Nota acumulada']], font_size=15, cell_width=15, cell_height=3, cell_command=select_student, select_mode='row', cursor='hand2', propagate_height=4, bg='#97836D')
        #self.table_students.pack()

    def student_homework(self, id_hom):
        table = [['ID', 'Estudiante', 'Estado', 'Nota', 'Nota acumulada']]
        for students_id in data.courses[self.course.course_id]['students']:
            name = data.students[students_id]['name']
            for material_id, material in data.students[students_id]['material'].items():
                if material_id [:3] == 'HOM':
                    if data.students[students_id]['material'][material_id]['homework'] == '': state = 'No entregado'
                    else: state = 'Entregado'
                    note = data.students[students_id]['material'][material_id]['obtained_points']
                    note_max = data.students[students_id]['material'][material_id]['points']
                    if material_id == id_hom:
                        table.append([students_id,name, state, note, note_max])
        return table

    def material_course(self):
        table = [['ID','Tarea', 'Descripción', 'Punteo']]
        for material_id in data.courses[self.course.course_id]['material']:
            if material_id[:3] == 'HOM':
                tittle = data.courses[self.course.course_id]['material'][material_id]['tittle']
                description = (data.courses[self.course.course_id]['material'][material_id]['description'][:25]
                               +'\n'+data.courses[self.course.course_id]['material'][material_id]['description'][25:40])
                if len(data.courses[self.course.course_id]['material'][material_id]['tittle']) >= 40: tittle +='...'

                points = data.courses[self.course.course_id]['material'][material_id]['points']
                table.append([material_id,tittle, description, points])
        return table

class SendNoteMenu(tk.Frame):
    def __init__(self, master, course_id:str, student_id, material_id, **kwargs):
        super().__init__(master=master,  width=1300, height=H_LEFT,bg=CL_BG,**kwargs)
        self.course_id = course_id
        self.pack_propagate(False)

        tk.Label(self, text=f'Tarea de {data.students[student_id]['name']} ({student_id}):', font=(FONT, 50, 'bold'), anchor='w', bg=CL_BG).pack(side='top', fill='x', pady=50, padx=50)
        self.t_hom = tk.Text(self, height=20, width=70, font=(FONT, 20))
        self.t_hom.insert(tk.END, data.students[student_id]['material'][material_id]['homework'])
        self.t_hom.config(state='disabled')
        self.t_hom.pack()

    def cancel_(self):
        self.pack_forget()
        info = self.master.master.f_left_info
        info.pack()

        self.master.master.canvas_top.create_rectangle(0, 0, 330, (1080 - H_LEFT), fill=CL_B_TOP_AC, outline='')
        self.master.master.canvas_top.create_text(165, 45, font=(FONT, 30, 'bold'), fill=FG_B_TOP_AC, text='ESTUDIANTES')
        self.master.master.canvas_top.create_rectangle(330, 0, 660, (1080 - H_LEFT), fill=CL_B_TOP_DC, outline='')
        self.master.master.canvas_top.create_text(495, 45, font=(FONT, 30, 'bold'), fill=FG_B_TOP_DC, text='SUBIR NOTA')

        self.master.master.canvas_top.create_polygon(0, 0, 20, 0, 0, (1080 - H_LEFT), fill=CL_BG_TOP_L)
        self.master.master.canvas_top.create_polygon(310, 0, 350, 0, 330, (1080 - H_LEFT),
                                       fill=CL_BG_TOP_L)  # Del vertice al centro hay 10, total de base =20px
        self.master.master.canvas_top.create_polygon(640, 0, 680, 0, 660, (1080 - H_LEFT),
                                       fill=CL_BG_TOP_L)  # Del vertice al centro hay 10, total de base =20px

        self.master.master.f_r_note.pack_forget()
        self.master.master.f_r_select.pack()
        self.master.master.b.pack_forget()
        self.master.master.b_inf.pack_forget()
        self.master.master.b_inf.config(text='Informe General')
        self.master.master.b_inf.pack(in_=self.master.master.f_r_select, pady=10)
        self.master.master.b.pack(in_=self.master.master.f_r_select, pady=10)
        # Restaurar comando del botón cancelar
        self.master.master.b.config(command=self.master.master.cancel_select)
        self.master.master.entry_note.delete(0, tk.END)
        self.master.master.select_ = True
