import tkinter as tk

from display_file_2d import DisplayFile2D
from graphics_system_2d import GraphicsSystem2D

# Exemplo de uso - main file
root = tk.Tk()
root.title("2D Graphics System")
root.geometry("1200x1000")

display_file = DisplayFile2D()
# display_file.add_line(((-50, -50), (50, 50)), 'red')
# display_file.add_point((0, 0))
# display_file.add_wireframe([(100, -100), (100, 100), (-100, 100), (-100, -100)], 'blue')
# control_points = [(-50, -50), (100, 0), (100, 0), (100, 100), (-50, 50), (0, 100), (0, 100), (-100, 100)]
# control_points = [(20, 20), (50, 20), (100, 50), (200, 50)]
# display_file.add_b_spline(control_points, 'red')

object_list = tk.Listbox(root)

graphics_system = GraphicsSystem2D(root, display_file, object_list)
graphics_system.draw_display_file()

root.mainloop()
