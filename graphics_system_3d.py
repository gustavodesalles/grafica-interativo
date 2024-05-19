import tkinter as tk
from tkinter import ttk

import numpy as np

from obj_descriptor import OBJDescriptor
from transformation_3d import Transformation3D
from viewport import Viewport
from window import Window


class GraphicsSystem3D:
    def __init__(self, master, display_file, object_list):
        self.master = master
        self.display_file = display_file
        self.object_list = object_list

        self.master.title("3D Graphics System")  # Definindo o título da janela

        # Adicionando um estilo ao tema
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Definindo as cores
        self.bg_color = 'white'
        self.frame_color = 'lightgray'
        self.button_color = 'lightblue'
        self.label_color = 'black'

        self.canvas = tk.Canvas(master, width=800, height=500, bg=self.bg_color)
        self.canvas.pack(side=tk.LEFT)

        # Coordenadas do canvas
        canvas_width = self.canvas.winfo_reqwidth()
        canvas_height = self.canvas.winfo_reqheight()
        canvas_depth = self.canvas.winfo_depth()

        viewport_margin = 20

        self.window = Window(0, 0, canvas_width, canvas_height)
        self.viewport = Viewport(
            canvas_width // 4 + viewport_margin,
            canvas_height // 4 + viewport_margin,
            3 * canvas_width // 4 - viewport_margin,
            3 * canvas_height // 4 - viewport_margin,
        )

        self.viewport_frame = self.canvas.create_rectangle(self.viewport.xmin, self.viewport.ymin, self.viewport.xmax, self.viewport.ymax, outline='green')

        self.clipping_method = 'parametric'
        # self.projection_type = 'orthographic'
        self.projection_type = 'perspective'

        self.angle_vup = 0

        self.setup_object_list_interface()
        self.setup_basic_button()
        self.setup_transform_object_button()
        # self.setup_rotation_object_button() - do we need this? 3D projection doesnt depend on Vup
        self.setup_add_remove_object_button()
        self.setup_projection_options()
        self.setup_export_object_button()
        self.setup_import_object_button()

    def setup_object_list_interface(self):
        self.object_list_frame = tk.Frame(self.master, bg=self.frame_color)
        self.object_list_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=10, pady=10)
        self.object_list_title = tk.Label(self.object_list_frame, text="Object List", bg=self.frame_color, fg=self.label_color)
        self.object_list_title.pack()
        self.object_list_label = tk.Label(self.object_list_frame, text="", bg=self.frame_color, fg=self.label_color)
        self.object_list_label.pack()

    def setup_basic_button(self):
        basic_button = tk.Button(self.master, text="Basic", command=self.setup_basic_interface)
        basic_button.pack(side=tk.TOP, padx=10, pady=10)

    def setup_add_remove_object_button(self):
        add_remove_button = tk.Button(self.master, text="Add/Remove Object", command=self.setup_add_remove_object_interface)
        add_remove_button.pack(side=tk.TOP, padx=10, pady=10)

    def setup_transform_object_button(self):
        transform_button = tk.Button(self.master, text="Transform Object", command=self.setup_transformation_interface)
        transform_button.pack(side=tk.TOP, padx=10, pady=10)

    def setup_projection_options(self):
        self.label_clipping_method = tk.Label(self.master, text="Projection", bg=self.frame_color,
                                              fg=self.label_color)
        self.label_clipping_method.pack()

        self.var_projection_type = tk.StringVar()
        self.var_projection_type.set(self.projection_type)

        self.radio_orthographic = tk.Radiobutton(self.master, text="Orthographic",
                                               variable=self.var_projection_type, value='orthographic',
                                               command=self.change_projection_type, bg=self.frame_color)
        self.radio_orthographic.pack()

        self.radio_perspective = tk.Radiobutton(self.master, text="Perspective",
                                                     variable=self.var_projection_type, value='perspective',
                                                     command=self.change_projection_type, bg=self.frame_color)
        self.radio_perspective.pack()

    def setup_rotation_object_button(self):
        rotate_button = tk.Button(self.master, text="Rotate Object", command=self.setup_rotation_interface)
        rotate_button.pack(side=tk.TOP, padx=10, pady=10)

    def setup_export_object_button(self):
        export_button = tk.Button(self.master, text="Export Object", command=self.setup_export_object_interface)
        export_button.pack(side=tk.TOP, padx=10, pady=10)

    def setup_import_object_button(self):
        import_button = tk.Button(self.master, text="Import Object", command=self.setup_import_object_interface)
        import_button.pack(side=tk.TOP, padx=10, pady=10)

    def setup_basic_interface(self):
        basic_window = tk.Toplevel(self.master)
        basic_window.title("Basic Functionalities")

        basic_frame = tk.Frame(basic_window, bg=self.frame_color)
        basic_frame.pack(padx=10, pady=10)

        button_pan_up = tk.Button(basic_frame, text="Pan Up", command=self.pan_up)
        button_pan_up.grid(row=0, column=0, pady=5)

        button_pan_left = tk.Button(basic_frame, text="Pan Left", command=self.pan_left)
        button_pan_left.grid(row=1, column=0)

        button_pan_right = tk.Button(basic_frame, text="Pan Right", command=self.pan_right)
        button_pan_right.grid(row=1, column=2)

        button_pan_down = tk.Button(basic_frame, text="Pan Down", command=self.pan_down)
        button_pan_down.grid(row=2, column=0, pady=5)

        button_zoom_in = tk.Button(basic_frame, text="Zoom In", command=self.zoom_in)
        button_zoom_in.grid(row=0, column=1, padx=5)

        button_zoom_out = tk.Button(basic_frame, text="Zoom Out", command=self.zoom_out)
        button_zoom_out.grid(row=0, column=2, padx=5)

    def setup_add_remove_object_interface(self):
        add_remove_window = tk.Toplevel(self.master)
        add_remove_window.title("Add/Remove Object")

        add_remove_frame = tk.Frame(add_remove_window, bg=self.frame_color)
        add_remove_frame.pack(padx=10, pady=10)

        # Add Object Interface
        label_add_object = tk.Label(add_remove_frame, text="Add Object:", bg=self.frame_color, fg=self.label_color)
        label_add_object.grid(row=0, column=0, padx=5, pady=5)

        # Set up the interface for adding objects
        self.setup_add_object_interface(add_remove_frame, row=0, column=1)

        # Remove Object Interface
        label_remove_object = tk.Label(add_remove_frame, text="Remove Object:", bg=self.frame_color, fg=self.label_color)
        label_remove_object.grid(row=1, column=0, padx=5, pady=5)

        # Set up the interface for removing objects
        self.setup_remove_object_interface(add_remove_frame, row=1, column=1)

    def setup_add_object_interface(self, parent_frame, row, column):
        add_object_frame = tk.Frame(parent_frame, bg=self.frame_color)
        add_object_frame.grid(row=row, column=column, padx=5, pady=5)

        self.object_type = tk.StringVar()
        self.object_types_combobox = ttk.Combobox(add_object_frame, state="readonly", textvariable=self.object_type,
                                                values=['Point', 'Polygon', 'Bicubic Bezier Surface'])
        self.object_types_combobox.current(0)
        self.object_types_combobox.pack(pady=10)

        self.label_coordinates = tk.Label(add_object_frame, text="Coordinates:")
        self.label_coordinates.pack(side=tk.TOP)

        self.entry_coordinates = tk.Entry(add_object_frame)
        self.entry_coordinates.pack()

        self.label_control_points = tk.Label(add_object_frame, text="Control Points (for Bicubic Bezier Surface):")
        self.label_control_points.pack(side=tk.TOP)
        self.entry_control_points = tk.Entry(add_object_frame)
        self.entry_control_points.pack()

        self.color_string = tk.StringVar()
        self.c1 = tk.Radiobutton(add_object_frame, text="Red", value="red", variable=self.color_string)
        self.c2 = tk.Radiobutton(add_object_frame, text="Green", value="green", variable=self.color_string)
        self.c3 = tk.Radiobutton(add_object_frame, text="Blue", value="blue", variable=self.color_string)
        self.c1.pack()
        self.c2.pack()
        self.c3.pack()

        self.fill_var = tk.BooleanVar()
        self.f1 = tk.Checkbutton(add_object_frame, text="Fill wireframe", variable=self.fill_var)
        self.f1.pack()

        self.button_add_object = tk.Button(add_object_frame, text="Add Object", command=self.add_object, bg=self.button_color)
        self.button_add_object.pack(side=tk.TOP)



    def setup_remove_object_interface(self, parent_frame, row, column):
        remove_object_frame = tk.Frame(parent_frame, bg=self.frame_color)
        remove_object_frame.grid(row=row, column=column, padx=5, pady=5)

        # Add your interface elements for removing objects here
        # Example: entry for object name, button to remove object, etc.
        self.object_name_label = tk.Label(remove_object_frame, text="Object Name:", bg=self.frame_color, fg=self.label_color)
        self.object_name_label.pack()
        self.entry_object_name = tk.Entry(remove_object_frame)
        self.entry_object_name.pack()
        self.button_remove_object = tk.Button(remove_object_frame, text="Remove Object", command=self.remove_object, bg=self.button_color)
        self.button_remove_object.pack()

    def setup_transformation_interface(self):
        transform_window = tk.Toplevel(self.master)
        transform_window.title("Transform Object")

        transform_frame = tk.Frame(transform_window, bg=self.frame_color)
        transform_frame.pack(padx=10, pady=10)

        # Transformation Interface
        label_transformation = tk.Label(transform_frame, text="Transformation", bg=self.frame_color, fg=self.label_color)
        label_transformation.grid(row=0, column=0, padx=5, pady=5)

        self.entry_transformation = tk.StringVar()
        self.r1 = tk.Radiobutton(transform_frame, text="Translation", value="translation",
                                variable=self.entry_transformation, bg=self.frame_color)
        self.r2 = tk.Radiobutton(transform_frame, text="Scaling", value="scaling", variable=self.entry_transformation, bg=self.frame_color)
        self.r3 = tk.Radiobutton(transform_frame, text="Rotation around origin (X)", value="rotation_x",
                                variable=self.entry_transformation, bg=self.frame_color)
        self.r4 = tk.Radiobutton(transform_frame, text="Rotation around origin (Y)", value="rotation_y",
                                variable=self.entry_transformation, bg=self.frame_color)
        self.r5 = tk.Radiobutton(transform_frame, text="Rotation around origin (Z)", value="rotation_z",
                                variable=self.entry_transformation, bg=self.frame_color)
        self.r6 = tk.Radiobutton(transform_frame, text="Rotation around object's center (X)", value="center_rotation_x",
                                variable=self.entry_transformation, bg=self.frame_color)
        self.r7 = tk.Radiobutton(transform_frame, text="Rotation around object's center (Y)", value="center_rotation_y",
                                variable=self.entry_transformation, bg=self.frame_color)
        self.r8 = tk.Radiobutton(transform_frame, text="Rotation around object's center (Z)", value="center_rotation_z",
                                variable=self.entry_transformation, bg=self.frame_color)
        self.r9 = tk.Radiobutton(transform_frame, text="Arbitrary rotation (X)", value="arbitrary_rotation_x",
                                variable=self.entry_transformation, bg=self.frame_color)
        self.r10 = tk.Radiobutton(transform_frame, text="Arbitrary rotation (Y)", value="arbitrary_rotation_y",
                                variable=self.entry_transformation, bg=self.frame_color)
        self.r11 = tk.Radiobutton(transform_frame, text="Arbitrary rotation (Z)", value="arbitrary_rotation_z",
                                variable=self.entry_transformation, bg=self.frame_color)
        self.r1.grid(row=1, column=0, sticky="w")
        self.r2.grid(row=2, column=0, sticky="w")
        self.r3.grid(row=3, column=0, sticky="w")
        self.r4.grid(row=4, column=0, sticky="w")
        self.r5.grid(row=5, column=0, sticky="w")
        self.r6.grid(row=6, column=0, sticky="w")
        self.r7.grid(row=7, column=0, sticky="w")
        self.r8.grid(row=8, column=0, sticky="w")
        self.r9.grid(row=9, column=0, sticky="w")
        self.r10.grid(row=10, column=0, sticky="w")
        self.r11.grid(row=11, column=0, sticky="w")

        self.label_object_name = tk.Label(transform_frame, text="Object Name:", bg=self.frame_color, fg=self.label_color)
        self.label_object_name.grid(row=12, column=0, padx=5, pady=5, sticky="w")

        self.entry_object_name_transform = tk.Entry(transform_frame)
        self.entry_object_name_transform.grid(row=12, column=1, padx=5, pady=5, sticky="w")

        self.label_params = tk.Label(transform_frame, text="Params (comma separated)", bg=self.frame_color, fg=self.label_color)
        self.label_params.grid(row=13, column=0, padx=5, pady=5, sticky="w")

        self.entry_params = tk.Entry(transform_frame)
        self.entry_params.grid(row=13, column=1, padx=5, pady=5, sticky="w")

        self.button_transform = tk.Button(transform_frame, text="Transform Object", command=self.transform_object, bg=self.button_color)
        self.button_transform.grid(row=14, column=0, columnspan=2, padx=5, pady=5)


    def setup_rotation_interface(self):
        basic_window = tk.Toplevel(self.master)
        basic_window.title("Rotation")

        basic_frame = tk.Frame(basic_window, bg=self.frame_color)
        basic_frame.pack(padx=10, pady=10)

        self.label_rotation = tk.Label(basic_frame, text="Rotation Angle (Vup):", bg=self.frame_color, fg=self.label_color)
        self.label_rotation.pack()
        self.entry_rotation = tk.Entry(basic_frame)
        self.entry_rotation.pack()
        self.button_rotate_window = tk.Button(basic_frame, text="Rotate Window", command=self.rotate_vup, bg=self.button_color)
        self.button_rotate_window.pack()

    def setup_export_object_interface(self):
        basic_window = tk.Toplevel(self.master)
        basic_window.title("Export")

        basic_frame = tk.Frame(basic_window, bg=self.frame_color)
        basic_frame.pack(padx=10, pady=10)

        self.label_export_obj = tk.Label(basic_frame, text="Export Obj:", bg=self.frame_color, fg=self.label_color)
        self.label_export_obj.pack(side=tk.LEFT, padx=10, pady=10)

        self.entry_export_obj_name = tk.Entry(basic_frame)
        self.entry_export_obj_name.pack(side=tk.LEFT, padx=10, pady=10)

        self.button_export_object = tk.Button(basic_frame, text="Export Obj", command=self.export_object, bg=self.button_color)
        self.button_export_object.pack(side=tk.LEFT, padx=10, pady=10)

    def setup_import_object_interface(self):
        basic_window = tk.Toplevel(self.master)
        basic_window.title("Import")

        basic_frame = tk.Frame(basic_window, bg=self.frame_color)
        basic_frame.pack(padx=10, pady=10)

        self.label_import_obj = tk.Label(basic_frame, text="Import Obj:", bg=self.frame_color, fg=self.label_color)
        self.label_import_obj.pack(side=tk.TOP, padx=10, pady=5)

        self.entry_import_obj_name = tk.Entry(basic_frame)
        self.entry_import_obj_name.pack(side=tk.TOP, padx=10, pady=5)

        self.button_import_object = tk.Button(basic_frame, text="Import Obj", command=self.import_object, bg=self.button_color)
        self.button_import_object.pack(side=tk.TOP, padx=10, pady=5)

    def setup_clipping_interface(self):
        basic_window = tk.Toplevel(self.master)
        basic_window.title("Import")

        basic_frame = tk.Frame(basic_window, bg=self.frame_color)
        basic_frame.pack(padx=10, pady=10)

        self.label_clipping_method = tk.Label(basic_frame, text="Clipping Method", bg=self.frame_color, fg=self.label_color)
        self.label_clipping_method.pack()

        self.var_clipping_method = tk.StringVar()
        self.var_clipping_method.set('parametric')

        self.radio_parametric = tk.Radiobutton(basic_frame, text="Parametric Clipping",
                                               variable=self.var_clipping_method, value='parametric',
                                               command=self.change_clipping_method, bg=self.frame_color)
        self.radio_parametric.pack()

        self.radio_cohen_sutherland = tk.Radiobutton(basic_frame, text="Cohen-Sutherland Clipping",
                                                     variable=self.var_clipping_method, value='cohen_sutherland',
                                                     command=self.change_clipping_method, bg=self.frame_color)
        self.radio_cohen_sutherland.pack()

