import tkinter as tk
from graphic_tools import Window, PagePrincipal, Page, ScrollFrame, Tabla

root = Window('Ventana', (1920, 500))
f = PagePrincipal(root, bg='#E8CFB0')
f2 = Page(root, bg='#CEF5EB')
b = tk.Button(f, text='saluda', command=lambda: f.change_page(f2), cursor='fleur')
b.pack(padx=50, pady=10, side='bottom')
frame = tk.Frame(f2, bg='#BC9FCF')
frame.pack()
tabla = ScrollFrame(f2, width=500, height=300, bg='#7DCC4E', hbar_position='bottom', vbar_position='left')
tabla.pack()

for i in range(12):
    l2 = tk.Label(tabla.scr_frame, text='HOLA')
    tabla.pack_on_scroll(l2, side='left')

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

scframe_f3 = ScrollFrame(f3, 'left', 'bottom', width=200, height=1080, bg='#4B6AFF')
scframe_f3.pack(side="right")

l_a = tk.Label(scframe_f3.scr_frame, text='Hola')
scframe_f3.pack_on_scroll(l_a)

b_f3 = tk.Button(f3, text='Volver al menú principal', command=lambda:f3.change_page(f))
b_f3.pack()

a = [[' ','Hola', 'adios', 'aa'],
     ['2','Hola', 'aaaa', 'pancjo'],
     ['1', 'adios', 'zxczxc'],
     ['4','Adios', 'adios'],]

l = Tabla(master=f, matrix=a, vbar_position='left', hbar_position='bottom', borderwidth=2)
l.pack(side='left')

root.mainloop()