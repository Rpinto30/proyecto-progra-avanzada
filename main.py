import tkinter as tk

from clases_internas.usuarios import Instructor, Student
from clases_internas.cursos import Courses
from menus.graphic_tools import Window, PagePrincipal, Page, Tabla
from data.data_base import data


#EN EL MAIN SIEMPRE HACER ESTOS DOS
root = Window('Ventana', (1500, 500))
#CLASE LOGIN EJEMPLO
class Login(PagePrincipal):
    def __init__(self, master, **kwargs):
        super().__init__(master=master,bg='red', **kwargs)

        #AQUÍ IRIA LOS BOTONES, FRAMES, TEXTOS DEL LOGIN (los botones de abajo son un ejemplo nada más)
        b = tk.Button(self, text='Sacar toplevel', command=lambda:self.__crear_usuario()) #<- BOTÓN EJEMPLO
        b.pack(pady=50) #<- BOTÓN EJEMPLO
        tk.Label(self, text='De quién es el siguiente menú?').pack() #Lo hago directo porque luego no lo uso
        e = tk.Entry(self) #Como si este fuese el de Entry de código en la interfaz
        e.pack()
        #FUNCIÓN PARA CAMBIAR AL X MENÚ, en vez de instanciar meú de prueba, instanciar el menú que se desea
        def cambiar_a_prueba():
            self.m_prubea = MenuPrueba(master=self.master)
            self.m_prubea.set_who(e.get())
            self.change_page(self.m_prubea)
            #self.change_page(MenuPrueba(master=self.master, bg='green', who=str(e.get()))) #SE CAMBIA DE PAGINA (OBLIGATORIO)

        b_cambio = tk.Button(self, text='Cambiar página', command=lambda:cambiar_a_prueba()) #<- BOTÓN EJEMPLO
        b_cambio.pack()#<- BOTÓN EJEMPLO

        #Al final, agregar siempre el clear_widgest a los widgets que se desean limpiar cuando se cargue otra vez el programa
        self.clear_widgest = [e]

        #ESTE ES UN EJEMPLO PARA UN TOPLEVEL
    def __crear_usuario(self):
        top_level = tk.Toplevel(self.master)
        top_level.pack_propagate(False) #PARA EVITAR QUE SE DEFORME AL HACER UN PACK
        txt = tk.Label(top_level, text='Holaaaaaaaaa')
        txt.pack()

class MenuPrueba(Page): #CLASE DE MENÚ DE PRUEBA
    def __init__(self, master, **kwargs): #Digamos que "who" es un string de quíen es el menú
        super().__init__(master=master, bg='green', **kwargs)
        self.who = ''
        #COLOCAR LO VISUAL DE ESTE MENÚ:
        self.l = tk.Label(self, text=f'Hola {self.who}!')
        self.l.pack()

        # PRUEBA DE RADIO BUTTONS
        v = tk.StringVar(value='1') #Variable global de los RadioButton
        tk.Radiobutton(self, text='Estudiante', value='1',variable=v).pack(ipady=5)
        tk.Radiobutton(self, text='Instructor', value='2',variable=v).pack(ipady=5)

        def close_menu():self.change_page(master.principal_page) #para volver al login

        def add_st_test():
            if v.get() == '1': #Estudiante
                i = Student(nombre.get(), contra.get())
                i.create_student(nombre.get(), contra.get())
                self.inf.config(text=f'Se agregó {nombre.get()}, su codigo es {i.user_id}')
            elif v.get() == '2': #Instructor
                i =Instructor(nombre.get(), contra.get())
                i.create_instructor(nombre.get(), contra.get())
                self.inf.config(text=f'Se agregó {nombre.get()}, su codigo es {i.user_id}')

        def iniciar_sesion():
            if str(nombre.get())[:3] == 'IST':
                #En este ejemplo nombre.get() sustituye a lo que seria un code.get()
                if str(nombre.get()) in data.instructors:
                    if data.instructors[str(nombre.get())]['password'] == str(contra.get()):
                        self.change_page(CreateCourse(self.master,
                                                      teacher=Instructor(data.instructors[str(nombre.get())]['name'], contra.get(), str(nombre.get())),
                                                      father=self))
                else: self.inf.config(text='No se pudo iniciar sesión, codigo no encontrado')
            elif str(nombre.get())[:3] == 'STU':
                # En este ejemplo nombre.get() sustituye a lo que seria un code.get()
                if str(nombre.get()) in data.students:
                    if data.students[str(nombre.get())]['password'] == str(contra.get()):
                        self.change_page(CoursesStudent(self.master,
                                                        student=Student(data.students[str(nombre.get())]['name'],
                                                                         contra.get(), str(nombre.get())), father=self))
                else:
                    self.inf.config(text='No se pudo iniciar sesión, codigo no encontrado')

        tk.Label(self, text='Nombre o código:').pack()
        nombre = tk.Entry(self)
        nombre.pack()

        tk.Label(self, text='Contraseña:').pack(pady=10)
        contra = tk.Entry(self)
        contra.pack()

        tk.Button(self, text='Crear Instructor', command=lambda:add_st_test()).pack(pady=20)
        tk.Button(self, text='Iniciar sesión', command=lambda: iniciar_sesion()).pack(pady=20)

        tk.Button(self,text='Regresar', command= lambda: close_menu()).pack()

        self.inf = tk.Label(self, text='')
        self.inf.pack()

        self.clear_widgest = [nombre, contra]

    def set_who(self, who):
        self.who = who
        self.l.config(text=f"Hola {who}!")