##################################################################################
##############################end of interface setup##############################
##################################################################################

    def rotate_align_vup(self, x, y, z):
        theta = np.radians(self.angle_vup)
        cos_theta = np.cos(theta)
        sin_theta = np.sin(theta)

        x_rotated = x * cos_theta - y * sin_theta
        y_rotated = x * sin_theta + y * cos_theta
        return x_rotated, y_rotated, z

    def transform_to_viewport(self, x_rotated, y_rotated):
        xmin, ymin, xmax, ymax = self.window.coordinates()
        xvmin, yvmin, xvmax, yvmax = self.viewport.coordinates()

        xv = ((x_rotated - xmin) / (xmax - xmin)) * (xvmax - xvmin) + xvmin
        yv = ((y_rotated - ymin) / (ymax - ymin)) * (yvmax - yvmin) + yvmin
        # zv = ((z - zmin) / (zmax - zmin)) * (zvmax - zvmin) + zvmin

        return xv, yv

    def change_clipping_method(self):
        self.clipping_method = self.var_clipping_method.get()

    def change_projection_type(self):
        self.projection_type = self.var_projection_type.get()
        self.draw_display_file()

    def clip_point(self, x, y):
        # Verificar se o ponto está dentro da window
        return self.window.xmin <= x <= self.window.xmax and self.window.ymin <= y <= self.window.ymax

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
                    return None, None, None, None  # Linha está fora da janela
            else:
                r = q[i] / p[i]
                if p[i] < 0:
                    t1 = max(t1, r)
                else:
                    t2 = min(t2, r)

        if t1 > t2:
            return None, None, None, None  # Linha está fora da janela

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
                return None, None, None, None

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
        output_list = polygon.copy()
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
            if len(input_list) == 0:
                return output_list
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
                segments = []
                lines = f.readlines()
                for line in lines:
                    if line.startswith('v'):
                        _, x, y, z = line.split()
                        vertices.append((float(x), float(y), float(z)))
                    elif line.startswith('l'):
                        segment = line.split()[1:]  # Ignorando 'l'
                        segment = [int(idx) for idx in segment]
                        segments.append(segment)

                type_index = self.get_index_with_substring(lines, '# Type:')
                if type_index != -1:
                    type = lines[type_index].split(":")[1].strip()
                    if type not in ["Point", "Polygon"]:
                        print(f"Arquivo {file_path} possui tipo inválido.")
                        return
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
                # elif type.upper() == 'LINE':
                #     self.display_file.add_line(vertices, color)
                # elif type.upper() == 'WIREFRAME':
                #     self.display_file.add_wireframe(vertices, color, filled)
                elif type.upper() == 'POLYGON':
                    self.display_file.add_polygon(vertices, color, segments)
                # elif type.upper() == 'CURVE':
                #     self.display_file.add_curve(vertices, color)
                # elif type.upper() == 'B-SPLINE':
                #     self.display_file.add_b_spline(vertices, color)
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

            if obj.type == 'Polygon':
                file_path = f"{obj_name}.obj"
                with open(file_path, 'w') as f:
                    f.write("# Type: Polygon\n")
                    f.write(f"# Color: {obj.color}\n")
                    # Escreve os vértices
                    for coordinate in obj.coordinates:
                        f.write("v {} {} {}\n".format(coordinate.coordinate_x, coordinate.coordinate_y, coordinate.coordinate_z))

                    # Escreve as faces
                    for i in obj.segments:
                        # Escreve a linha de face no arquivo .obj
                        f.write("l {} {}\n".format(obj.coordinates.index(i[0]) + 1,
                                                         obj.coordinates.index(i[1]) + 1))

                print(f"Objeto '{obj_name}' exportado para '{file_path}'.")
            else:
                print("Apenas objetos do tipo Polygon3D podem ser exportados.")
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

        try:
            if transformation == 'translation':
                tx, ty, tz = map(float, transformation_params)
                transformation_matrix = Transformation3D.translation(tx, ty, tz)
            elif transformation == 'rotation_x':
                angle = float(transformation_params[0])
                transformation_matrix = Transformation3D.rotation_x(angle)
            elif transformation == 'rotation_y':
                angle = float(transformation_params[0])
                transformation_matrix = Transformation3D.rotation_y(angle)
            elif transformation == 'rotation_z':
                angle = float(transformation_params[0])
                transformation_matrix = Transformation3D.rotation_z(angle)
            elif transformation == 'center_rotation_x':
                angle = float(transformation_params[0])
                center = self.get_object_center(obj)
                transformation_matrix = Transformation3D.arbitrary_rotation_x(angle, center)
            elif transformation == 'center_rotation_y':
                angle = float(transformation_params[0])
                center = self.get_object_center(obj)
                transformation_matrix = Transformation3D.arbitrary_rotation_y(angle, center)
            elif transformation == 'center_rotation_z':
                angle = float(transformation_params[0])
                center = self.get_object_center(obj)
                transformation_matrix = Transformation3D.arbitrary_rotation_z(angle, center)
            elif transformation == 'scaling':
                sx, sy, sz = map(float, transformation_params)
                center = self.get_object_center(obj)
                transformation_matrix = Transformation3D.scale(sx, sy, sz, center)
            elif transformation == 'arbitrary_rotation_x':
                angle = float(transformation_params[0])
                center = tuple(map(float, transformation_params[1:]))
                transformation_matrix = Transformation3D.arbitrary_rotation_x(angle, center)
            elif transformation == 'arbitrary_rotation_y':
                angle = float(transformation_params[0])
                center = tuple(map(float, transformation_params[1:]))
                transformation_matrix = Transformation3D.arbitrary_rotation_y(angle, center)
            elif transformation == 'arbitrary_rotation_z':
                angle = float(transformation_params[0])
                center = tuple(map(float, transformation_params[1:]))
                transformation_matrix = Transformation3D.arbitrary_rotation_z(angle, center)
        except ValueError:
            print('Invalid value(s)')

        if transformation_matrix is not None:
            self.apply_transformation(obj, transformation_matrix)
            self.draw_display_file()
        else:
            print('No transformation')

    def apply_transformation(self, obj, transformation_matrix):
        if obj.type == 'Point':
            new_coordinates = np.dot(transformation_matrix, np.array([obj.coordinate_x, obj.coordinate_y, obj.coordinate_z, 1]))
            obj.coordinate_x = new_coordinates[0]
            obj.coordinate_y = new_coordinates[1]
            obj.coordinate_z = new_coordinates[2]
            new_coordinates_scn = np.dot(transformation_matrix,
                                         np.array([obj.coordinate_x_scn, obj.coordinate_y_scn, obj.coordinate_z_scn, 1]))
            obj.coordinate_x_scn = new_coordinates_scn[0]
            obj.coordinate_y_scn = new_coordinates_scn[1]
            obj.coordinate_z_scn = new_coordinates_scn[2]
        elif obj.type == 'Line':
            obj.start_point = np.dot(transformation_matrix, np.array([obj.start_point[0], obj.start_point[1], 1]))
            obj.end_point = np.dot(transformation_matrix, np.array([obj.end_point[0], obj.end_point[1], 1]))
            obj.start_point_scn = np.dot(transformation_matrix,
                                         np.array([obj.start_point_scn[0], obj.start_point_scn[1], 1]))
            obj.end_point_scn = np.dot(transformation_matrix, np.array([obj.end_point_scn[0], obj.end_point_scn[1], 1]))
        elif obj.type == 'Wireframe' or obj.type == 'Curve' or obj.type == 'B-Spline':
            for i in range(len(obj.point_list_scn)):
                point = obj.point_list[i]
                point_vector = np.dot(transformation_matrix, np.array([point[0], point[1], 1]))
                obj.point_list[i] = (point_vector[0], point_vector[1])
                point_scn = obj.point_list_scn[i]
                point_vector_scn = np.dot(transformation_matrix, np.array([point_scn[0], point_scn[1], 1]))
                obj.point_list_scn[i] = (point_vector_scn[0], point_vector_scn[1])
        elif obj.type == 'Polygon':
            for i in range(len(obj.coordinates)):
                vertex = obj.coordinates[i]
                vertex_vector = np.dot(transformation_matrix, np.array([vertex.coordinate_x, vertex.coordinate_y, vertex.coordinate_z, 1]))
                obj.coordinates[i].coordinate_x = vertex_vector[0]
                obj.coordinates[i].coordinate_y = vertex_vector[1]
                obj.coordinates[i].coordinate_z = vertex_vector[2]
                vertex_vector_scn = np.dot(transformation_matrix, np.array([vertex.coordinate_x_scn, vertex.coordinate_y_scn, vertex.coordinate_z_scn, 1]))
                obj.coordinates[i].coordinate_x_scn = vertex_vector_scn[0]
                obj.coordinates[i].coordinate_y_scn = vertex_vector_scn[1]
                obj.coordinates[i].coordinate_z_scn = vertex_vector_scn[2]
                # obj.coordinates[i] = (vertex_vector[0], vertex_vector[1], vertex[2])  # Include z-coordinate if 3D

    def draw_object(self, obj):
        if obj.type == 'Point':
            obj.coordinate_x_scn, obj.coordinate_y_scn, obj.coordinate_z_scn = self.rotate_align_vup(obj.coordinate_x_scn, obj.coordinate_y_scn, obj.coordinate_z_scn)
            x, y, z = self.transform_to_viewport(obj.coordinate_x_scn, obj.coordinate_y_scn, obj.coordinate_z_scn)
            self.canvas.create_oval(x, y, x + 2, y + 2, fill=obj.color)
        elif obj.type == 'Line':
            obj.start_point_scn[0], obj.start_point_scn[1], obj.start_point_scn[2] = self.rotate_align_vup(obj.start_point_scn[0], obj.start_point_scn[1], obj.start_point_scn[2])
            obj.end_point_scn[0], obj.end_point_scn[1], obj.end_point_scn[2] = self.rotate_align_vup(obj.end_point_scn[0], obj.end_point_scn[1], obj.end_point_scn[2])
            x1, y1, z1 = self.transform_to_viewport(obj.start_point_scn[0], obj.start_point_scn[1], obj.start_point_scn[2])
            x2, y2, z2 = self.transform_to_viewport(obj.end_point_scn[0], obj.end_point_scn[1], obj.end_point_scn[2])
            self.canvas.create_line(x1, y1, x2, y2, fill=obj.color)
        elif obj.type == 'Wireframe':
            transformed_coords = []
            for i in range(len(obj.point_list_scn)):
                obj.point_list_scn[i] = self.rotate_align_vup(obj.point_list_scn[i][0], obj.point_list_scn[i][1], obj.point_list_scn[i][2])
            for point in obj.point_list_scn:
                x, y, z = self.transform_to_viewport(point[0], point[1], point[2])
                transformed_coords.append((x, y, z))
            self.draw_wireframe(transformed_coords, obj.color, obj.filled)
        else:
            transformed_coords = []
            for i in range(len(obj.point_list_scn)):
                obj.point_list_scn[i] = self.rotate_align_vup(obj.point_list_scn[i][0], obj.point_list_scn[i][1], obj.point_list_scn[i][2])
            for point in obj.point_list_scn:
                x, y, z = self.transform_to_viewport(point[0], point[1], point[2])
                transformed_coords.append((x, y, z))
            if obj.type == 'Curve':
                self.draw_hermite_curve(transformed_coords, obj.color)
            elif obj.type == 'B-Spline' and len(transformed_coords) > 3:
                self.calculate_b_spline(transformed_coords, obj.color)

    def draw_object_3d(self, obj, vrp, vpn, cop):
        transformed_coords = None
        if self.projection_type == 'orthographic':
            transformed_coords = self.orthogonal_projection(obj, vrp, vpn)
        elif self.projection_type == 'perspective':
            transformed_coords = self.perspective_projection(obj, cop, vpn)

        if transformed_coords is not None:
            if obj.type == 'Point':
                self.canvas.create_oval(transformed_coords[0], transformed_coords[1], transformed_coords[0] + 2, transformed_coords[1] + 2, fill=obj.color)
            elif obj.type == 'Polygon':
                self.draw_polygon(transformed_coords, obj.color)
            elif obj.type == "Bezier Surface":
                self.draw_bezier_surface(transformed_coords, obj.color)

    def draw_polygon(self, coordinates, color):
        # Draw the polygon
        self.canvas.create_polygon(coordinates, outline=color, fill='')

    # def draw_bezier_surface(self, control_points, color):
    #     num_points = len(control_points)
    #     mb = np.array([[-1, 3, -3, 1],
    #                     [3, -6, 3, 0],
    #                     [-3, 3, 0, 0],
    #                     [1, 0, 0, 0]])

    #     for i in range(num_points - 15):
    #         for t in np.arange(0, 1, 0.01):
    #             #TODO: definir matrizes gx e gy e desenhar curvas da superfície
    #             g = np.array([control_points[x:x+4] for x in range(0, len(control_points), 4)]) # não tenho certeza

    def draw_bezier_surface(self, control_points, color):
        control_points = np.array(control_points).reshape(4, 4, 3)  # Garantir que está no formato correto
        u_values = np.linspace(0, 1, 20)
        v_values = np.linspace(0, 1, 20)
        surface_points = self.bezier_surface(control_points, u_values, v_values)

        for i in range(surface_points.shape[0] - 1):
            for j in range(surface_points.shape[1] - 1):
                # Desenhar linhas da superfície
                self.canvas.create_line(surface_points[i, j, 0], surface_points[i, j, 1],
                                        surface_points[i + 1, j, 0], surface_points[i + 1, j, 1], fill=color)
                self.canvas.create_line(surface_points[i, j, 0], surface_points[i, j, 1],
                                        surface_points[i, j + 1, 0], surface_points[i, j + 1, 1], fill=color)



    
    # Função de cálculo de ponto na superfície de Bézier
    def bezier_surface_point(self, u, v, gx, gy, gz, mb):
        u_vec = np.array([u**3, u**2, u, 1])
        v_vec = np.array([v**3, v**2, v, 1])
        
        x = u_vec @ mb @ gx @ mb.T @ v_vec.T
        y = u_vec @ mb @ gy @ mb.T @ v_vec.T
        z = u_vec @ mb @ gz @ mb.T @ v_vec.T
        
        return x, y, z

    def convert_3d_to_2d(self, x, y, z):
        # Aqui você deve implementar a lógica para converter coordenadas 3D para 2D,
        # baseada no tipo de projeção (perspectiva ou ortográfica) que você está usando.
        # Esta é uma implementação de exemplo para uma projeção perspectiva simples:
        d = 500  # Distância do plano de projeção (pode ajustar conforme necessário)
        screen_x = x * d / (d + z)
        screen_y = y * d / (d + z)
        return screen_x, screen_y

    def parse_control_points(self, control_points_str):
        rows = control_points_str.split(';')
        control_points = []
        for row in rows:
            points = row.split(',')
            parsed_points = []
            for point in points:
                x, y, z = map(float, point.strip('()').split(','))
                parsed_points.append((x, y, z))
            control_points.append(parsed_points)
        return control_points

    def draw_wireframe(self, coordinates, color, filled):
        # Desenhar as linhas do polígono
        # Desenhar as linhas entre os vértices do modelo
        for i in range(len(coordinates)):
            x1, y1, z1 = coordinates[i]
            x2, y2, z2 = coordinates[(i + 1) % len(coordinates)]

            # Desenhar linha entre os vértices nos planos x-y, x-z e y-z
            self.canvas.create_line(x1, y1, x2, y2, fill=color)  # Linha no plano x-y
            self.canvas.create_line(x1, z1, x2, z2, fill=color)  # Linha no plano x-z
            self.canvas.create_line(y1, z1, y2, z2, fill=color)  # Linha no plano y-z

        # Preencher o interior do polígono manualmente
        if filled:
            scanline_y = min(y for x, y, z in coordinates)
            while scanline_y <= max(y for x, y, z in coordinates):
                intersections = []
                for i in range(len(coordinates)):
                    x1, y1, z1 = coordinates[i]
                    x2, y2, z2 = coordinates[(i + 1) % len(coordinates)]
                    if y1 != y2 and (y1 <= scanline_y <= y2 or y2 <= scanline_y <= y1):
                        x_intersect = x1 + (scanline_y - y1) * (x2 - x1) / (y2 - y1)
                        z_intersect = z1 + (scanline_y - y1) * (z2 - z1) / (y2 - y1)
                        intersections.append((x_intersect, z_intersect))
                intersections.sort()
                for i in range(0, len(intersections), 2):
                    self.canvas.create_line(intersections[i][0], scanline_y, intersections[i][1], scanline_y, fill='black')
                scanline_y += 1

    def draw_hermite_curve(self, control_points, color):
        num_segments = 100  # Número de segmentos para desenhar a curva
        t_values = np.linspace(0, 1, num_segments)

        for i in range(0, len(control_points) - 3, 3):
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

                if i > 0:
                    x1_clip, y1_clip, x2_clip, y2_clip = self.clip_line(prev_x, prev_y, x, y)
                    if x1_clip is not None:
                        x1, y1 = self.transform_to_viewport(x1_clip, y1_clip)
                        x2, y2 = self.transform_to_viewport(x2_clip, y2_clip)
                        self.canvas.create_line(x1, y1, x2, y2, fill=color)

                prev_x, prev_y = x, y

    def calculate_b_spline(self, control_points, color):
        num_points = len(control_points)
        spline_points = []

        # Forward Differences algorithm for B-Splines
        for i in range(num_points - 3):
            for t in np.arange(0, 1, 0.01):
                x = ((-1 * t ** 3 + 3 * t ** 2 - 3 * t + 1) / 6) * control_points[i][0] + \
                    ((3 * t ** 3 - 6 * t ** 2 + 4) / 6) * control_points[i + 1][0] + \
                    ((-3 * t ** 3 + 3 * t ** 2 + 3 * t + 1) / 6) * control_points[i + 2][0] + \
                    (t ** 3 / 6) * control_points[i + 3][0]
                y = ((-1 * t ** 3 + 3 * t ** 2 - 3 * t + 1) / 6) * control_points[i][1] + \
                    ((3 * t ** 3 - 6 * t ** 2 + 4) / 6) * control_points[i + 1][1] + \
                    ((-3 * t ** 3 + 3 * t ** 2 + 3 * t + 1) / 6) * control_points[i + 2][1] + \
                    (t ** 3 / 6) * control_points[i + 3][1]
                spline_points.append((x, y))

                if i > 0:
                    x1_clip, y1_clip, x2_clip, y2_clip = self.clip_line(prev_x, prev_y, x, y)
                    if x1_clip is not None:
                        x1, y1 = self.transform_to_viewport(x1_clip, y1_clip)
                        x2, y2 = self.transform_to_viewport(x2_clip, y2_clip)
                        self.canvas.create_line(x1, y1, x2, y2, fill=color)

                prev_x, prev_y = x, y

        return spline_points

    def rotate_vup(self):
        angle = float(self.entry_rotation.get())
        self.angle_vup = angle
        self.draw_display_file()

    def draw_display_file(self):
        self.canvas.delete('all')

        # Redesenha as bordas
        self.viewport_border = self.canvas.create_rectangle(self.viewport.xmin, self.viewport.ymin, self.viewport.xmax, self.viewport.ymax, outline='red', dash=(5, 5))
        # self.window_border = self.canvas.create_rectangle(self.window.xmin, self.window.ymin, self.window.xmax, self.window.ymax, outline='blue')

        # for obj in self.display_file.objects.values():
        #     self.draw_object(obj)

        vrp = (0,0,0)
        vpn = (0,0,0)
        cop = (0,0,5)

        for obj in self.display_file.objects.values():
            self.draw_object_3d(obj, vrp, vpn, cop)

        # Atualizar a lista de objetos
        object_names = "\n".join(self.display_file.objects.keys())
        self.object_list_label.config(text=object_names)
        self.angle_vup = 0

    def orthogonal_projection(self, obj, vrp, vpn):
        # 1. Translade VRP para a origem
        translation_matrix = Transformation3D.translation(-vrp[0], -vrp[1], -vrp[2])

        # 2. Determine VPN e rotacione o mundo
        vpn_angle_x = np.arctan2(vpn[1], vpn[0])
        vpn_angle_y = np.arctan2(np.sqrt(vpn[0] ** 2 + vpn[1] ** 2), vpn[2])

        # 3. Rotacione o mundo em torno de X e Y para alinhar VPN com o eixo Z
        rotation_matrix_x = Transformation3D.rotation_x(np.degrees(vpn_angle_y))
        rotation_matrix_y = Transformation3D.rotation_y(np.degrees(vpn_angle_x))

        if obj.type == 'Polygon':
            return self.project_orthogonal_polygon(obj, rotation_matrix_x, rotation_matrix_y, translation_matrix)
        elif obj.type == 'Point':
            return self.project_orthogonal_point(obj, rotation_matrix_x, rotation_matrix_y, translation_matrix)
        elif obj.type == 'Bezier Surface':
            return self.project_orthogonal_bezier_surface(obj, rotation_matrix_x, rotation_matrix_y, translation_matrix)



    def project_orthogonal_point(self, obj, rotation_matrix_x, rotation_matrix_y, translation_matrix):
        # Ignore a coordenada Z
        px, py, pz = obj.coordinate_x_scn, obj.coordinate_y_scn, obj.coordinate_z_scn
        # Aplicar transformação
        transformed_point = np.dot(translation_matrix,
                                    np.dot(rotation_matrix_y, np.dot(rotation_matrix_x, [px, py, pz, 1])))
        # Clipping
        if self.clip_point(transformed_point[0], transformed_point[1]):
            x, y = self.transform_to_viewport(transformed_point[0], transformed_point[1])
            return x, y
        else:
            return None

    def project_orthogonal_polygon(self, obj, rotation_matrix_x, rotation_matrix_y, translation_matrix):
        # 4. Ignorar todas as coordenadas Z dos objetos
        normalized_points = []
        for i in range(len(obj.segments)):
            # Ignore a coordenada Z
            p1, p2 = obj.segments[i]
            p1_x, p1_y, p1_z = p1.coordinate_x_scn, p1.coordinate_y_scn, p1.coordinate_z_scn
            p2_x, p2_y, p2_z = p2.coordinate_x_scn, p2.coordinate_y_scn, p2.coordinate_z_scn
            # Aplicar transformações
            transformed_point1 = np.dot(translation_matrix,
                                        np.dot(rotation_matrix_y, np.dot(rotation_matrix_x, [p1_x, p1_y, p1_z, 1])))
            transformed_point2 = np.dot(translation_matrix,
                                        np.dot(rotation_matrix_y, np.dot(rotation_matrix_x, [p2_x, p2_y, p2_z, 1])))
            normalized_points.append((transformed_point1[0], transformed_point1[1]))
            normalized_points.append((transformed_point2[0], transformed_point2[1]))
        # 5. Clippe
        # Algoritmo de clipping aqui, se necessário
        clipped_points = self.clip_polygon(normalized_points)
        if clipped_points:
            # 6. Transforme para coordenadas de Viewport
            viewport_points = []
            for point in clipped_points:
                # Aplicar transformação para viewport chamando o método transform_to_viewport()
                x, y = self.transform_to_viewport(point[0], point[1])
                viewport_points.append((x, y))
            return viewport_points
        else:
            return None  # Retorna None se o polígono estiver completamente fora da janela de visualização

    def project_orthogonal_bezier_surface(self, obj, rotation_matrix_x, rotation_matrix_y, translation_matrix):
        control_points = np.array([point.to_array() for point in obj.coordinates])
        transformed_points = []

        for point in control_points:
            # Verifique se point tem pelo menos três componentes, adicionando 0 para z se necessário
            if len(point) == 2:
                point = np.append(point, 0)
            point_h = np.append(point, 1)  # Coordenadas homogêneas
            transformed_point = translation_matrix @ point_h
            transformed_point = rotation_matrix_x @ transformed_point
            transformed_point = rotation_matrix_y @ transformed_point
            transformed_points.append(transformed_point[:3])  # Mantém x, y, z para cálculos de Bézier

        transformed_points = np.array(transformed_points).reshape(4, 4, 3)
        return transformed_points


    def bezier_surface(self, control_points, u_values, v_values):
        m, n, _ = control_points.shape
        num_u = len(u_values)
        num_v = len(v_values)
        surface_points = np.zeros((num_u, num_v, 2))

        for i, u in enumerate(u_values):
            for j, v in enumerate(v_values):
                Bu = self.bernstein_basis(m - 1, u)
                Bv = self.bernstein_basis(n - 1, v)
                point = np.zeros(3)
                for k in range(m):
                    for l in range(n):
                        point += control_points[k, l] * Bu[k] * Bv[l]
                surface_points[i, j] = point[:2]  # Mantém apenas x, y para desenhar

        return surface_points


    def bernstein_basis(self, n, t):
        basis = np.zeros(n + 1)
        for i in range(n + 1):
            basis[i] = np.math.comb(n, i) * (t ** i) * ((1 - t) ** (n - i))
        return basis

    def perspective_projection(self, obj, cop, vpn):
        # 1. Translade COP para a origem
        translation_matrix = Transformation3D.translation(-cop[0], -cop[1], -cop[2])

        # 2. Determine os ângulos de VPN com X e Y
        vpn_angle_x = np.arctan2(vpn[1], vpn[0])
        vpn_angle_y = np.arctan2(np.sqrt(vpn[0] ** 2 + vpn[1] ** 2), vpn[2])

        # 3. Rotacione o mundo em torno de X e Y para alinhar VPN com o eixo Z
        rotation_matrix_x = Transformation3D.rotation_x(np.degrees(vpn_angle_y))
        rotation_matrix_y = Transformation3D.rotation_y(np.degrees(vpn_angle_x))

        if obj.type == 'Polygon':
            return self.project_perspective_polygon(cop, obj, rotation_matrix_x, rotation_matrix_y, translation_matrix)
        elif obj.type == 'Point':
            return self.project_perspective_point(cop, obj, rotation_matrix_x, rotation_matrix_y, translation_matrix)

    def project_perspective_point(self, cop, obj, rotation_matrix_x, rotation_matrix_y, translation_matrix):
        px, py, pz = obj.coordinate_x_scn, obj.coordinate_y_scn, obj.coordinate_z_scn
        d = pz - cop[2]
        transform_matrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0], [0, 0, (1 / d), 1]])
        transformed_point = np.dot(transform_matrix, [px, py, pz, 1])
        xp = transformed_point[0] / transformed_point[3]
        yp = transformed_point[1] / transformed_point[3]
        normalized_point = np.dot(translation_matrix, np.dot(rotation_matrix_y, np.dot(rotation_matrix_x,
                                                                                       [xp, yp,
                                                                                        0, 1])))
        if self.clip_point(normalized_point[0], normalized_point[1]):
            x, y = self.transform_to_viewport(normalized_point[0], normalized_point[1])
            return x, y
        else:
            return None

    def project_perspective_polygon(self, cop, obj, rotation_matrix_x, rotation_matrix_y, translation_matrix):
        # 4. Projete, calculando xp e yp
        projected_points = []
        for segment in obj.segments:
            for point in segment:  # Apply transformations
                px, py, pz = point.coordinate_x_scn, point.coordinate_y_scn, point.coordinate_z_scn
                d = pz - cop[2]
                transform_matrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, (1 / d), 0]])
                transformed_point = np.dot(transform_matrix, [px, py, pz, 1])
                xp = transformed_point[0] / transformed_point[3]  # Calculate xp
                yp = transformed_point[1] / transformed_point[3]  # Calculate yp
                projected_points.append((xp, yp, 0))
        # 5. Normalize xp e yp (coordenadas de window)
        normalized_points = []
        for point in projected_points:
            # Normalize points
            normalized_point = np.dot(translation_matrix, np.dot(rotation_matrix_y, np.dot(rotation_matrix_x,
                                                                                            [point[0], point[1],
                                                                                             point[2], 1])))
            # x_normalized = ...
            # y_normalized = ...
            normalized_points.append((normalized_point[0], normalized_point[1]))
        # 6. Clippe 2D
        clipped_points = self.clip_polygon(normalized_points)
        # 7. Transforme para coordenadas de Viewport
        if clipped_points:
            viewport_points = []
            for point in clipped_points:
                # Transform to viewport coordinates
                x, y = self.transform_to_viewport(point[0], point[1])  # Assuming z = 0 for viewport coordinates
                viewport_points.append((x, y))
            return viewport_points
        else:
            return None

    ################################################################################
