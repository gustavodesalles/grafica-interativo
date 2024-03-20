import tkinter as tk

import numpy as np

from transformation_2d import Transformation2D


class GraphicsSystem2D:
    def __init__(self, master, display_file, object_list):
        self.master = master
        self.display_file = display_file
        self.object_list = object_list

        self.canvas = tk.Canvas(master, width=800, height=500, bg='white')
        self.canvas.pack(side=tk.LEFT)

        self.object_list_frame = tk.Frame(master)
        self.object_list_frame.pack(side=tk.RIGHT)
        self.object_list_title = tk.Label(self.object_list_frame, text="Object List")
        self.object_list_title.pack()
        self.object_list_label = tk.Label(self.object_list_frame, text="")
        self.object_list_label.pack()
        self.object_name_label = tk.Label(self.object_list_frame, text="Object Name:")
        self.object_name_label.pack()
        self.entry_object_name = tk.Entry(self.object_list_frame)
        self.entry_object_name.pack()
        self.button_remove_object = tk.Button(self.object_list_frame, text="Remove Object", command=self.remove_object)
        self.button_remove_object.pack()

        self.label_object_name = tk.Label(self.master, text="Object Name:")
        self.label_object_name.place(x=900, y=300)

        self.entry_object_name_transform = tk.Entry(self.master)
        self.entry_object_name_transform.place(x=900, y=330)

        self.window = [-300, -200, 300, 200]  # Coordenadas da janela
        self.viewport = [100, 100, 700, 400]  # Coordenadas da viewport

        # Adicionar rótulos para viewport e window
        self.label_viewport = tk.Label(master, text="Viewport", font=('Helvetica', 14))
        self.label_viewport.place(x=650, y=10)
        self.label_window = tk.Label(master, text="Window", font=('Helvetica', 14))
        self.label_window.place(x=100, y=10)

        # Desenhar a borda da viewport
        self.viewport_border = self.canvas.create_rectangle(*self.viewport, outline='red', dash=(5, 5))

        # Desenhar a borda da janela
        self.window_border = self.canvas.create_rectangle(*self.window, outline='blue')

        self.setup_transformation_interface()

    def transform_to_viewport(self, x, y):
        xmin, ymin, xmax, ymax = self.window
        xvmin, yvmin, xvmax, yvmax = self.viewport

        xv = ((x - xmin) / (xmax - xmin)) * (xvmax - xvmin) + xvmin
        yv = (1 - (y - ymin) / (ymax - ymin)) * (yvmax - yvmin) + yvmin

        return xv, yv

    def setup_transformation_interface(self):
        self.label_transformation = tk.Label(self.master, text="Transformation")
        self.label_transformation.place(x=1050, y=200)

        self.entry_transformation = tk.Entry(self.master)
        self.entry_transformation.place(x=1050, y=230)

        self.label_params = tk.Label(self.master, text="Params (comma separated)")
        self.label_params.place(x=1050, y=260)

        self.entry_params = tk.Entry(self.master)
        self.entry_params.place(x=1050, y=290)

        self.button_transform = tk.Button(self.master, text="Transform Object", command=self.transform_object)
        self.button_transform.place(x=1050, y=320)

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
        obj_type, coordinates = self.display_file.objects[obj_name]
        if obj_type == 'point':
            new_coordinates = np.dot(transformation_matrix, np.array([coordinates[0], coordinates[1], 1]))
            self.display_file.objects[obj_name] = ('point', (new_coordinates[0], new_coordinates[1]))
        elif obj_type == 'line':
            new_coords = []
            for coord in coordinates:
                new_coord = np.dot(transformation_matrix, np.array([coord[0], coord[1], 1]))
                new_coords.append((new_coord[0], new_coord[1]))
            self.display_file.objects[obj_name] = ('line', (new_coords[0], new_coords[1]))
        elif obj_type == 'wireframe':
            new_coords = []
            for coord in coordinates:
                new_coord = np.dot(transformation_matrix, np.array([coord[0], coord[1], 1]))
                new_coords.append((new_coord[0], new_coord[1]))
            self.display_file.objects[obj_name] = ('wireframe', new_coords)

    def draw_object(self, obj_type, coordinates):
        if obj_type == 'point':
            x, y = self.transform_to_viewport(*coordinates)
            self.canvas.create_oval(x, y, x+2, y+2, fill='black')
        elif obj_type == 'line':
            x1, y1 = self.transform_to_viewport(*coordinates[0])
            x2, y2 = self.transform_to_viewport(*coordinates[1])
            self.canvas.create_line(x1, y1, x2, y2, fill='black')
        elif obj_type == 'wireframe':
            transformed_coords = [self.transform_to_viewport(*coord) for coord in coordinates]
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
        self.viewport_border = self.canvas.create_rectangle(*self.viewport, outline='red', dash=(5, 5))
        self.window_border = self.canvas.create_rectangle(*self.window, outline='blue')

        for obj_name, (obj_type, coordinates) in self.display_file.objects.items():
            self.draw_object(obj_type, coordinates)

        # Atualizar a lista de objetos
        object_names = "\n".join(self.display_file.objects.keys())
        self.object_list_label.config(text=object_names)

    def pan(self, dx, dy):
        self.window[0] += dx
        self.window[1] += dy
        self.window[2] += dx
        self.window[3] += dy

    def zoom(self, factor):
        cx = (self.window[0] + self.window[2]) / 2
        cy = (self.window[1] + self.window[3]) / 2

        self.window[0] = cx - (cx - self.window[0]) * factor
        self.window[1] = cy - (cy - self.window[1]) * factor
        self.window[2] = cx + (self.window[2] - cx) * factor
        self.window[3] = cy + (self.window[3] - cy) * factor

        self.draw_display_file()

    def remove_object(self):
        object_name = self.entry_object_name.get()
        self.display_file.remove_object(object_name)
        self.draw_display_file()
