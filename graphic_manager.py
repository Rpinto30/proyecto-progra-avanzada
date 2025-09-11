import tkinter as tk
import tkinter.ttk as ttk
from tkinter import PhotoImage


class Window(tk.Tk):
    def __init__(self, title='ventana', geometry=tuple[int, int], icon_image='', **kwargs):
        super().__init__(**kwargs)
        self.__principal_page = None
        self.__CURRENT_FRAME = None
        self.__desactive_exit = False
        # ----------------------------------WINDOWS-----------------------------------
        self.title(title)
        self.geometry(f"{geometry[0]}x{geometry[1]}")
        # self.resizable(False,False)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.protocol("WM_DELETE_WINDOW", self.exit_root)
        # ----------------------------------ICONO-----------------------------------
        if icon_image != '':
            icon_image = tk.PhotoImage(file=icon_image)
            self.iconphoto(True, icon_image)

    def set_principal_page(self, page):
        self.__principal_page = page
        self.change_frame(self.__principal_page)

    def change_frame(self, page):
        self.__CURRENT_FRAME = page
        self.__CURRENT_FRAME.grid(row=0, column=0, sticky='nsew')
        self.__CURRENT_FRAME.tkraise()

    def exit_root(self):
        if not self.__desactive_exit: self.quit()

    @property
    def desactive_exit(self):
        return self.__desactive_exit

    @desactive_exit.setter
    def desactive_exit(self, value: bool):
        self.__desactive_exit = value


class Page(tk.Frame):
    # **kwargs para heredar todos los argumentos de tk.Frame
    # https://www.geeksforgeeks.org/python/packing-and-unpacking-arguments-in-python
    def __init__(self, master, **kwargs):
        super().__init__(master=master, **kwargs)
        self._clear_widgest = []

    @property
    def clear_widget(self):
        return self._clear_widgest

    @clear_widget.setter
    def add_clear_widgets(self, widget: list[tk.Widget]):
        if widget not in self.clear_widget:
            self.clear_widget.extend(widget)

    def __clear_widgets_in_frame(self):
        for widget in self._clear_widgest:
            if isinstance(widget, (tk.Label)):
                widget.config(text=' ')
            elif isinstance(widget, tk.Entry):
                widget.delete(0, tk.END)
            elif isinstance(widget, tk.Checkbutton):
                widget.deselect()
            elif isinstance(widget, tk.Radiobutton):
                widget.deselect()
            elif isinstance(widget, tk.Listbox):
                widget.selection_clear(0, tk.END)

    def change_page(self, page):
        if self._clear_widgest: self.__clear_widgets_in_frame()
        self.master.change_frame(page)


class PagePrincipal(Page):
    def __init__(self, master, **kwargs):
        super().__init__(master=master, **kwargs)
        master.set_principal_page(self)


class ScrollFrame(tk.Frame):
    def __init__(self, master, vbar_position='right', hbar_position='bottom', **kwargs):
        super().__init__(master=master, **kwargs)
        if int(self.cget('width')) > 0 and int(self.cget('height')) > 0: self.pack_propagate(False)
        self.__canvas_scroll = tk.Canvas(self)
        # BARRAS PARA MOVER (SE ME OLVIDO COMO SE DICEN EN ESPAÑOL xd)
        self.__vbar = ttk.Scrollbar(self, orient="vertical")  # VERTICAL BAR
        self.__vbar.pack(side=vbar_position, fill="y")
        self.__vbar.config(command=self.__canvas_scroll.yview)
        self.__hbar = ttk.Scrollbar(self, orient="horizontal")  # HORIZONTAL BAR
        self.__hbar.pack(side=hbar_position, fill="x")
        self.__hbar.config(command=self.__canvas_scroll.xview)
        # HACER QUE EL CANVAS SE MUEVA
        self.__canvas_scroll.config(xscrollcommand=self.__hbar.set, yscrollcommand=self.__vbar.set)
        self.__canvas_scroll.pack(side="left", expand=True, fill='both')
        self.__sub_frame = tk.Frame(self.__canvas_scroll)
        # ESTO LO GUARDO NOMAS PARA LIMITAR EL SCROLL (PCHES BOTONES)
        self.__canvas_scroll.create_window((0, 0), window=self.__sub_frame, anchor="nw")
        self.__sub_frame.bind("<Configure>",
                              lambda e: self.__canvas_scroll.configure(scrollregion=self.__canvas_scroll.bbox("all")))

    @property
    def scr_frame(self): return self.__sub_frame


root = Window('Ventana', (500, 500))
f = PagePrincipal(root, bg='#E8CFB0')
f2 = Page(root, bg='#CEF5EB')
b = tk.Button(f, text='saluda', command=lambda: f.change_page(f2), cursor='fleur')
b.pack(padx=50, pady=10, side='bottom')
frame = tk.Frame(f2, bg='#BC9FCF')
frame.pack()
tabla = ScrollFrame(f2, width=200, height=300)
tabla.pack()
b2 = tk.Button(tabla.scr_frame, text='saluda', command=lambda: print("hola"), state='disabled')
b2.pack()
b = tk.Button(frame, text='volver', command=lambda: f2.change_page(f))
b.pack(padx=50, pady=10, side='right')

root.mainloop()

