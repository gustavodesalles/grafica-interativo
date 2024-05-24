import tkinter as tk
from display_file_3d import DisplayFile3D
from graphics_system_3d import GraphicsSystem3D

# Exemplo de uso - main file
root = tk.Tk()
root.title("3D Graphics System")
root.geometry("1200x1000")

display_file = DisplayFile3D()
# Exemplo de adicionar objetos

coordinates1 = (50, 50, 50)
coordinates2 = [
    (45, 45, 50), (255, 45, 50), (255, 255, 50),
    (45, 255, 50), (45, 45, 50), (45, 45, 710),
    (255, 45, 710), (255, 45, 50), (255, 45, 710),
    (255, 255, 710), (255, 255, 50), (255, 255, 710),
    (45, 255, 710), (45, 255, 50), (45, 255, 710), (45, 45, 710)
]

coordinates3 = [
    (45, 45, 50), (255, 45, 50), (255, 255, 50),
    (45, 255, 50), (45, 45, 50), (45, 45, 710),
    (255, 45, 710), (255, 45, 50), (255, 45, 710),
    (255, 255, 710), (255, 255, 50), (255, 255, 710),
    (45, 255, 710), (45, 255, 50), (45, 255, 710), (45, 45, 710)
]

display_file.add_point(coordinates1, color='red')
#display_file.add_polygon(coordinates2, color='blue')
#display_file.add_bezier_surface(coordinates3, color='blue')
display_file.add_b_spline_surface(coordinates3, color='blue')

object_list = tk.Listbox(root)
graphics_system = GraphicsSystem3D(root, display_file, object_list)
graphics_system.draw_display_file()

root.mainloop()