class CoursesStudent(Page):
    def __init__(self, master, student:Student, father, **kwargs):
        super().__init__(master=master, bg='#43701B', **kwargs)
        self.student = student
        self.father = father

        tk.Label(self, text=f"Bienvenido {student.name}").pack(pady=20)
        tk.Label(self, text='Ingresa el código de un curos').pack()
        c = tk.Entry(self)
        c.pack(pady=50)
        def asig_course():
            s = Student(student.name, student.password, student.user_id)
            if str(c.get()) in data.courses:
                s.course_register(str(c.get()))
                teacher = data.courses[str(c.get())]['teacher']
                self.inf.config(text=f"Se asigno al curso {data.courses[str(c.get())]} impartido por {data.instructors[teacher]['name']}")
            else: self.inf.config(text='Lo siento, no ecnontramos ningun curso')
            self.t.reload(self.check_student_courses())
            self.t.reload(self.check_student_courses())

        tk.Button(self, text='Asignarse a curso', command=lambda: asig_course()).pack(pady=20)

        def ver_tareas(row, colum, value):
            if row>0:
                self.change_page(DoHomework(self.master, student, self, value))
        tk.Label(self, text='TAREAS:').pack(pady=10)
        self.t = Tabla(self, self.check_student_courses(), vbar_position='left', propagate_height=5, cell_command=ver_tareas,
                  select_mode='row')
        self.t.pack()

        tk.Button(self, text='regresar', command=lambda: self.change_page(father)).pack()  # volver al anterior
        self.inf = tk.Label(self, text='')
        self.inf.pack()

    def check_student_courses(self):
        c = [['Codigo Curso', 'Curso', 'Tarea']]
        homework_id = data.students[self.student.user_id]['material']
        for id_ in homework_id:
            print(data.students[self.student.user_id]['material'][id_]['homework'])
            if data.students[self.student.user_id]['material'][id_]['homework'] == '':
                cur_id = data.students[self.student.user_id]['material'][id_]["course"]
                n_cur = data.courses[cur_id]['course_name']
                title = data.students[self.student.user_id]['material'][id_]["tittle"]
                c.append([id_, n_cur, title])
        return c

class DoHomework(Page):
    def __init__(self, master, student: Student, father, id_homework, **kwargs):
        super().__init__(master=master, bg='#43701B', **kwargs)

        self.e = tk.Text(self, width=50, height=10)
        self.e.pack()

        def send():
            student.send_homework(id_homework, self.e.get('1.0', tk.END))
            father.t.reload(father.check_student_courses())

        tk.Button(self, text='Enviar', command=lambda :send()).pack(pady=50)
        tk.Button(self, text='regresar', command=lambda: self.change_page(father)).pack()  # volver al anterior

