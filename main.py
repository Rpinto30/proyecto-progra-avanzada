import tkinter as tk
from graphic_tools import Window, PagePrincipal

root = Window('Ventana', (1920, 500))

class Login(PagePrincipal):
    def __init__(self, master, **kwargs):
        super().__init__(master=master,bg='red', **kwargs)
        b = tk.Button(self, text='Sacar toplevel', command=lambda:self.__crear_usuario())
        b.pack(pady=50)

    def __crear_usuario(self):
        top_level = tk.Toplevel(self.master)
        top_level.pack_propagate(False) #PARA EVITAR QUE SE DEFORME AL HACER UN PACK
        txt = tk.Label(top_level, text='Holaaaaaaaaa')
        txt.pack()

f = Login(root)
root.mainloop()

