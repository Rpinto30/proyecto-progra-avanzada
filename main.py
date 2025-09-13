import tkinter as tk
from graphic_tools import Window, PagePrincipal, Page

root = Window('Ventana', (1920, 500))
#CLASE LOGIN
class Login(PagePrincipal):
    def __init__(self, master, **kwargs):
        super().__init__(master=master,bg='red', **kwargs)
        b = tk.Button(self, text='Sacar toplevel', command=lambda:self.__crear_usuario())
        b.pack(pady=50)
        tk.Label(self, text='De quién es el siguiente menú?').pack() #Lo hago directo porque luego no lo uso
        e = tk.Entry(self) #Como si este fuese el de Entry de código en la interfaz
        e.pack()
        #FUNCIÓN PARA CAMBIAR AL X MENÚ
        def cambiar_a_prueba():
            m = MenuPrueba(master=self.master, bg='green', who=str(e.get())) #ISNTANCIA DEL MENÚ
            self.change_page(m) #SE CAMBIA DE PAGINA
        b_cambio = tk.Button(self, text='Cambiar página', command=lambda:cambiar_a_prueba())
        b_cambio.pack()
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
        tk.Button(self,text='Regresar', command= lambda: close_menu()).pack()

login = Login(root) #Solo vamos a reutilizar el login, por eso se coloca como atributo del root
root.mainloop()

