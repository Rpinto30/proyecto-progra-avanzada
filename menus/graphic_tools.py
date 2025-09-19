import tkinter as tk
import tkinter.ttk as ttk

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
        self.w = self.winfo_screenwidth()
        self.h = self.winfo_screenheight()
        # ----------------------------------WINDOWS-----------------------------------
        self.title(title)
        self.geometry(f"{self.w}x{self.h}")
        #self.resizable(True,True)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.protocol("WM_DELETE_WINDOW", self.exit_root)

        # ----------------------------------ICONO-----------------------------------
        if icon_image != '':
            icon_image = tk.PhotoImage(file=icon_image)
            self.iconphoto(True, icon_image)

        self.update_idletasks()

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

    @property
    def principal_page(self): return self.__principal_page

class Page(tk.Frame):
    # **kwargs para heredar todos los argumentos de tk.Frame
    # https://www.geeksforgeeks.org/python/packing-and-unpacking-arguments-in-python
    def __init__(self, master:Window | tk.Misc, **kwargs):
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

    def clear_widgets_in_frame(self):
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
            if self._clear_widgest: self.clear_widgets_in_frame()
            self.master.change_frame(page)
        else: raise SyntaxError("Estas realizando un cambio de página desde un frame que no es el actual")

    def return_main(self):
        if self.master.current_frame == self:
            if self._clear_widgest: self.clear_widgets_in_frame()
            self.master.change_frame(self.master.principal_page)
        else:
            raise SyntaxError("Estas realizando un cambio de página desde un frame que no es el actual")

    def close_menu(self):
        pass

class PagePrincipal(Page):
    def __init__(self, master: Window | tk.Misc, **kwargs):
        super().__init__(master=master, **kwargs)
        master.set_principal_page(self)
class ScrollFrame(tk.Frame):
    def __init__(self, master, vbar_position=None, hbar_position=None,
                 cl_bars_bg='#ffffff', cl_bars_des='#ffffff', cl_bars_act='#ffffff', **kwargs):
        super().__init__(master=master, **kwargs)
        style = ttk.Style() #Aprendi a hacer estilo XD
        style.theme_use("alt")
        style.configure("Custom.Vertical.TScrollbar",
                        background=cl_bars_des,  #Los cosos de arriba
                        troughcolor=cl_bars_bg,  #El fondo
                        arrowcolor=cl_bars_bg,  #Las flechas
                        arrowsize=15, troughrelief='solid', relief='ridge')
        style.configure("Custom.Horizontal.TScrollbar",
                        background=cl_bars_des,  # Los cosos de arriba
                        troughcolor=cl_bars_bg,  # El fondo
                        arrowcolor=cl_bars_bg,  # Las flechas
                        arrowsize=15, troughrelief='solid', relief='ridge')
        style.map("Custom.Vertical.TScrollbar", background=[("active", cl_bars_act), ("!active", cl_bars_des)])
        self._canvas_scroll = tk.Canvas(self, width=self.cget('width'), height=self.cget('height'),bg=self.cget('bg'), highlightthickness=0, bd=0)
        self.__vbar = ttk.Scrollbar(self, orient="vertical", style="Custom.Vertical.TScrollbar")
        self.__vbar.config(command=self._canvas_scroll.yview)
        self.__hbar = ttk.Scrollbar(self, orient="horizontal", style="Custom.Horizontal.TScrollbar")
        self.__hbar.config(command=self._canvas_scroll.xview)
        self._canvas_scroll.config(xscrollcommand=self.__hbar.set, yscrollcommand=self.__vbar.set)
        if vbar_position is not None:self.__vbar.pack(side=vbar_position, fill="y")
        if hbar_position is not None:self.__hbar.pack(side=hbar_position, fill="x")


        self.__sub_frame = tk.Frame(self._canvas_scroll, bg=self.cget('bg'))
        self._canvas_scroll.create_window((0, 0), window=self.__sub_frame, anchor="nw")

        def confi_canvas_scroll():
            self.master.update_idletasks()

            def al_chile_mejor_lo_desactivo_xd(): pass

            # CUANDO LO QUE BOUDING BOX DEL CANVAS SEA MENOR A LA ALTURA DE ESTE FRAME
            if self._canvas_scroll.bbox('all')[3] <= self.cget('height'):
                self.__vbar.config(command=al_chile_mejor_lo_desactivo_xd) #El nombre ya dice que solución encontré JAJAJAJ
            else:
                self.__vbar.config(command=self._canvas_scroll.yview)
                self._canvas_scroll.configure(scrollregion=self._canvas_scroll.bbox('all'))

        self.__sub_frame.bind("<Configure>", lambda e: confi_canvas_scroll())

        self._canvas_scroll.pack(fill='both', expand=True)


    def pack_on_scroll(self, widget:tk.Widget, **kwargs):
        widget.pack(**kwargs)
        self._canvas_scroll.configure(scrollregion=self._canvas_scroll.bbox("all"))
    @property
    def scr_frame(self):return self.__sub_frame

