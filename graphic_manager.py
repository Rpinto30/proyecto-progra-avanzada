import tkinter as tk
import tkinter.ttk as ttk

class Window(tk.Tk):
    def __init__(self, title='ventana', geometry:tuple[int, int]=(500,500), icon_image='', **kwargs):
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
    def __init__(self, master:Window, **kwargs):
        super().__init__(master=master, **kwargs)
        self._clear_widgest = []

    @property
    def clear_widgest(self):
        return self._clear_widgest

    @clear_widgest.setter
    def clear_widgest(self, widgets: list[tk.Widget]):
        self.clear_widgest.extend(widgets)

    def __clear_widgets_in_frame(self):
        for widget in self._clear_widgest:
            if isinstance(widget, tk.Label):
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
        self.__canvas_scroll = tk.Canvas(self, bg= '#ffffff')
        self.__canvas_scroll.pack_propagate(False)
        # BARRAS PARA MOVER (SE ME OLVIDO COMO SE DICEN EN ESPAÑOL xd)
        self.__vbar = tk.Scrollbar(self, orient="vertical")  # VERTICAL BAR

        self.__vbar.config(command=self.__canvas_scroll.yview)
        self.__hbar = tk.Scrollbar(self, orient="horizontal")  # HORIZONTAL BAR

        self.__hbar.config(command=self.__canvas_scroll.xview)
        # HACER QUE EL CANVAS SE MUEVA
        self.__canvas_scroll.config(xscrollcommand=self.__hbar.set, yscrollcommand=self.__vbar.set)

        self.__vbar.pack(side=vbar_position, fill="y")
        self.__hbar.pack(side=hbar_position, fill="x")

        self.__canvas_scroll.pack(side="left", expand=True, fill='both')
        self.__sub_frame = tk.Frame(self.__canvas_scroll)
        # ESTO LO GUARDO NOMAS PARA LIMITAR EL SCROLL (PCHES BOTONES)
        self.__canvas_scroll.create_window((0, 0), window=self.__sub_frame, anchor="nw")
        #self.__sub_frame.bind("<Configure>",
        #                      lambda e: self.__canvas_scroll.configure(scrollregion=self.__canvas_scroll.bbox("all")))

    def pack_on_scroll(self, widget:tk.Widget, **kwargs):
        print(self.__canvas_scroll.winfo_width())
        widget.pack(**kwargs)
        #Actualiza el canvas por cada pack
        self.__sub_frame.bind("<Configure>",
                                  lambda e: self.__canvas_scroll.configure(
                                      scrollregion=self.__canvas_scroll.bbox("all")))

    @property
    def scr_frame(self):
        return self.__sub_frame




