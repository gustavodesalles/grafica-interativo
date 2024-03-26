import tkinter as tk

import numpy as np

from transformation_2d import Transformation2D
from window import Window


class GraphicsSystem2D:
    def __init__(self, master, display_file, object_list):
        self.master = master
        self.display_file = display_file
        self.object_list = object_list

        self.canvas = tk.Canvas(master, width=800, height=500, bg='white')
        self.canvas.pack(side=tk.LEFT)

        # self.window = [-300, -200, 300, 200]  # Coordenadas da janela
        self.window = Window(-300, -200, 300, 200)
        self.viewport = [100, 100, 700, 400]  # Coordenadas da viewport

        # Adicionar rótulos para viewport e window
        # self.label_viewport = tk.Label(master, text="Viewport", font=('Helvetica', 14))
        # self.label_viewport.place(x=650, y=10)
        # self.label_window = tk.Label(master, text="Window", font=('Helvetica', 14))
        # self.label_window.place(x=100, y=10)

        # Desenhar a borda da viewport
        # self.viewport_border = self.canvas.create_rectangle(*self.viewport, outline='red', dash=(5, 5))

        # Desenhar a borda da janela
        # self.window_border = self.canvas.create_rectangle(*self.window, outline='blue')

        self.setup_object_list_interface()
        self.setup_pan_interface()
        self.setup_zoom_interface()
        self.setup_add_object_interface()
        self.setup_remove_object_interface()
        self.setup_transformation_interface()

    def transform_to_viewport(self, x, y):
        xmin, ymin, xmax, ymax = self.window.xmin, self.window.ymin, self.window.xmax, self.window.ymax
        xvmin, yvmin, xvmax, yvmax = self.viewport

        xv = ((x - xmin) / (xmax - xmin)) * (xvmax - xvmin) + xvmin
        yv = (1 - (y - ymin) / (ymax - ymin)) * (yvmax - yvmin) + yvmin

        return xv, yv

    def setup_object_list_interface(self):
        self.object_list_frame = tk.Frame(self.master)
        self.object_list_frame.pack(side=tk.RIGHT)
        self.object_list_title = tk.Label(self.object_list_frame, text="Object List")
        self.object_list_title.pack()
        self.object_list_label = tk.Label(self.object_list_frame, text="")
        self.object_list_label.pack()

    def setup_remove_object_interface(self):
        self.object_name_label = tk.Label(self.object_list_frame, text="Object Name:")
        self.object_name_label.pack()
        self.entry_object_name = tk.Entry(self.object_list_frame)
        self.entry_object_name.pack()
        self.button_remove_object = tk.Button(self.object_list_frame, text="Remove Object", command=self.remove_object)
        self.button_remove_object.pack()

    def setup_object_list_interface(self):
        self.object_list_frame = tk.Frame(self.master)
        self.object_list_frame.pack(side=tk.RIGHT)
        self.object_list_title = tk.Label(self.object_list_frame, text="Object List")
        self.object_list_title.pack()
        self.object_list_label = tk.Label(self.object_list_frame, text="")
        self.object_list_label.pack()

    def setup_remove_object_interface(self):
        self.object_name_label = tk.Label(self.object_list_frame, text="Object Name:")
        self.object_name_label.pack()
        self.entry_object_name = tk.Entry(self.object_list_frame)
        self.entry_object_name.pack()
        self.button_remove_object = tk.Button(self.object_list_frame, text="Remove Object", command=self.remove_object)
        self.button_remove_object.pack()

    def setup_add_object_interface(self):
        self.label_coordinates = tk.Label(self.master, text="Coordinates:")
        self.label_coordinates.pack(side=tk.TOP)

        self.entry_coordinates = tk.Entry(self.master)
        self.entry_coordinates.pack(side=tk.TOP)

        self.button_add_object = tk.Button(self.master, text="Add Object", command=self.add_object)
        self.button_add_object.pack(side=tk.TOP)
        
    def setup_pan_interface(self):
        button_pan_left = tk.Button(self.master, text="Pan Left", command=self.pan_left)
        button_pan_left.pack(side=tk.TOP)

        button_pan_right = tk.Button(self.master, text="Pan Right", command=self.pan_right)
        button_pan_right.pack(side=tk.TOP)

    def setup_zoom_interface(self):
        button_zoom_in = tk.Button(self.master, text="Zoom In", command=self.zoom_in)
        button_zoom_in.pack(side=tk.TOP)

        button_zoom_out = tk.Button(self.master, text="Zoom Out", command=self.zoom_out)
        button_zoom_out.pack(side=tk.TOP)

    def setup_transformation_interface(self):
        self.label_transformation = tk.Label(self.master, text="Transformation")
        self.label_transformation.pack()

        self.entry_transformation = tk.Entry(self.master)
        self.entry_transformation.pack()

        self.label_object_name = tk.Label(self.master, text="Object Name:")
        self.label_object_name.pack()

        self.entry_object_name_transform = tk.Entry(self.master)
        self.entry_object_name_transform.pack()

        self.label_params = tk.Label(self.master, text="Params (comma separated)")
        self.label_params.pack()

        self.entry_params = tk.Entry(self.master)
        self.entry_params.pack()

        self.button_transform = tk.Button(self.master, text="Transform Object", command=self.transform_object)
        self.button_transform.pack()

    def transform_object(self):
        obj_name = self.entry_object_name_transform.get()
        if obj_name not in self.display_file.objects:
            print("OBJECT DOES NOT EXIST")
            return

        transformation = self.entry_transformation.get()
        transformation_params = self.entry_params.get().split(',')

        if transformation == 'translation':
            tx, ty = map(float, transformation_params)
            transformation_matrix = Transformation2D.translation(tx, ty)
        elif transformation == 'rotation':
            angle = float(transformation_params[0])
            transformation_matrix = Transformation2D.rotation(angle)
        elif transformation == 'scaling':
            sx, sy = map(float, transformation_params)
            transformation_matrix = Transformation2D.scale(sx, sy)
        elif transformation == 'arbitrary_rotation':
            angle = float(transformation_params[0])
            center = tuple(map(float, transformation_params[1:]))
            transformation_matrix = Transformation2D.arbitrary_rotation(angle, center)

        self.apply_transformation(obj_name, transformation_matrix)
        self.draw_display_file()

    def apply_transformation(self, obj_name, transformation_matrix):
        obj = self.display_file.objects[obj_name]
        if obj.type == 'Point':
            new_coordinates = np.dot(transformation_matrix, np.array([obj.coordinate_x, obj.coordinate_y, 1]))
            obj.coordinate_x = new_coordinates[0]
            obj.coordinate_y = new_coordinates[1]
        elif obj.type == 'Line':
            obj.start_point = np.dot(transformation_matrix, np.array([obj.start_point[0], obj.start_point[1], 1]))
            obj.end_point = np.dot(transformation_matrix, np.array([obj.end_point[0], obj.end_point[1], 1]))
        elif obj.type == 'Wireframe':
            for i in range(len(obj.point_list)):
                point = obj.point_list[i]
                obj.point_list[i] = np.dot(transformation_matrix, np.array([point[0], point[1], 1]))

    def draw_object(self, obj):
        if obj.type == 'Point':
            x, y = self.transform_to_viewport(obj.coordinate_x, obj.coordinate_y)
            self.canvas.create_oval(x, y, x+2, y+2, fill='black')
        elif obj.type == 'Line':
            x1, y1 = self.transform_to_viewport(obj.start_point[0], obj.start_point[1])
            x2, y2 = self.transform_to_viewport(obj.end_point[0], obj.end_point[1])
            self.canvas.create_line(x1, y1, x2, y2, fill='black')
        elif obj.type == 'Wireframe':
            transformed_coords = [self.transform_to_viewport(point[0], point[1]) for point in obj.point_list]
            self.draw_wireframe(transformed_coords)

    def draw_wireframe(self, coordinates):
        # Desenhar as linhas do polígono
        for i in range(len(coordinates)):
            x1, y1 = coordinates[i]
            x2, y2 = coordinates[(i + 1) % len(coordinates)]
            self.canvas.create_line(x1, y1, x2, y2, fill='black')

        # Preencher o interior do polígono manualmente
        scanline_y = min(y for x, y in coordinates)
        while scanline_y <= max(y for x, y in coordinates):
            intersections = []
            for i in range(len(coordinates)):
                x1, y1 = coordinates[i]
                x2, y2 = coordinates[(i + 1) % len(coordinates)]
                if y1 != y2 and (y1 <= scanline_y <= y2 or y2 <= scanline_y <= y1):
                    x_intersect = x1 + (scanline_y - y1) * (x2 - x1) / (y2 - y1)
                    intersections.append(x_intersect)
            intersections.sort()
            for i in range(0, len(intersections), 2):
                self.canvas.create_line(intersections[i], scanline_y, intersections[i + 1], scanline_y, fill='black')
            scanline_y += 1

    def draw_display_file(self):
        self.canvas.delete('all')

        # Redesenha as bordas
        # self.viewport_border = self.canvas.create_rectangle(*self.viewport, outline='red', dash=(5, 5))
        # self.window_border = self.canvas.create_rectangle(*self.window, outline='blue')

        for obj in self.display_file.objects.values():
            self.draw_object(obj)

        # Atualizar a lista de objetos
        object_names = "\n".join(self.display_file.objects.keys())
        self.object_list_label.config(text=object_names)

    def pan(self, dx, dy):
        # self.window[0] += dx
        # self.window[1] += dy
        # self.window[2] += dx
        # self.window[3] += dy
        self.window.xmin += dx
        self.window.ymin += dy
        self.window.xmax += dx
        self.window.ymax += dy

    def pan_left(self):
        self.pan(-20, 0)
        self.draw_display_file()

    def pan_right(self):
        self.pan(20, 0)
        self.draw_display_file()

    def zoom(self, factor):
        cx = (self.window.xmin + self.window.xmax) / 2
        cy = (self.window.ymin + self.window.ymax) / 2

        self.window.xmin = cx - (cx - self.window.xmin) * factor
        self.window.ymin = cy - (cy - self.window.ymin) * factor
        self.window.xmax = cx + (self.window.xmax - cx) * factor
        self.window.ymax = cy + (self.window.ymax - cy) * factor

        self.draw_display_file()

    def zoom_in(self):
        self.zoom(0.8)
        self.draw_display_file()

    def zoom_out(self):
        self.zoom(1.2)
        self.draw_display_file()

    def add_object(self):
        coordinates_str = self.entry_coordinates.get()
        coordinates = coordinates_str.split(",")
        coordinates_head = coordinates.pop(0)
        coordinates = list(map(lambda x: int(x), coordinates))
        coordinates = [(coordinates[i], coordinates[i+1]) for i in range(0, len(coordinates), 2)]

        if coordinates_head.upper() == "POINT":
            self.display_file.add_point(coordinates[0])
        elif coordinates_head.upper() == "LINE":
            self.display_file.add_line(coordinates)
        elif coordinates_head.upper() == "WIREFRAME":
            self.display_file.add_wireframe(coordinates)
        else:
            print("Unable to add object")
        self.draw_display_file()

    def remove_object(self):
        object_name = self.entry_object_name.get()
        self.display_file.remove_object(object_name)
        self.draw_display_file()