class Tabla(ScrollFrame):
    def __init__(self, master:Window | tk.Misc| tk.Frame, matrix:list, bg:str,
                 vbar_position=None, hbar_position=None,
                 cell_width=10, cell_height=1,
                 font_size = 12, propagate_width:int=0, propagate_height:int=0,
                 borderwidth:int= 1,
                 color_header:str='#A9B1D1', color_first_colum:str='',
                 color_first:str='', color_table:str='', cell_command=None, select_mode=None, cursor ='arrow',
                 **kwargs):
        """
        Crea una tabla con información que se le pase, necesita una matriz
        [['VALOR1','VALOR2'],['VALOR3','VALOR4']], en caso faltar un item se llena la celda estando vacía.

        Por defecto la tabla se adapta al tamaño de columnas y filas, pero con propagate_width y
        propagate_height se puede configurar hasta cuantas filas o columnas se desea que aparezcan
        cuando la tabla se genera.

        :param master: En donde se coloca la tabla
        :param matrix: La matriz que muestra la tabla
        :param vbar_position: Opcional, si se desea tener una barra vertical
        :param hbar_position: Opciona, si se desea tener una barra horizontal
        :param cell_width: El largo de las celdas, la cantidad de caracteres
        :param cell_height: El alto de las celdas
        :param font_size: El tamaño de la fuente que se coloca en todas las celdas
        :param propagate_width: Opcional, la cantidad de columnas que entran en la tabla (recomendación: usar con hbar_position)
        :param propagate_height:Opcional, la cantidad de filas que entran en la tabla (recomendación: usar con vbar_position)
        :param borderwidth: Opcional, el tamaño del borde de la tabla
        :param color_header: Opcional, el color del encabezado de la tabla
        :param color_first_colum: Opcional, el color de la primera columna de la tabla
        :param color_first: Opcional, el color de la primera celda de la tabla
        :param color_table: Opcional, el color general de la tabla
        :param kwargs:
        """
        super().__init__(master, vbar_position, hbar_position, bg=bg,**kwargs)
        self.master = master
        self.matrix = matrix
        self.vbar_position = vbar_position
        self.hbar_position = hbar_position
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.font_size = font_size
        self.propagate_width = propagate_width
        self.propagate_height = propagate_height
        self.borderwidth = borderwidth
        self.color_header = color_header
        self.color_first_colum = color_first_colum
        self.color_first = color_first
        self.color_table = color_table

        self.cell_command = cell_command
        self.select_mode = select_mode
        self.cursor = cursor
        self.__create_table(self.matrix)

    def __create_table(self, matrix):
        self.__rows = len(matrix)
        self.__colums = len(matrix[0])
        self.__table = tk.Frame(self.scr_frame)
        for i in range(self.__rows):  # Filas
            row = []
            self.__table.grid_rowconfigure(i, weight=1)
            for j in range(self.__colums):  # Columnas
                text_value = self.matrix[i][j] if j < len(self.matrix[i]) else " "
                try:
                    e = tk.Label(
                        self.__table,
                        fg='black',
                        font=("Arial", self.font_size),
                        text=self.matrix[i][j],
                        relief='solid',
                        borderwidth=self.borderwidth, cursor=self.cursor
                    )
                except IndexError:
                    e = tk.Label(
                        self.__table,
                        fg='black',
                        font=("Arial", self.font_size),
                        text=" ",
                        relief='solid',
                        borderwidth=self.borderwidth, cursor=self.cursor
                    )

                # Tamaño fijo de la celda
                if i == 0: e.config(cursor='arrow')
                e.config(width=self.cell_width, height=self.cell_height)
                # --- Colores ---
                if self.color_table != '': e.config(bg=self.color_table)
                if i == 0 and j % self.__colums == 0 and self.color_first != '':e.config(bg=self.color_first)
                elif i == 0 and self.color_header != '':e.config(bg=self.color_header)
                elif j % self.__colums == 0 and self.color_first_colum != '':e.config(bg=self.color_first_colum)

                if self.cell_command:
                    def handler(event, row=i, col=j):
                        if self.select_mode == "row":
                            value = self.matrix[row] # primer elemento de la fila
                        elif self.select_mode == "column":
                            value = self.matrix[row][col]  # primer elemento de la columna
                        else:
                            value = self.matrix[row][col]  # valor normal
                        self.cell_command(row, col, value)
                    e.bind("<Button-1>", handler)
                e.grid(row=i, column=j)
                row.append(e)

        # --- Ajuste dinámico del canvas ---
        if self.propagate_height <= 0 or self.propagate_width == 0: self.master.update_idletasks()

        if self.propagate_width <= 0:
            self._canvas_scroll.config(width=[a for a in self.__table.winfo_children()][0].winfo_width() * len(self.matrix[0]))
        else:
            self._canvas_scroll.config(width=[a for a in self.__table.winfo_children()][0].winfo_width() * int(self.propagate_width))

        if self.propagate_height <= 0:
            self._canvas_scroll.config(height=[a for a in self.__table.winfo_children()][0].winfo_reqheight() * len(self.matrix))
        else:
            self._canvas_scroll.config(height=[a for a in self.__table.winfo_children()][0].winfo_reqheight() * int(self.propagate_height))

        self.pack_on_scroll(self.__table)

    def __on_cell_click(self, row, col):
        valor = self.matrix[row][col]
        self.click_row = row
        self.click_colum = col


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

    def confi_fg_cell(self, index=(0, 0), color='red'):
        for n_row, row in enumerate(self.__table.winfo_children(), 0):
            if index[1] == n_row%self.__colums and n_row//self.__colums == index[0]:
                row.config( fg=color)
                print(row.cget("text"))

    def confi_font_cell(self, index=(0, 0), font=('Arial',12)):
        for n_row, row in enumerate(self.__table.winfo_children(), 0):
            if index[1] == n_row%self.__colums and n_row//self.__colums == index[0]:
                row.config(font = font)
                print(row.cget("text"))

    def reload(self, matrix):
        self.matrix = matrix
        self.__table.destroy()
        self.__create_table(self.matrix)


def pack_create_line(master: tk.Frame,
                     l_type, left_kwargs: dict,
                     r_type, right_kwargs: dict,
                     _padx=0, _pady=0, width=0, height=0, bg='#f0f0f0'):
    row = tk.Frame(master, width=width+5, height=height, bg=bg)
    left = l_type(row, **left_kwargs)
    right = r_type(row, **right_kwargs)

    left.pack(side='left', padx=_padx, anchor='w')
    right.pack(side='right', padx=_padx, anchor='e')

    if width != 0 and height != 0: row.pack_propagate(False)
    row.pack(pady=_pady)
    return left, right