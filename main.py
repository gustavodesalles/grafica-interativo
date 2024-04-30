import tkinter as tk
from display_file_3d import DisplayFile3D
from graphics_system_3d import GraphicsSystem3D

# Exemplo de uso - main file
root = tk.Tk()
root.title("3D Graphics System")
root.geometry("1200x1000")

display_file = DisplayFile3D()
# Exemplo de adicionar objetos
# display_file.add_point((50, 50, 50), color='red')
# display_file.add_line([(-50, -50, -50), (50, 50, 50)], color='red')
coordinates = [(0, 0, 0), (100, 0, 0), (100, 100, 0), (0, 100, 0)]
display_file.add_polygon(coordinates, color='blue', filled=False)


object_list = tk.Listbox(root)
graphics_system = GraphicsSystem3D(root, display_file, object_list)
graphics_system.draw_display_file()

root.mainloop()