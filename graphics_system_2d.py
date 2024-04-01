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
        self.setup_rotation_interface()

        self.angle_vup = 0  # Inicializa o ângulo de rotação de Vup como 0

    def transform_to_viewport(self, x, y):
        # Obter os ângulos de rotação
        theta = np.radians(self.angle_vup)
        cos_theta = np.cos(theta)
        sin_theta = np.sin(theta)

        # Aplicar rotação para alinhar vup com o eixo Y
        x_rotated = x * cos_theta - y * sin_theta
        y_rotated = x * sin_theta + y * cos_theta

        # Normalizar coordenadas
        xmin, ymin, xmax, ymax = self.window.xmin, self.window.ymin, self.window.xmax, self.window.ymax
        xvmin, yvmin, xvmax, yvmax = self.viewport

        xv = ((x_rotated - xmin) / (xmax - xmin)) * (xvmax - xvmin) + xvmin
        yv = (1 - (y_rotated - ymin) / (ymax - ymin)) * (yvmax - yvmin) + yvmin

        return xv, yv, x_rotated, y_rotated

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

        self.color_string = tk.StringVar()
        self.c1 = tk.Radiobutton(self.master, text="Red", value="red", variable=self.color_string)
        self.c2 = tk.Radiobutton(self.master, text="Green", value="green", variable=self.color_string)
        self.c3 = tk.Radiobutton(self.master, text="Blue", value="blue", variable=self.color_string)
        self.c1.pack()
        self.c2.pack()
        self.c3.pack()

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

        # self.entry_transformation = tk.Entry(self.master)
        self.entry_transformation = tk.StringVar()
        self.r1 = tk.Radiobutton(self.master, text="Translation", value="translation", variable=self.entry_transformation)
        self.r2 = tk.Radiobutton(self.master, text="Scaling", value="scaling", variable=self.entry_transformation)
        self.r3 = tk.Radiobutton(self.master, text="Rotation around origin", value="rotation", variable=self.entry_transformation)
        self.r4 = tk.Radiobutton(self.master, text="Rotation around object's center", value="center_rotation", variable=self.entry_transformation)
        self.r5 = tk.Radiobutton(self.master, text="Rotation around arbitrary point", value="arbitrary_rotation", variable=self.entry_transformation)
        self.r1.pack()
        self.r2.pack()
        self.r3.pack()
        self.r4.pack()
        self.r5.pack()

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

    def setup_rotation_interface(self):
        self.label_rotation = tk.Label(self.master, text="Rotation Angle (Vup):")
        self.label_rotation.pack()
        self.entry_rotation = tk.Entry(self.master)
        self.entry_rotation.pack()
        self.button_rotate_object = tk.Button(self.object_list_frame, text="Rotate Object", command=self.rotate_vup)
        self.button_rotate_object.pack()

    def transform_object(self):
        obj_name = self.entry_object_name_transform.get()
        if obj_name not in self.display_file.objects:
            print("OBJECT DOES NOT EXIST")
            return

        transformation = self.entry_transformation.get().lower()
        transformation_params = self.entry_params.get().split(',')
        transformation_matrix = None
        obj = self.display_file.objects[obj_name]

        if transformation == 'translation':
            tx, ty = map(float, transformation_params)
            theta = np.radians(- self.angle_vup)
            cos_theta = np.cos(theta)
            sin_theta = np.sin(theta)
            tx_r = tx * cos_theta - ty * sin_theta
            ty_r = tx * sin_theta + ty * cos_theta
            transformation_matrix = Transformation2D.translation(tx_r, ty_r)
        elif transformation == 'rotation':
            angle = float(transformation_params[0])
            transformation_matrix = Transformation2D.rotation(angle)
        elif transformation == 'scaling':
            sx, sy = map(float, transformation_params)
            center = self.get_object_center(obj)
            transformation_matrix = Transformation2D.scale(sx, sy, center)
        elif transformation == 'arbitrary_rotation':
            angle = float(transformation_params[0])
            center = tuple(map(float, transformation_params[1:]))
            transformation_matrix = Transformation2D.arbitrary_rotation(angle, center)
        elif transformation == 'center_rotation':
            angle = float(transformation_params[0])
            center = self.get_object_center(obj)
            transformation_matrix = Transformation2D.arbitrary_rotation(angle, center)

        if transformation_matrix is not None:
            self.apply_transformation(obj, transformation_matrix)
            self.draw_display_file()
        else:
            print('No transformation')

    def apply_transformation(self, obj, transformation_matrix):
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
                point_vector = np.dot(transformation_matrix, np.array([point[0], point[1], 1]))
                obj.point_list[i] = (point_vector[0], point_vector[1])

    def draw_object(self, obj):
        if obj.type == 'Point':
            x, y, obj.coordinate_x_scn, obj.coordinate_y_scn = self.transform_to_viewport(obj.coordinate_x, obj.coordinate_y)
            self.canvas.create_oval(x, y, x+2, y+2, fill=obj.color)
        elif obj.type == 'Line':
            x1, y1, obj.start_point_scn[0], obj.start_point_scn[1] = self.transform_to_viewport(obj.start_point[0], obj.start_point[1])
            x2, y2, obj.end_point_scn[0], obj.end_point_scn[1] = self.transform_to_viewport(obj.end_point[0], obj.end_point[1])
            self.canvas.create_line(x1, y1, x2, y2, fill=obj.color)
        elif obj.type == 'Wireframe':
            transformed_coords = []
            for i in range(len(obj.point_list)):
                point = obj.point_list[i]
                x, y, obj.point_list_scn[i][0], obj.point_list_scn[i][1] = self.transform_to_viewport(point[0], point[1])
                transformed_coords.append((x, y))
            self.draw_wireframe(transformed_coords, obj.color)

    def draw_wireframe(self, coordinates, color):
        # Desenhar as linhas do polígono
        for i in range(len(coordinates)):
            x1, y1 = coordinates[i]
            x2, y2 = coordinates[(i + 1) % len(coordinates)]
            self.canvas.create_line(x1, y1, x2, y2, fill=color)

    def rotate_vup(self):
        angle = float(self.entry_rotation.get())
        self.angle_vup = angle
        self.draw_display_file()

    def draw_display_file(self):
        self.canvas.delete('all')

        try:
            self.angle_vup = float(self.entry_rotation.get())
        except ValueError:
            self.angle_vup = 0  # Definir como 0 se a entrada não for válida

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
        self.pan(20, 0)
        self.draw_display_file()

    def pan_right(self):
        self.pan(-20, 0)
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
        object_color = self.color_string.get()
        coordinates = coordinates_str.split(",")
        coordinates_head = coordinates.pop(0)
        coordinates = list(map(lambda x: int(x), coordinates))
        coordinates = [(coordinates[i], coordinates[i+1]) for i in range(0, len(coordinates), 2)]

        if coordinates_head.upper() == "POINT":
            self.display_file.add_point(coordinates[0], object_color)
        elif coordinates_head.upper() == "LINE":
            self.display_file.add_line(coordinates, object_color)
        elif coordinates_head.upper() == "WIREFRAME":
            self.display_file.add_wireframe(coordinates, object_color)
        else:
            print("Unable to add object")
        self.draw_display_file()

    def remove_object(self):
        object_name = self.entry_object_name.get()
        self.display_file.remove_object(object_name)
        self.draw_display_file()

    def get_object_center(self, obj):
        if obj.type == "Point":
            return obj.coordinate_x, obj.coordinate_y
        elif obj.type == "Line":
            return (obj.start_point[0] + obj.end_point[0]) / 2, (obj.start_point[1] + obj.end_point[1]) / 2
        elif obj.type == "Wireframe":
            center_x = sum([p[0] for p in obj.point_list]) / len(obj.point_list)
            center_y = sum([p[1] for p in obj.point_list]) / len(obj.point_list)
            return center_x, center_y