############################### BASIC OPERATIONS ###############################
################################################################################

    def pan(self, dx, dy):
        self.window.xmin += dx
        self.window.ymin += dy
        # self.window.zmin += dz
        self.window.xmax += dx
        self.window.ymax += dy
        # self.window.zmax += dz

    def pan_left(self):
        self.pan(-20, 0)
        self.draw_display_file()

    def pan_right(self):
        self.pan(20, 0)
        self.draw_display_file()

    def pan_up(self):
        self.pan(0, -20)
        self.draw_display_file()

    def pan_down(self):
        self.pan(0, 20)
        self.draw_display_file()

    def zoom(self, factor):
        cx = (self.window.xmin + self.window.xmax) / 2
        cy = (self.window.ymin + self.window.ymax) / 2
        # cz = (self.window.zmin + self.window.zmax) / 2

        self.window.xmin = cx - (cx - self.window.xmin) * factor
        self.window.ymin = cy - (cy - self.window.ymin) * factor
        # self.window.zmin = cz - (cz - self.window.zmin) * factor
        self.window.xmax = cx + (self.window.xmax - cx) * factor
        self.window.ymax = cy + (self.window.ymax - cy) * factor
        # self.window.zmax = cz + (self.window.zmax - cz) * factor

        self.draw_display_file()

    def zoom_in(self):
        self.zoom(0.8)
        self.draw_display_file()

    def zoom_out(self):
        self.zoom(1.2)
        self.draw_display_file()

    def add_object(self):
        try:
            coordinates_str = self.entry_coordinates.get()
            object_color = self.color_string.get()
            filled = self.fill_var.get()
            coordinates = coordinates_str.replace("(", "").replace(")", "").split(",")
            coordinates_head = self.object_type.get()
            coordinates = list(map(lambda x: float(x), coordinates))

            if coordinates_head.upper() == "POINT":
                self.display_file.add_point((coordinates[0], coordinates[1], coordinates[2]), object_color)
            elif coordinates_head.upper() == "LINE":
                self.display_file.add_line([(coordinates[i], coordinates[i + 1], coordinates[i + 2]) for i in range(0, len(coordinates), 3)], object_color)
            elif coordinates_head.upper() == "WIREFRAME":
                self.display_file.add_wireframe([(coordinates[i], coordinates[i + 1], coordinates[i + 2]) for i in range(0, len(coordinates), 3)], object_color, filled)
            elif coordinates_head.upper() == "CURVE":
                self.display_file.add_curve([(coordinates[i], coordinates[i + 1], coordinates[i + 2]) for i in range(0, len(coordinates), 3)], object_color)
            elif coordinates_head.upper() == "B-SPLINE":
                self.display_file.add_b_spline([(coordinates[i], coordinates[i + 1], coordinates[i + 2]) for i in range(0, len(coordinates), 3)], object_color)
            elif coordinates_head.upper() == "POLYGON":
                self.display_file.add_polygon([(coordinates[i], coordinates[i + 1], coordinates[i + 2]) for i in range(0, len(coordinates), 3)], object_color)
            elif coordinates_head.upper() == "BEZIER SURFACE":
                control_points = self.entry_control_points.get()
                self.display_file.add_bezier_surface(control_points, object_color)
            else:
                print("Unable to add object")
            self.draw_display_file()
        except IndexError:
            print("Insufficient coordinates")
        except ValueError:
            print("Invalid coordinates")


    def remove_object(self):
        object_name = self.entry_object_name.get()
        self.display_file.remove_object(object_name)
        self.draw_display_file()

    def get_object_center(self, obj):
        if obj.type == "Point":
            return obj.coordinate_x, obj.coordinate_y, obj.coordinate_z
        elif obj.type == "Line":
            center_x = (obj.start_point[0] + obj.end_point[0]) / 2
            center_y = (obj.start_point[1] + obj.end_point[1]) / 2
            center_z = (obj.start_point[2] + obj.end_point[2]) / 2
            return center_x, center_y, center_z
        elif obj.type in ["Wireframe", "Curve", "B-Spline"]:
            center_x = sum([p[0] for p in obj.point_list]) / len(obj.point_list)
            center_y = sum([p[1] for p in obj.point_list]) / len(obj.point_list)
            center_z = sum([p[2] for p in obj.point_list]) / len(obj.point_list)
            return center_x, center_y, center_z
        elif obj.type == "Polygon":
            center_x = sum([p.coordinate_x for p in obj.coordinates]) / len(obj.coordinates)
            center_y = sum([p.coordinate_y for p in obj.coordinates]) / len(obj.coordinates)
            center_z = sum([p.coordinate_z for p in obj.coordinates]) / len(obj.coordinates)
            return center_x, center_y, center_z

