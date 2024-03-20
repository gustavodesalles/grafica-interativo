import tkinter as tk

from display_file_2d import DisplayFile2D
from graphics_system_2d import GraphicsSystem2D

# Exemplo de uso - main file
root = tk.Tk()
root.title("2D Graphics System")

display_file = DisplayFile2D()
display_file.add_line(((-50, -50), (50, 50)))
display_file.add_point((0, 0))
display_file.add_wireframe([(100, -100), (100, 100), (-100, 100), (-100, -100)])

object_list = tk.Listbox(root)

graphics_system = GraphicsSystem2D(root, display_file, object_list)
graphics_system.draw_display_file()

def pan_left():
    graphics_system.pan(-20, 0)
    graphics_system.draw_display_file()

def pan_right():
    graphics_system.pan(20, 0)
    graphics_system.draw_display_file()

def zoom_in():
    graphics_system.zoom(0.8)
    graphics_system.draw_display_file()

def zoom_out():
    graphics_system.zoom(1.2)
    graphics_system.draw_display_file()

def add_object():
    coordinates_str = entry_coordinates.get()
    coordinates = eval(coordinates_str)
    display_file.add_wireframe(coordinates)
    graphics_system.draw_display_file()

button_pan_left = tk.Button(root, text="Pan Left", command=pan_left)
button_pan_left.pack(side=tk.TOP)

button_pan_right = tk.Button(root, text="Pan Right", command=pan_right)
button_pan_right.pack(side=tk.TOP)

button_zoom_in = tk.Button(root, text="Zoom In", command=zoom_in)
button_zoom_in.pack(side=tk.TOP)

button_zoom_out = tk.Button(root, text="Zoom Out", command=zoom_out)
button_zoom_out.pack(side=tk.TOP)

label_coordinates = tk.Label(root, text="Coordinates:")
label_coordinates.pack(side=tk.TOP)

entry_coordinates = tk.Entry(root)
entry_coordinates.pack(side=tk.TOP)

button_add_object = tk.Button(root, text="Add Object", command=add_object)
button_add_object.pack(side=tk.TOP)

root.mainloop()
