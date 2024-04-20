import tkinter as tk
from tkinter import ttk

import numpy as np

from obj_descriptor import OBJDescriptor
from transformation_2d import Transformation2D
from viewport import Viewport
from window import Window


class GraphicsSystem2D:
    def __init__(self, master, display_file, object_list):
        self.master = master
        self.display_file = display_file
        self.object_list = object_list

        self.canvas = tk.Canvas(master, width=800, height=500, bg='white')
        self.canvas.pack(side=tk.LEFT)
        canvas_width = self.canvas.winfo_reqwidth()
        canvas_height = self.canvas.winfo_reqheight()

        viewport_margin = 20
        # self.window = [-300, -200, 300, 200]  # Coordenadas da janela
        self.window = Window(0, 0, canvas_width, canvas_height)
        self.viewport = Viewport(canvas_width // 4 + viewport_margin,
                                 canvas_height // 4 + viewport_margin,
                                 3 * canvas_width // 4 - viewport_margin,
                                 3 * canvas_height // 4 - viewport_margin)  # Coordenadas da viewport

        # Desenhar uma moldura ao redor da viewport
        self.viewport_frame = self.canvas.create_rectangle(self.viewport.coordinates(), outline='green')

        # Inicializar a técnica de clipagem atual
        self.clipping_method = 'parametric'

        self.setup_object_list_interface()
        self.setup_pan_interface()
        self.setup_zoom_interface()
        self.setup_add_object_interface()
        self.setup_remove_object_interface()
        self.setup_transformation_interface()
        self.setup_rotation_interface()
        self.setup_export_object_interface()
        self.setup_import_object_interface()
        self.setup_clipping_interface()

        self.angle_vup = 0  # Inicializa o ângulo de rotação de Vup como 0

    def rotate_align_vup(self, x, y):
        # Obter os ângulos de rotação
        theta = np.radians(self.angle_vup)
        cos_theta = np.cos(theta)
        sin_theta = np.sin(theta)

        # Aplicar rotação para alinhar vup com o eixo Y
        x_rotated = x * cos_theta - y * sin_theta
        y_rotated = x * sin_theta + y * cos_theta
        return x_rotated, y_rotated

    def transform_to_viewport(self, x_rotated, y_rotated):
        # Normalizar coordenadas
        xmin, ymin, xmax, ymax = self.window.coordinates()
        xvmin, yvmin, xvmax, yvmax = self.viewport.coordinates()

        xv = ((x_rotated - xmin) / (xmax - xmin)) * (xvmax - xvmin) + xvmin
        yv = (1 - (y_rotated - ymin) / (ymax - ymin)) * (yvmax - yvmin) + yvmin

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

    def setup_add_object_interface(self):
        self.object_type = tk.StringVar()
        self.object_types_combobox = ttk.Combobox(self.master, state="readonly", textvariable=self.object_type,
                                                  values=['Point', 'Line', 'Wireframe'])
        self.object_types_combobox.current(0)
        self.object_types_combobox.pack()

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

        self.fill_var = tk.BooleanVar()
        self.f1 = tk.Checkbutton(self.master, text="Fill wireframe", variable=self.fill_var)
        self.f1.pack()

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
        self.r1 = tk.Radiobutton(self.master, text="Translation", value="translation",
                                 variable=self.entry_transformation)
        self.r2 = tk.Radiobutton(self.master, text="Scaling", value="scaling", variable=self.entry_transformation)
        self.r3 = tk.Radiobutton(self.master, text="Rotation around origin", value="rotation",
                                 variable=self.entry_transformation)
        self.r4 = tk.Radiobutton(self.master, text="Rotation around object's center", value="center_rotation",
                                 variable=self.entry_transformation)
        self.r5 = tk.Radiobutton(self.master, text="Rotation around arbitrary point", value="arbitrary_rotation",
                                 variable=self.entry_transformation)
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
        self.button_rotate_window = tk.Button(self.master, text="Rotate Window", command=self.rotate_vup)
        self.button_rotate_window.pack()

    def setup_export_object_interface(self):
        self.label_export_obj = tk.Label(self.master, text="Export Obj:")
        self.label_export_obj.pack()

        self.entry_export_obj_name = tk.Entry(self.master)
        self.entry_export_obj_name.pack()

        self.button_export_object = tk.Button(self.master, text="Export Obj", command=self.export_object)
        self.button_export_object.pack()

    def setup_import_object_interface(self):
        self.label_import_obj = tk.Label(self.master, text="Import Obj:")
        self.label_import_obj.pack()

        self.entry_import_obj_name = tk.Entry(self.master)
        self.entry_import_obj_name.pack()

        self.button_import_object = tk.Button(self.master, text="Import Obj", command=self.import_object)
        self.button_import_object.pack()

    def setup_clipping_interface(self):
        # Adicionar radio buttons para selecionar a técnica de clipagem
        self.label_clipping_method = tk.Label(self.master, text="Clipping Method")
        self.label_clipping_method.pack()

        self.var_clipping_method = tk.StringVar()
        self.var_clipping_method.set('parametric')

        self.radio_parametric = tk.Radiobutton(self.master, text="Parametric Clipping",
                                               variable=self.var_clipping_method, value='parametric',
                                               command=self.change_clipping_method)
        self.radio_parametric.pack()

        self.radio_cohen_sutherland = tk.Radiobutton(self.master, text="Cohen-Sutherland Clipping",
                                                     variable=self.var_clipping_method, value='cohen_sutherland',
                                                     command=self.change_clipping_method)
        self.radio_cohen_sutherland.pack()

    def change_clipping_method(self):
        self.clipping_method = self.var_clipping_method.get()

    def clip_point(self, x, y):
        # Verificar se o ponto está dentro da viewport
        return self.viewport.xmin <= x <= self.viewport.xmax and self.viewport.ymin <= y <= self.viewport.ymax

    def clip_line(self, x1, y1, x2, y2):
        if self.clipping_method == 'parametric':
            return self.clip_parametric(x1, y1, x2, y2)
        elif self.clipping_method == 'cohen_sutherland':
            return self.clip_cohen_sutherland(x1, y1, x2, y2)

    def clip_parametric(self, x1, y1, x2, y2):
        # Implementação do algoritmo de clipagem usando a equação paramétrica da reta
        # Checagem por meio da equação paramétrica envolvendo os limites da janela e a própria linha
        # Retorna as coordenadas clipadas (x1_clip, y1_clip, x2_clip, y2_clip)
        xmin, ymin, xmax, ymax = self.window.coordinates()
        t1 = 0
        t2 = 1

        dx = x2 - x1
        dy = y2 - y1

        # Parâmetros da equação paramétrica da reta
        p = [-dx, dx, -dy, dy]
        q = [x1 - xmin, xmax - x1, y1 - ymin, ymax - y1]

        for i in range(4):
            if p[i] == 0:
                if q[i] < 0:
                    return None  # Linha está fora da janela
            else:
                r = q[i] / p[i]
                if p[i] < 0:
                    t1 = max(t1, r)
                else:
                    t2 = min(t2, r)

        if t1 > t2:
            return None  # Linha está fora da janela

        x1_clip = x1 + t1 * dx
        y1_clip = y1 + t1 * dy
        x2_clip = x1 + t2 * dx
        y2_clip = y1 + t2 * dy

        return x1_clip, y1_clip, x2_clip, y2_clip

    def clip_cohen_sutherland(self, x1, y1, x2, y2):
        # Implementação do algoritmo de recorte de Cohen-Sutherland
        # Retorna as coordenadas clipadas (x1_clip, y1_clip, x2_clip, y2_clip)
        xmin, ymin, xmax, ymax = self.window.coordinates()
        # Códigos de região para os pontos inicial e final da linha
        code1 = self.calculate_region_code(x1, y1)
        code2 = self.calculate_region_code(x2, y2)

        while True:
            if not (code1 | code2):  # Ambos pontos estão dentro da janela
                return x1, y1, x2, y2

            if code1 & code2:  # Ambos pontos estão fora da janela
                return None

            # Escolher um dos pontos fora da janela
            code_outside = code1 if code1 else code2

            # Encontrar o ponto de interseção
            if code_outside & 8:  # Topo da janela
                x = x1 + (x2 - x1) * (ymax - y1) / (y2 - y1)
                y = ymax
            elif code_outside & 4:  # Fundo da janela
                x = x1 + (x2 - x1) * (ymin - y1) / (y2 - y1)
                y = ymin
            elif code_outside & 2:  # Direita da janela
                y = y1 + (y2 - y1) * (xmax - x1) / (x2 - x1)
                x = xmax
            elif code_outside & 1:  # Esquerda da janela
                y = y1 + (y2 - y1) * (xmin - x1) / (x2 - x1)
                x = xmin

            # Substituir o ponto fora da janela pelo ponto de interseção
            if code_outside == code1:
                x1, y1 = x, y
                code1 = self.calculate_region_code(x1, y1)
            else:
                x2, y2 = x, y
                code2 = self.calculate_region_code(x2, y2)

    def calculate_region_code(self, x, y):
        code = 0
        xmin, ymin, xmax, ymax = self.window.coordinates()

        if x < xmin:  # Esquerda da janela
            code |= 1
        elif x > xmax:  # Direita da janela
            code |= 2
        if y < ymin:  # Topo da janela
            code |= 4
        elif y > ymax:  # Fundo da janela
            code |= 8

        return code

    def clip_polygon(self, polygon):
        output_list = polygon.point_list_scn.copy()
        edge_points = [
            (self.window.xmin, self.window.ymin),
            (self.window.xmax, self.window.ymin),
            (self.window.xmax, self.window.ymax),
            (self.window.xmin, self.window.ymax)
        ]
        edges = [(edge_points[i], edge_points[(i + 1) % 4]) for i in range(len(edge_points))]

        # Clip against each window edge
        for edge in edges:
            input_list = output_list
            output_list = []
            p1 = input_list[-1]

            for p2 in input_list:
                if self.inside(p2, edge):
                    if not self.inside(p1, edge):
                        intersect = self.intersect(p1, p2, edge)
                        if intersect:
                            output_list.append(intersect)
                    output_list.append(p2)
                elif self.inside(p1, edge):
                    intersect = self.intersect(p1, p2, edge)
                    if intersect:
                        output_list.append(intersect)
                p1 = p2

        return output_list

    def inside(self, point, edge):
        # Test if a point is inside a window edge
        x, y = point
        x1, y1 = edge[0]
        x2, y2 = edge[1]

        return (x2 - x1) * (y - y1) > (y2 - y1) * (x - x1)

    def intersect(self, p1, p2, edge):
        # Find the intersection point of a line segment and a window edge
        x1, y1 = p1
        x2, y2 = p2
        x3, y3 = edge[0]
        x4, y4 = edge[1]

        denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if denom == 0:
            return None  # Parallel lines
        else:
            t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
            if 0 <= t <= 1:
                # Intersection point lies within the line segment
                x = x1 + t * (x2 - x1)
                y = y1 + t * (y2 - y1)
                return x, y
            else:
                return None  # Intersection point lies outside the line segment

    def import_object(self):
        file_path = self.entry_import_obj_name.get()
        try:
            with open(file_path, 'r') as f:
                vertices = []
                lines = f.readlines()
                for line in lines:
                    if line.startswith('v'):
                        _, x, y, _ = line.split()
                        vertices.append((float(x), float(y)))

                type_index = self.get_index_with_substring(lines, '# Type:')
                if type_index != -1:
                    type = lines[type_index].split(":")[1].strip()
                else:
                    raise ValueError

                # Check for color information
                color_index = self.get_index_with_substring(lines, '# Color:')
                if color_index != -1:
                    color = lines[color_index].split(":")[1].strip()
                    if color in ['red', 'green', 'blue', 'black']:
                        print(f"Cor do objeto: {color}")
                    else:
                        print("Nenhuma informação de cor encontrada.")
                        color = 'black'
                else:
                    print("Nenhuma informação de cor encontrada.")
                    color = 'black'

                filled_index = self.get_index_with_substring(lines, '# Filled:')
                if filled_index != -1:
                    filled = eval(lines[filled_index].split(":")[1].strip())
                else:
                    filled = False

                if type.upper() == 'POINT':
                    self.display_file.add_point(vertices[0], color)
                elif type.upper() == 'LINE':
                    self.display_file.add_line(vertices, color)
                elif type.upper() == 'WIREFRAME':
                    self.display_file.add_wireframe(vertices, color, filled)
                elif type.upper() == 'CURVE':
                    self.display_file.add_curve(vertices, color)
                self.draw_display_file()
                print(f"Objeto importado de '{file_path}'.")
        except FileNotFoundError:
            print(f"Arquivo '{file_path}' não encontrado.")
        except ValueError:
            print(f"Arquivo '{file_path}' não possui tipo.")

    def get_index_with_substring(self, lista, substring):
        for i, s in enumerate(lista):
            if substring in s:
                return i
        return -1

    def export_object(self):
        obj_name = self.entry_export_obj_name.get()
        if obj_name in self.display_file.objects:
            obj = self.display_file.objects[obj_name]

            file_path = f"{obj_name}.obj"
            OBJDescriptor.write_obj_file(file_path, obj)
            print(f"Objeto '{obj_name}' exportado para '{file_path}'.")
        else:
            print(f"O objeto '{obj_name}' não existe na lista de objetos.")

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
            new_coordinates_scn = np.dot(transformation_matrix,
                                         np.array([obj.coordinate_x_scn, obj.coordinate_y_scn, 1]))
            obj.coordinate_x_scn = new_coordinates_scn[0]
            obj.coordinate_y_scn = new_coordinates_scn[1]
        elif obj.type == 'Line':
            obj.start_point = np.dot(transformation_matrix, np.array([obj.start_point[0], obj.start_point[1], 1]))
            obj.end_point = np.dot(transformation_matrix, np.array([obj.end_point[0], obj.end_point[1], 1]))
            obj.start_point_scn = np.dot(transformation_matrix,
                                         np.array([obj.start_point_scn[0], obj.start_point_scn[1], 1]))
            obj.end_point_scn = np.dot(transformation_matrix, np.array([obj.end_point_scn[0], obj.end_point_scn[1], 1]))
        elif obj.type == 'Wireframe' or obj.type == 'Curve':
            for i in range(len(obj.point_list_scn)):
                point = obj.point_list[i]
                point_vector = np.dot(transformation_matrix, np.array([point[0], point[1], 1]))
                obj.point_list[i] = (point_vector[0], point_vector[1])
                point_scn = obj.point_list_scn[i]
                point_vector_scn = np.dot(transformation_matrix, np.array([point_scn[0], point_scn[1], 1]))
                obj.point_list_scn[i] = (point_vector_scn[0], point_vector_scn[1])

    def draw_object(self, obj):
        if obj.type == 'Point':
            obj.coordinate_x_scn, obj.coordinate_y_scn = self.rotate_align_vup(obj.coordinate_x_scn,
                                                                               obj.coordinate_y_scn)
            x, y = self.transform_to_viewport(obj.coordinate_x_scn, obj.coordinate_y_scn)
            if self.clip_point(x, y):
                self.canvas.create_oval(x, y, x + 2, y + 2, fill=obj.color)
        elif obj.type == 'Line':
            obj.start_point_scn[0], obj.start_point_scn[1] = self.rotate_align_vup(obj.start_point_scn[0],
                                                                                   obj.start_point_scn[1])
            obj.end_point_scn[0], obj.end_point_scn[1] = self.rotate_align_vup(obj.end_point_scn[0],
                                                                               obj.end_point_scn[1])
            x1_clip, y1_clip, x2_clip, y2_clip = self.clip_line(obj.start_point_scn[0], obj.start_point_scn[1],
                                                                obj.end_point_scn[0], obj.end_point_scn[1])
            x1, y1 = self.transform_to_viewport(x1_clip, y1_clip)
            x2, y2 = self.transform_to_viewport(x2_clip, y2_clip)
            self.canvas.create_line(x1, y1, x2, y2, fill=obj.color)
        elif obj.type == 'Wireframe':
            transformed_coords = []
            for i in range(len(obj.point_list_scn)):
                obj.point_list_scn[i] = self.rotate_align_vup(obj.point_list_scn[i][0], obj.point_list_scn[i][1])
            polygon = self.clip_polygon(obj)
            for i in range(len(polygon)):
                point = polygon[i]
                x, y = self.transform_to_viewport(point[0], point[1])
                transformed_coords.append((x, y))
            self.draw_wireframe(transformed_coords, obj.color, obj.filled)
        elif obj.type == 'Curve':
            transformed_coords = []
            for i in range(len(obj.point_list_scn)):
                obj.point_list_scn[i] = self.rotate_align_vup(obj.point_list_scn[i][0], obj.point_list_scn[i][1])
                # TODO: implementar método de clipping para curva
            for i in range(len(obj.point_list_scn)):
                x, y = obj.point_list_scn[i]
                # x, y = self.transform_to_viewport(point[0], point[1])
                transformed_coords.append((x, y))
            self.draw_hermite_curve(transformed_coords, obj.color)

    def draw_wireframe(self, coordinates, color, filled):
        # Desenhar as linhas do polígono
        for i in range(len(coordinates)):
            x1, y1 = coordinates[i]
            x2, y2 = coordinates[(i + 1) % len(coordinates)]
            self.canvas.create_line(x1, y1, x2, y2, fill=color)

        # Preencher o interior do polígono manualmente
        if filled:
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
                    self.canvas.create_line(intersections[i], scanline_y, intersections[i + 1], scanline_y,
                                            fill='black')
                scanline_y += 1

    def draw_hermite_curve(self, control_points, color):
        num_segments = 100  # Número de segmentos para desenhar a curva
        t_values = np.linspace(0, 1, num_segments)

        for i in range(1, len(control_points) - 3, 3):
            p0, m0, m1, p1 = control_points[i:i+4]  # Extrair os pontos de controle e vetores de tangente

            for t in t_values:
                t2 = t * t
                t3 = t2 * t
                h1 = 2 * t3 - 3 * t2 + 1
                h2 = -2 * t3 + 3 * t2
                h3 = t3 - 2 * t2 + t
                h4 = t3 - t2

                x = h1 * p0[0] + h2 * p1[0] + h3 * m0[0] + h4 * m1[0]
                y = h1 * p0[1] + h2 * p1[1] + h3 * m0[1] + h4 * m1[1]

                x, y = self.transform_to_viewport(x, y)  # Transformar as coordenadas para a viewport
                if self.clip_point(x, y):  # Verificar se o ponto está dentro da viewport
                    self.canvas.create_oval(x, y, x + 2, y + 2, fill=color)  # Desenhar o ponto na viewport

    def rotate_vup(self):
        angle = float(self.entry_rotation.get())
        self.angle_vup = angle
        self.draw_display_file()

    def draw_display_file(self):
        self.canvas.delete('all')

        # Redesenha as bordas
        self.viewport_border = self.canvas.create_rectangle(self.viewport.coordinates(), outline='red', dash=(5, 5))
        self.window_border = self.canvas.create_rectangle(self.window.coordinates(), outline='blue')

        for obj in self.display_file.objects.values():
            self.draw_object(obj)

        # Atualizar a lista de objetos
        object_names = "\n".join(self.display_file.objects.keys())
        self.object_list_label.config(text=object_names)
        self.angle_vup = 0

    def pan(self, dx, dy):
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
        object_color = self.color_string.get()
        filled = self.fill_var.get()
        coordinates = coordinates_str.split(",")
        # coordinates_head = coordinates.pop(0)
        coordinates_head = self.object_type.get()
        coordinates = list(map(lambda x: int(x), coordinates))
        coordinates = [(coordinates[i], coordinates[i + 1]) for i in range(0, len(coordinates), 2)]

        if coordinates_head.upper() == "POINT":
            self.display_file.add_point(coordinates[0], object_color)
        elif coordinates_head.upper() == "LINE":
            self.display_file.add_line(coordinates, object_color)
        elif coordinates_head.upper() == "WIREFRAME":
            self.display_file.add_wireframe(coordinates, object_color, filled)
        elif coordinates_head.upper() == "CURVE":
            self.display_file.add_curve(coordinates, object_color)
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
        elif obj.type == "Wireframe" or obj.type == "Curve":
            center_x = sum([p[0] for p in obj.point_list]) / len(obj.point_list)
            center_y = sum([p[1] for p in obj.point_list]) / len(obj.point_list)
            return center_x, center_y
