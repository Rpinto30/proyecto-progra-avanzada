import tkinter as tk

class Window(tk.Tk):
    # DOCSTRING: https://www.datacamp.com/tutorial/docstrings-python
    def __init__(self, title='ventana', geometry:tuple[int, int]=(500,500), icon_image='', **kwargs):
        """
        Crea una ventana, usar como si fuese el tipico root = tk.Tk()
        Por defecto muestra un frame en blanco, pero se le puede asignar uno
        usando set_principal_page()

        :param title: Título de la ventana
        :param geometry: Geometria en píxeles de la ventana
        :param icon_image: Si existe, coloca una imagen de icono
        :param kwargs: Hereda parámetros de la clase tk.TK()
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
    def __init__(self, master, vbar_position=None, hbar_position=None, **kwargs):
        super().__init__(master=master, **kwargs)
        if int(self.cget('width')) > 0 and int(self.cget('height')) > 0: self.pack_propagate(False)
        self._canvas_scroll = tk.Canvas(self, width=self.cget('width'), height=self.cget('height'), bg= self.cget('bg'))
        #self.__canvas_scroll.pack_propagate(False)
        # BARRAS PARA MOVER (SE ME OLVIDO COMO SE DICEN EN ESPAÑOL xd)
        self.__vbar = tk.Scrollbar(self, orient="vertical")  # VERTICAL BAR
        self.__vbar.config(command=self._canvas_scroll.yview)
        self.__hbar = tk.Scrollbar(self, orient="horizontal")  # HORIZONTAL BAR
        self.__hbar.config(command=self._canvas_scroll.xview)
        #Configura el vbar y hbar para alinearlos dentro de este frame y se ajusta el comando que se llama cuando se actualiza el scroll
        self._canvas_scroll.config(xscrollcommand=self.__hbar.set, yscrollcommand=self.__vbar.set)
        if vbar_position is not None: self.__vbar.pack(side=vbar_position, fill="y")
        if hbar_position is not None: self.__hbar.pack(side=hbar_position, fill="x")

        self._canvas_scroll.pack(side="left", expand=True, fill='both')
        self.__sub_frame = tk.Frame(self._canvas_scroll, width=self.cget('width'), height=self.cget('height'), bg= self.cget('bg'))
        #self.__sub_frame.pack_propagate(False)
        self._canvas_scroll.create_window((0, 0), window=self.__sub_frame, anchor="nw")
        self.__sub_frame.bind("<Configure>",
                              lambda e: self._canvas_scroll.configure(
                                  scrollregion=self._canvas_scroll.bbox("all")))

    def pack_on_scroll(self, widget:tk.Widget, **kwargs):
        widget.pack(**kwargs)
        # Actualiza el canvas por cada pack
        self._canvas_scroll.configure(scrollregion=self._canvas_scroll.bbox("all"))

    @property
    def scr_frame(self):
        return self.__sub_frame

class Tabla(ScrollFrame):
    def __init__(self, master, matrix:list,
                 vbar_position=None, hbar_position=None,
                 cell_width=10, cell_height=1,
                 font_size = 12, propagate_width:int=0, propagate_height:int=0,
                 borderwidth:int= 1,
                 color_header:str='#A9B1D1', color_first_colum:str='',
                 color_first:str='',
                 **kwargs):
        super().__init__(master, vbar_position, hbar_position,**kwargs)
        self.__rows =len(matrix)
        self.__colums=len(matrix[0])
        self.__table = tk.Frame(self.scr_frame, bg='#58FFB2')
        for i in range(self.__rows): #ROWS
            row = []
            self.__table.grid_rowconfigure(i, weight=1)
            for j in range(self.__colums): #COLUMS
                try:
                    e = tk.Label(self.__table, fg='black', font=("Arial", font_size), text=matrix[i][j], relief='solid', borderwidth=borderwidth)
                except IndexError: e = tk.Label(self.__table, fg='black', font=("Arial", font_size), text=" ", relief='solid', borderwidth=borderwidth)
                e.config(width=cell_width, height=cell_height)
                #---------------------COLOR DE COLUMNAS---------------------------
                if i == 0 and j%self.__colums==0 and color_first != '': e.config(bg=color_first)
                elif i == 0 and color_header != '': e.config(bg=color_header)
                elif j%self.__colums==0 and color_first_colum != '': e.config(bg=color_first_colum)

                e.grid(row=i, column=j)
                row.append(e)
        if propagate_height <= 0 or propagate_width == 0: self.master.update_idletasks()  # Actualiza tkinter para la lectura de la geometria
        if propagate_width <= 0:
            self._canvas_scroll.config(
                width=[a for a in self.__table.winfo_children()][0].winfo_width()*(len(matrix[0])))
        else:
            self._canvas_scroll.config(
                width=[a for a in self.__table.winfo_children()][0].winfo_width() * int(propagate_width))
        if propagate_height <= 0:
            self._canvas_scroll.config(
                height=[a for a in self.__table.winfo_children()][0].winfo_reqheight()*(len(matrix)))
        else:
            self._canvas_scroll.config(
                height=[a for a in self.__table.winfo_children()][0].winfo_reqheight() * int(propagate_height))

        self.pack_on_scroll(self.__table)

    def pack_table(self, **kwargs):
        self.pack(**kwargs)

    def confi_row(self, index=0, height_=1):
        """
        Ajusta el tamaño de toda una columna
        :param index: El index de la columna que se desea modificar, por defecto 0
        :param height_: El tamaño que se desea que tenga la calumna seleccionada
        """
        for n_row, row in enumerate(self.__table.winfo_children(),0):
            if  n_row//self.__colums <= index:
                row.config(height=height_)

    def confi_colum(self, index=0, width_=1):
        """
        Ajusta el tamaño de toda una columna
        :param index: El index de la columna que se desea modificar, por defecto 0
        :param width_: El tamaño que se desea que tenga la calumna seleccionada
        """
        for n_row, row in enumerate(self.__table.winfo_children(),0):
            if index == n_row%self.__colums:
                row.config(width=width_)
