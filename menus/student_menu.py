from graphic_tools import Window, PagePrincipal

root = Window('Test', (1920,1080))

COLOR_BG = '#669BBC'

class StudentMenu(PagePrincipal):
    def __init__(self, master:Window, **kwargs):
        super().__init__(master, bg=COLOR_BG,**kwargs)

S = StudentMenu(root)

root.mainloop()