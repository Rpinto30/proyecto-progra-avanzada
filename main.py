import tkinter as tk

from menus.graphic_tools import Window, PagePrincipal, Page
from data.data_base import DataBase
from clases_internas.usuarios import Student

#EN EL MAIN SIEMPRE HACER ESTOS DOS
data = DataBase()
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
            m = MenuPrueba(master=self.master, bg='green', who=str(e.get())) #ISNTANCIA DEL MENÚ QUE SE DESEE
            self.change_page(m) #SE CAMBIA DE PAGINA (OBLIGATORIO)

        b_cambio = tk.Button(self, text='Cambiar página', command=lambda:cambiar_a_prueba()) #<- BOTÓN EJEMPLO
        b_cambio.pack()#<- BOTÓN EJEMPLO

    #ESTE ES UN EJEMPLO PARA UN TOPLEVEL
    def __crear_usuario(self):
        top_level = tk.Toplevel(self.master)
        top_level.pack_propagate(False) #PARA EVITAR QUE SE DEFORME AL HACER UN PACK
        txt = tk.Label(top_level, text='Holaaaaaaaaa')
        txt.pack()

#Los menus van a ser dinamicos, crean y destruyen conforme el programa los necesite
class MenuPrueba(Page): #CLASE DE MENÚ DE PRUEBA
    def __init__(self, master:Window, who, **kwargs): #Digamos que "who" es un string de quíen es el menú
        super().__init__(master=master, **kwargs)
        #COLOCAR LO VISUAL DE ESTE MENÚ:
        l = tk.Label(self, text=f'Hola {who}!')
        l.pack()
        def close_menu():
            self.change_page(master.principal_page)
        #para volver al login (la unica que va a perdurar) se cambia a lo que guardo la root(aquí master) en login_page

        def add_st_test():
            if ID.get() not in data.students:
                st = Student(ID.get(), nombre.get(),contra.get(), '')
                print(st.user_id)
                data.students[str(ID.get())] = {'name': nombre.get(), 'contra':contra.get()}
                data.save_data('students')
            else: print("No")
        tk.Label(self, text='ID:').pack()
        ID = tk.Entry(self)
        ID.pack()

        tk.Label(self, text='Nombre:').pack()
        nombre = tk.Entry(self)
        nombre.pack()

        tk.Label(self, text='Contraseña:').pack(pady=10)
        contra = tk.Entry(self)
        contra.pack()

        tk.Button(self, text='Añadir algo a estudiantes', command=lambda:add_st_test()).pack(pady=20)
        tk.Button(self, text='Probar base de datos', command=lambda:print(data.students)).pack(pady=20)

        tk.Button(self,text='Regresar', command= lambda: close_menu()).pack()

login = Login(root)
root.mainloop()

