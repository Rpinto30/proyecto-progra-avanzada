import tkinter as tk
from graphic_manager import Window, PagePrincipal, Page, ScrollFrame

root = Window('Ventana', (500, 500))
f = PagePrincipal(root, bg='#E8CFB0')
f2 = Page(root, bg='#CEF5EB')
b = tk.Button(f, text='saluda', command=lambda: f.change_page(f2), cursor='fleur')
b.pack(padx=50, pady=10, side='bottom')
frame = tk.Frame(f2, bg='#BC9FCF')
frame.pack()
tabla = ScrollFrame(f2, width=500, height=300, bg='#7DCC4E')
tabla.pack()

for i in range(4):
    l2 = tk.Label(tabla.scr_frame, text='HOLA')
    tabla.pack_on_scroll(l2, side='right', anchor='ne')


def texto_prueba(texto):
    global  text_v, l_f3
    text_v = "Hola "+ str(texto)
    l_f3.config(text=text_v)
    f2.change_page(f3)

text_v = tk.StringVar()
for i in range(20):
    b2 = tk.Button(tabla.scr_frame, text=f'saluda {i}', command=lambda: texto_prueba(i))
    tabla.pack_on_scroll(b2)

b = tk.Button(frame, text='volver', command=lambda: f2.change_page(f))
b.pack(padx=50, pady=10, side='right')

f3 = Page(root, bg='#FFE46E')

l_f3 = tk.Label(f3, text='Hola')
l_f3.pack()

b_f3 = tk.Button(f3, text='Volver al menú principal', command=lambda:f3.change_page(f))
b_f3.pack()
root.mainloop()