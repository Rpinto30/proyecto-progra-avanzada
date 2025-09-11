import tkinter as tk
import warnings #Para hacer advertencias en el código

class Window(tk.Tk):
    # DOCSTRING: https://www.datacamp.com/tutorial/docstrings-python
    def __init__(self, title='ventana', geometry:tuple[int, int]=(500,500), icon_image='', **kwargs):
        """
        Crea una ventana, usar como si fuese el tipico root = tk.Tk()
        Por defecto muestra un frame en blanco, pero se le puede asignar uno
        usando set_principal_page()

        :param title: Título de la ventana
        :param geometry: Geometria en pixeles de la ventana
        :param icon_image: Si existe, coloca una imagen de icono
        :param kwargs: Hereda parametros de la clase tk.TK()
        """
        super().__init__(**kwargs)
        self.__principal_page = None
        self.__current_frame = None
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
        """
        Deja como Frame o página principal el frame que se desee.
        Este frame aparecerá cuando se ejecute el programa

        :param page: El frame que se desea dejar como principal(predefinido)
        """
        self.__principal_page = page
        self.change_frame(self.__principal_page)

    def change_frame(self, page):
        self.__current_frame = page
        self.__current_frame.grid(row=0, column=0, sticky='nsew')
        self.__current_frame.tkraise()

    def exit_root(self):
        if not self.__desactive_exit: self.quit()

    @property
    def desactive_exit(self):
        return self.__desactive_exit

    @desactive_exit.setter
    def desactive_exit(self, value: bool):
        self.__desactive_exit = value

    @property
    def current_frame(self): return self.__current_frame


class Page(tk.Frame):
    # **kwargs para heredar todos los argumentos de tk.Frame
    # https://www.geeksforgeeks.org/python/packing-and-unpacking-arguments-in-python
    def __init__(self, master:Window, **kwargs):
        """
        Crea una página, las páginas son frames que permiten organizar en secciones
        widgets para un uso específico. Se adaptan al tamaño de la pantalla y por medio
        de change_page() se puede saltar a otra página y los widgets que se deseen pueden
        ser limpiados en este salto de página.
        :param master: La ventana donde se colocará la página, debe ser de tipo Window
        :param kwargs: cualquier otro atributo de tk.Frame()
        """
        super().__init__(master=master, **kwargs)
        self._clear_widgest = []

    @property
    def clear_widgest(self):
        return self._clear_widgest

    @clear_widgest.setter
    def clear_widgest(self, widgets: list[tk.Widget]):
        self.clear_widgest.extend(widgets)

    def _clear_widgets_in_frame(self):
        for widget in self._clear_widgest:
            if isinstance(widget, tk.Label): widget.config(text=' ')
            elif isinstance(widget, tk.Entry): widget.delete(0, tk.END)
            elif isinstance(widget, tk.Checkbutton): widget.deselect()
            elif isinstance(widget, tk.Radiobutton): widget.deselect()
            elif isinstance(widget, tk.Listbox): widget.selection_clear(0, tk.END)

    def change_page(self, page):
        """
        Cambia de este frame a otro, verifica que el frame desde el que cambias es el actual
        :param page: El frame al que se quiere transportar
        """
        if self.master.current_frame == self:
            if self._clear_widgest: self._clear_widgets_in_frame()
            self.master.change_frame(page)
        else: raise SyntaxError("Estas realizando un cambio de página desde un frame que no es el actual")

class PagePrincipal(Page):
    def __init__(self, master, **kwargs):
        super().__init__(master=master, **kwargs)
        master.set_principal_page(self)

class ScrollFrame(tk.Frame):
    def __init__(self, master, vbar_position="right", hbar_position='bottom', **kwargs):
        super().__init__(master=master, **kwargs)
        if int(self.cget('width')) > 0 and int(self.cget('height')) > 0: self.pack_propagate(False)
        self.__canvas_scroll = tk.Canvas(self, bg= '#5ECFFF')
        self.__canvas_scroll.pack_propagate(False)
        # BARRAS PARA MOVER (SE ME OLVIDO COMO SE DICEN EN ESPAÑOL xd)
        self.__vbar = tk.Scrollbar(self, orient="vertical")  # VERTICAL BAR
        self.__vbar.config(command=self.__canvas_scroll.yview)
        self.__hbar = tk.Scrollbar(self, orient="horizontal")  # HORIZONTAL BAR
        self.__hbar.config(command=self.__canvas_scroll.xview)
        #Configura el vbar y hbar para alinearlos dentro de este frame y se ajusta el comando que se llama cuando se actualiza el scroll
        self.__canvas_scroll.config(xscrollcommand=self.__hbar.set, yscrollcommand=self.__vbar.set)
        self.__vbar.pack(side=vbar_position, fill="y")
        self.__hbar.pack(side=hbar_position, fill="x")

        self.__canvas_scroll.pack(side="left", expand=True, fill='both')
        self.__sub_frame = tk.Frame(self.__canvas_scroll, width=self.cget('width'), height=self.cget('height'))
        self.__sub_frame.pack_propagate(False)
        self.__canvas_scroll.create_window((0, 0), window=self.__sub_frame, anchor="nw")
        self.__sub_frame.bind("<Configure>",
                              lambda e: self.__canvas_scroll.configure(
                                  scrollregion=self.__canvas_scroll.bbox("all")))

    def pack_on_scroll(self, widget:tk.Widget, **kwargs):
        widget.pack(**kwargs)
        # Actualiza el canvas por cada pack
        self.__canvas_scroll.configure(scrollregion=self.__canvas_scroll.bbox("all"))

    @property
    def scr_frame(self):
        return self.__sub_frame