class CreateCourse(Page):
    def __init__(self, master, teacher:Instructor, father, **kwargs):
        super().__init__(master=master, bg='gray', **kwargs)
        tk.Label(self, text=f"Bienvenido {teacher.name}").pack(pady=20)
        tk.Label(self, text='Nombre del curso').pack()
        self.nombre = tk.Entry(self)
        self.nombre.pack(pady=20)

        def c_curso():
            teacher.create_course(self.nombre.get())
            t.reload(check_teacher_courses())

        def check_teacher_courses():
            c = [['Codigo', 'Nombre']]
            curs_id = data.instructors[teacher.user_id]['courses']
            for id_ in curs_id:
                n_cur = data.courses[id_]['course_name']
                c.append([id_, n_cur])
            return c

        def create_tarea(row, colum, value):
            if row > 0:
                value = value[0]
                self.change_page(
                    CrearTarea(self.master, self, teacher,
                               Courses(data.courses[str(value)]['course_name'], data.courses[str(value)]['teacher'],
                                       data.courses[str(value)]['students'], data.courses[str(value)]['material'],
                                       str(value))))

        t = Tabla(self,check_teacher_courses(), vbar_position='left', propagate_height=5, cell_command=create_tarea, select_mode='row')
        t.pack()
        tk.Label(self,text='Selecciona un codigo para asignar una tarea')


        tk.Button(self, text='Crear curso', command=lambda: c_curso()).pack(pady=25)
        #tk.Button(self, text='Subir nota', command=lambda: create_tarea()).pack(pady=25)
        tk.Button(self, text='regresar', command=lambda:self.change_page(father)).pack() #volver al anterior


class CrearTarea(Page):
    def __init__(self, master, parent, teacher, course:Courses, **kwargs):
        super().__init__(master=master, bg='#B1945E', **kwargs)
        self.course = course
        tk.Label(self, text=f'Agrega tarea para {course.course_name}').pack()
        tk.Label(self, text='Agrega titulo').pack(pady=10)
        self.tittle = tk.Entry(self)
        self.tittle.pack()

        def solo_numeros(event):
            if event.char.isdigit() or event.keysym in ('BackSpace', 'Delete', 'Left', 'Right'): return None
            else: return "break"

        tk.Label(self, text='Agrega descripcion').pack(pady=10)
        self.desc = tk.Entry(self)
        self.desc.pack()

        tk.Label(self, text='Agrega Punteo').pack(pady=10)
        self.poi = tk.Entry(self)
        self.poi.bind("<KeyPress>", solo_numeros)
        self.poi.pack()
        def crear():
            course.assign_homework(self.tittle.get(), self.desc.get(), self.poi.get())

        tk.Button(self, text='Asignar', command=lambda:crear()).pack(pady=20)
        tk.Button(self, text='regresar', command=lambda:self.change_page(parent)).pack(pady=20)

        def check_hom(row, colum, value):
            if value[-1] == 'Entregado':
                self.change_page(CheckHomework(self.master, value, course, self))
        self.t = Tabla(self, matrix=self.check_student_homework(), cell_command=check_hom, select_mode='row')
        self.t.pack(side='right')

    def check_student_homework(self):
        c = [['Estudiante', 'ID', 'Tarea', 'ID', 'Estado']]
        for id_st in data.courses[self.course.course_id]['students']:
            name_ = data.students[id_st]['name']
            for id_hom, hom in data.students[id_st]['material'].items():
                if hom['course'] == self.course.course_id:
                    line = [name_, id_st, hom['tittle'], id_hom]
                    if hom['homework'] == '': line.append('No entregado')
                    else: line.append('Entregado')
                    c.append(line)

        return c

class CheckHomework(Page):
    def __init__(self, master, ids_, course, parent, **kwargs):
        super().__init__(master=master, **kwargs)
        tk.Label(self, text="Tarea:").pack(pady=20)
        tk.Label(self, text=str(data.students[ids_[1]]['material'][ids_[3]]['homework'])).pack()

        def solo_numeros(event):
            if event.char.isdigit() or event.keysym in ('BackSpace', 'Delete', 'Left', 'Right'): return None
            else: return "break"

        self.e = tk.Entry(self)
        self.e.bind("<KeyPress>", solo_numeros)
        self.e.pack()

        def subir_punteo():
            if 0<= int(self.e.get()) <= int(data.courses[course.course_id]['material'][ids_[3]]['points']):
                course.qualification(ids_[1], ids_[3], int(self.e.get()))

        tk.Button(self, text='Subir punteo', command=subir_punteo).pack()
        tk.Button(self, text='regresar', command=lambda: self.change_page(parent)).pack(pady=20)


#CREACION DE MENÚS (Instancias)
login = Login(root)

root.mainloop()


