import tkinter as tk

from clases_internas.usuarios import Instructor
from menus.graphic_tools import Window, PagePrincipal, Page
from data.data_base import data


#EN EL MAIN SIEMPRE HACER ESTOS DOS
root = Window('Ventana', (1920, 500))
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
            self.m_prubea = MenuPrueba(self.master)
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
    def __init__(self, master:Window, **kwargs): #Digamos que "who" es un string de quíen es el menú
        super().__init__(master=master, bg='green', **kwargs)
        self.who = ''
        #COLOCAR LO VISUAL DE ESTE MENÚ:
        self.l = tk.Label(self, text=f'Hola {self.who}!')
        self.l.pack()

        def close_menu():self.change_page(master.principal_page) #para volver al login

        def add_st_test():
            i =Instructor(nombre.get(), contra.get())
            self.inf.config(text=f'Se agregó {nombre.get()}, su codigo es {i.user_id}')

            #self.change_page(CreateCourse(self.master, teacher=i))

        def iniciar_sesion():
            #En este ejemplo nombre.get() sustituye a lo que seria un code.get()
            if str(nombre.get()) in data.instructors:
                if data.instructors[str(nombre.get())]['password'] == str(contra.get()):
                    self.change_page(CreateCourse(self.master,
                                                  teacher=Instructor(data.instructors[str(nombre.get())]['name'], contra.get(), str(nombre.get())),
                                                  father=self))
            else: self.inf.config(text='No se pudo iniciar sesión, codigo no encontrado')

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

class CreateCourse(Page):
    def __init__(self, master, teacher:Instructor, father, **kwargs):
        super().__init__(master=master, bg='gray', **kwargs)
        tk.Label(self, text=f"Bienvenido {teacher.name}").pack(pady=20)
        tk.Label(self, text='Nombre del curso').pack()
        self.nombre = tk.Entry(self)
        self.nombre.pack(pady=20)

        def c_curso():
            teacher.create_course(self.nombre.get())

        def create_tarea():
            self.change_page(CrearTarea(self.master, self))

        tk.Button(self, text='Crear curso', command=lambda: c_curso()).pack(pady=25)
        tk.Button(self, text='Subir nota', command=lambda: create_tarea()).pack(pady=25)
        tk.Button(self, text='regresar', command=lambda:self.change_page(father)).pack() #volver al anterior


class CrearTarea(Page):
    def __init__(self, master, parent, **kwargs):
        super().__init__(master=master, bg='#B1945E', **kwargs)
        tk.Button(self, text='regresar', command=lambda:self.change_page(parent)).pack()

#CREACION DE MENÚS (Instancias)
login = Login(root)

root.mainloop()


