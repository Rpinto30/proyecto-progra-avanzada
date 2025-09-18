from menus.graphic_tools import Window
from Login_menu import Login


root = Window('Ventana', (1920, 1080))

log = Login(root)
root.mainloop()