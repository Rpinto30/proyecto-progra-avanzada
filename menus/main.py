from menus.graphic_tools import Window
from Login_menu import Login

root = Window('Gestor de notas - Universidad RAR', (1920, 1080), icon_image=r'sources\Logo_iso.png')

log = Login(root)
root.mainloop()