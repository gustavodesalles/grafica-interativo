import tkinter as tk
import numpy as np
import ast

class DisplayFile2D:
    def __init__(self):
        self.objects = {}  # Dicionário para armazenar objetos
        self.counters = {'point': 0, 'line': 0, 'wireframe': 0, 'curve': 0}  # Contadores para nomeação dos objetos

    def add_point(self, coordinates, color='black'):
        name = f'Ponto{self.counters["point"] + 1}'
        self.objects[name] = ('point', coordinates, color)
        self.counters['point'] += 1

    def add_line(self, coordinates, color='black'):
        name = f'Reta{self.counters["line"] + 1}'
        self.objects[name] = ('line', coordinates, color)
        self.counters['line'] += 1

    def add_wireframe(self, coordinates, color='black'):
        name = f'Wireframe{self.counters["wireframe"] + 1}'
        self.objects[name] = ('wireframe', coordinates, color)
        self.counters['wireframe'] += 1

    def add_curve(self, points, color='black'):
        name = f'Curva{self.counters["curve"] + 1}'
        self.objects[name] = ('curve', points, color)
        self.counters['curve'] += 1    

    def remove_object(self, name):
        if name in self.objects:
            del self.objects[name]

class OBJDescriptor:
    @staticmethod
    def write_obj_file(file_path, obj_name, obj_type, vertices, color):
        with open(file_path, 'w') as f:
            f.write(f'g {obj_name}\n')
            for vertex in vertices:
                f.write(f'v {vertex[0]} {vertex[1]} 0.0\n')
            if obj_type == 'line' or obj_type == 'wireframe':
                for i in range(1, len(vertices) + 1):
                    f.write(f'l {i} {i % len(vertices) + 1}\n')
            # Escrever a cor como um comentário
            f.write(f'# Color: {color}\n')


class Transformation2D:
    @staticmethod
    def translation(tx, ty):
        return np.array([
            [1, 0, tx],
            [0, 1, ty],
            [0, 0, 1]
        ])

    @staticmethod
    def rotation(angle):
        theta = np.radians(angle)
        cos_theta = np.cos(theta)
        sin_theta = np.sin(theta)
        return np.array([
            [cos_theta, -sin_theta, 0],
            [sin_theta, cos_theta, 0],
            [0, 0, 1]
        ])

    @staticmethod
    def scale(sx, sy):
        return np.array([
            [sx, 0, 0],
            [0, sy, 0],
            [0, 0, 1]
        ])

    @staticmethod
    def arbitrary_rotation(theta, center):
        cx, cy = center
        translation_matrix = Transformation2D.translation(-cx, -cy)
        rotation_matrix = Transformation2D.rotation(theta)
        inv_translation_matrix = Transformation2D.translation(cx, cy)
        return np.dot(inv_translation_matrix, np.dot(rotation_matrix, translation_matrix))

class GraphicsSystem2D:
    def __init__(self, master, display_file, object_list):
        self.master = master
        self.display_file = display_file
        self.object_list = object_list

        # Canvas
        self.canvas = tk.Canvas(master, width=800, height=500, bg='white')
        self.canvas.pack(side=tk.LEFT)

        self.window = [-300, -200, 300, 200]  # Coordenadas da janela
        self.viewport = [100, 100, 700, 400]  # Coordenadas da viewport

        # Adicionar rótulos para viewport e window
        self.label_viewport = tk.Label(master, text="Viewport", font=('Helvetica', 14))
        self.label_viewport.place(x=650, y=10)
        self.label_window = tk.Label(master, text="Window", font=('Helvetica', 14))
        self.label_window.place(x=100, y=10)

        canvas_width = self.canvas.winfo_reqwidth()
        canvas_height = self.canvas.winfo_reqheight()

        # Ajustar a viewport para ser menor que o objeto de desenho
        viewport_margin = 20
        self.viewport = [
            canvas_width // 4 + viewport_margin,
            canvas_height // 4 + viewport_margin,
            3 * canvas_width // 4 - viewport_margin,
            3 * canvas_height // 4 - viewport_margin
        ]

        # Ajustar a janela para ser igual ao canvas
        self.window = [0, 0, canvas_width, canvas_height]

        # Desenhar uma moldura ao redor da viewport
        self.viewport_frame = self.canvas.create_rectangle(*self.viewport, outline='green')

        # Inicializar a técnica de clipagem atual
        self.clipping_method = 'parametric'

        self.setup_object_list_interface()
        self.setup_remove_object_interface()
        self.setup_add_object_interface()
        self.setup_transformation_interface()
        self.setup_pan_interface()
        self.setup_zoom_interface()
        self.setup_rotation_interface()
        self.setup_export_object_interface()
        self.setup_import_object_interface()
        self.setup_clipping_interface()


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
        xmin, ymin, xmax, ymax = self.window
        xvmin, yvmin, xvmax, yvmax = self.viewport

        xv = ((x_rotated - xmin) / (xmax - xmin)) * (xvmax - xvmin) + xvmin
        yv = ((y_rotated - ymin) / (ymax - ymin)) * (yvmax - yvmin) + yvmin

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
        self.label_coordinates = tk.Label(root, text="Coordinates:")
        self.label_coordinates.pack(side=tk.TOP)

        self.entry_coordinates = tk.Entry(root)
        self.entry_coordinates.pack(side=tk.TOP)

        self.label_curve_points = tk.Label(root, text="Hermite Curve Points:")
        self.label_curve_points.pack(side=tk.TOP)

        self.entry_curve_points = tk.Entry(root)  # Adicione uma entrada para os pontos de controle da curva de Hermite
        self.entry_curve_points.pack(side=tk.TOP)

        self.button_add_object = tk.Button(root, text="Add Object", command=self.add_object)
        self.button_add_object.pack(side=tk.TOP)


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

    def setup_pan_interface(self):
        button_pan_left = tk.Button(root, text="Pan Left", command=self.pan_left)
        button_pan_left.pack(side=tk.TOP)

        button_pan_right = tk.Button(root, text="Pan Right", command=self.pan_right)
        button_pan_right.pack(side=tk.TOP)

    def setup_zoom_interface(self):
        button_zoom_in = tk.Button(root, text="Zoom In", command=self.zoom_in)
        button_zoom_in.pack(side=tk.TOP)

        button_zoom_out = tk.Button(root, text="Zoom Out", command=self.zoom_out)
        button_zoom_out.pack(side=tk.TOP)

    def setup_rotation_interface(self):
        self.label_rotation = tk.Label(self.master, text="Rotation Angle (Vup):")
        self.label_rotation.pack()
        self.entry_rotation = tk.Entry(self.master)
        self.entry_rotation.pack()
        self.button_rotate_object = tk.Button(self.object_list_frame, text="Rotate Object", command=self.rotate_vup)
        self.button_rotate_object.pack()

    def setup_export_object_interface(self):
        self.label_export_obj = tk.Label(root, text="Export Obj:")
        self.label_export_obj.pack()

        self.entry_export_obj_name = tk.Entry(root)
        self.entry_export_obj_name.pack()

        self.button_export_object = tk.Button(root, text="Export Obj", command=self.export_object)
        self.button_export_object.pack()

    def setup_import_object_interface(self):
        self.label_import_obj = tk.Label(root, text="Import Obj:")
        self.label_import_obj.pack()

        self.entry_import_obj_name = tk.Entry(root)
        self.entry_import_obj_name.pack()

        self.button_import_object = tk.Button(root, text="Import Obj", command=self.import_object)
        self.button_import_object.pack()

    def setup_clipping_interface(self):
       # Adicionar radio buttons para selecionar a técnica de clipagem
        self.label_clipping_method = tk.Label(self.master, text="Clipping Method")
        self.label_clipping_method.pack()

        self.var_clipping_method = tk.StringVar()
        self.var_clipping_method.set('parametric')

        self.radio_parametric = tk.Radiobutton(self.master, text="Parametric Clipping", variable=self.var_clipping_method, value='parametric', command=self.change_clipping_method)
        self.radio_parametric.pack()

        self.radio_cohen_sutherland = tk.Radiobutton(self.master, text="Cohen-Sutherland Clipping", variable=self.var_clipping_method, value='cohen_sutherland', command=self.change_clipping_method)
        self.radio_cohen_sutherland.pack()


    def change_clipping_method(self):
        self.clipping_method = self.var_clipping_method.get()

    def clip_line(self, x1, y1, x2, y2):
        if self.clipping_method == 'parametric':
            return self.clip_parametric(x1, y1, x2, y2)
        elif self.clipping_method == 'cohen_sutherland':
            return self.clip_cohen_sutherland(x1, y1, x2, y2)

    def clip_parametric(self, x1, y1, x2, y2):
        # Implementação do algoritmo de clipagem usando a equação paramétrica da reta
        # Checagem por meio da equação paramétrica envolvendo os limites da janela e a própria linha
        # Retorna as coordenadas clipadas (x1_clip, y1_clip, x2_clip, y2_clip)
        xmin, ymin, xmax, ymax = self.window
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
        xmin, ymin, xmax, ymax = self.window
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
            if code_outside & 1:  # Topo da janela
                x = x1 + (x2 - x1) * (ymax - y1) / (y2 - y1)
                y = ymax
            elif code_outside & 2:  # Fundo da janela
                x = x1 + (x2 - x1) * (ymin - y1) / (y2 - y1)
                y = ymin
            elif code_outside & 4:  # Direita da janela
                y = y1 + (y2 - y1) * (xmax - x1) / (x2 - x1)
                x = xmax
            elif code_outside & 8:  # Esquerda da janela
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
        xmin, ymin, xmax, ymax = self.window

        if x < xmin:  # Esquerda da janela
            code |= 1
        elif x > xmax:  # Direita da janela
            code |= 2
        if y < ymin:  # Topo da janela
            code |= 4
        elif y > ymax:  # Fundo da janela
            code |= 8

        return code

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
                obj_name = f'Imported_Object_{len(self.display_file.objects) + 1}'
                
                # Check for color information
                color_line_index = lines.index("# Color: black\n") if "# Color: black\n" in lines else -1
                if color_line_index != -1:
                    color_line = lines[color_line_index]
                    # Extract color information if available
                    color = color_line.split(":")[1].strip()
                    print(f"Cor do objeto: {color}")
                else:
                    color = "black"  # Default color
                    
                # Check the type of object and add it appropriately
                if "l" in lines[0]:  # Check if the object is a line
                    self.display_file.add_line(vertices, color)
                elif "v" in lines[0]:  # Check if the object is a point
                    self.display_file.add_point(vertices, color)
                elif "f" in lines[0]:  # Check if the object is a wireframe
                    self.display_file.add_wireframe(vertices, color)
                    
                self.draw_display_file()
                print(f"Objeto importado de '{file_path}'.")
        except FileNotFoundError:
            print(f"Arquivo '{file_path}' não encontrado.")


    def transform_object(self):
        obj_name = self.entry_object_name.get()
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

    def draw_object(self, obj_type, coordinates, color='black'):
        if obj_type == 'point':
            x, y = self.transform_to_viewport(*coordinates)  # Apenas um conjunto de coordenadas para o ponto
            if self.clip_point(x, y):
                self.canvas.create_oval(x, y, x + 2, y + 2, fill=color)  # Desenha um pequeno oval para representar o ponto
        elif obj_type == 'line':
            x1, y1 = self.transform_to_viewport(*coordinates[:2])  # As coordenadas da reta estão no primeiro conjunto
            x2, y2 = self.transform_to_viewport(*coordinates[2:])  # As coordenadas da reta estão no segundo conjunto
            self.canvas.create_line(x1, y1, x2, y2, fill=color)
        elif obj_type == 'wireframe':
            transformed_coords = [self.transform_to_viewport(*coord) for coord in coordinates]
            self.draw_wireframe(transformed_coords)


    def clip_point(self, x, y):
        # Verificar se o ponto está dentro da viewport
        return self.viewport[0] <= x <= self.viewport[2] and self.viewport[1] <= y <= self.viewport[3]

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

        try:
            self.angle_vup = float(self.entry_rotation.get())
        except ValueError:
            self.angle_vup = 0

        self.viewport_border = self.canvas.create_rectangle(*self.viewport, outline='red', dash=(5, 5))
        self.window_border = self.canvas.create_rectangle(*self.window, outline='blue')

        for obj_name, (obj_type, coordinates, color) in self.display_file.objects.items():
            if obj_type == 'line':
                x1, y1 = coordinates[0]
                x2, y2 = coordinates[1]
                if self.clipping_method == 'parametric':
                    clipped_coords = self.clip_parametric(x1, y1, x2, y2)
                elif self.clipping_method == 'cohen_sutherland':
                    clipped_coords = self.clip_cohen_sutherland(x1, y1, x2, y2)
                else:
                    clipped_coords = (x1, y1, x2, y2)
                if clipped_coords and isinstance(clipped_coords, tuple):
                    self.draw_object(obj_type, clipped_coords, color)
            elif obj_type == 'point':
                self.draw_object(obj_type, coordinates, color)
            elif obj_type == 'curve':  # Adicione um caso para a curva de Hermite
                self.draw_hermite_curve(coordinates, color)

    def draw_hermite_curve(self, control_points, color):
        pass
        # num_segments = 100  # Número de segmentos para desenhar a curva
        # t_values = np.linspace(0, 1, num_segments)

        # print("CONTROL")
        # print(control_points)

        # for i in range(1,len(control_points) - 2):
        #     #p0, m0, p1, m1 = control_points[i]  # Extrair os pontos de controle e vetores de tangente

        #     for t in t_values:
        #         t2 = t * t
        #         t3 = t2 * t
        #         h1 = 2 * t3 - 3 * t2 + 1
        #         h2 = -2 * t3 + 3 * t2
        #         h3 = t3 - 2 * t2 + t
        #         h4 = t3 - t2

        #         x = h1 * p0[0] + h2 * p1[0] + h3 * m0[0] + h4 * m1[0]
        #         y = h1 * p0[1] + h2 * p1[1] + h3 * m0[1] + h4 * m1[1]

        #         x, y = self.transform_to_viewport(x, y)  # Transformar as coordenadas para a viewport
        #         if self.clip_point(x, y):  # Verificar se o ponto está dentro da viewport
        #             self.canvas.create_oval(x, y, x + 2, y + 2, fill=color)  # Desenhar o ponto na viewport

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

    def pan_left(self):
        self.pan(-20, 0)
        self.draw_display_file()

    def pan_right(self):
        self.pan(20, 0)
        self.draw_display_file()

    def zoom_in(self):
        self.zoom(0.8)
        self.draw_display_file()

    def zoom_out(self):
        self.zoom(1.2)
        self.draw_display_file()

    def remove_object(self):
        object_name = self.entry_object_name.get()
        self.display_file.remove_object(object_name)
        self.draw_display_file()

    def add_object(self):
        coordinates_str = self.entry_curve_points.get()
        object_type = self.get_object_type(coordinates_str)

        print(object_type)
        
        if object_type == 'hermite_curve':
            coordinates = self.parse_hermite_curve(coordinates_str)
        elif object_type == "B-Spline":
            parsed_coord = self.parse_hermite_curve(coordinates_str)
            coordinates = self.calculate_b_spline(parsed_coord)
        else:
            coordinates = self.parse_coordinates(coordinates_str)

        print(coordinates)

        if coordinates:
            if (object_type == "hermite_curve" or object_type == "B-Spline"):
                self.display_file.add_curve(coordinates)
            elif len(coordinates) == 1:
                self.display_file.add_point(coordinates)
            elif len(coordinates) == 2:
                self.display_file.add_line(coordinates)
            elif len(coordinates) > 2:
                self.display_file.add_wireframe(coordinates)
            self.draw_display_file()
        else:
            print("Entrada de coordenadas inválida.")

    def get_object_type(self, coordinates_str):
        if coordinates_str.startswith("[("):  # Verifica se a entrada parece ser para uma curva de Hermite
            return 'hermite_curve'
        else:
            return 'other'  # Assume que a entrada é para outro tipo de objeto

    def parse_hermite_curve(self, coordinates_str):
        coordinates = ast.literal_eval(coordinates_str)
        coordinates_result = []
        for group in coordinates:
            for coord in group:
                coordinates_result.append(coord)
        return coordinates_result


    def parse_coordinates(self, coordinates_str):
        try:
            coordinates = eval(coordinates_str)
        except Exception as e:
            print("Erro ao analisar as coordenadas:", e)
            return None
        return coordinates
    
    def calculate_b_spline(self, control_points):
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

        return spline_points


    def rotate_vup(self):
        angle = float(self.entry_rotation.get())
        self.angle_vup = angle
        self.draw_display_file()

    def export_object(self):
        obj_name = self.entry_export_obj_name.get()
        if obj_name in self.display_file.objects:
            obj_data = self.display_file.objects[obj_name]
            if len(obj_data) == 2:  # Sem cor associada
                obj_type, vertices = obj_data
                color = "black"  # Cor padrão
            elif len(obj_data) == 3:  # Com cor associada
                obj_type, vertices, color = obj_data
            else:
                print("Formato de objeto inválido.")
                return

            file_path = f"{obj_name}.obj"
            if obj_type in ['point', 'line', 'wireframe']:  # Modificação aqui
                OBJDescriptor.write_obj_file(file_path, obj_name, obj_type, vertices, color)
                print(f"Objeto '{obj_name}' exportado para '{file_path}'.")
            else:
                print("Apenas objetos do tipo 'point', 'line' ou 'wireframe' podem ser exportados.")  # Modificação aqui
        else:
            print(f"O objeto '{obj_name}' não existe na lista de objetos.")


# Exemplo de uso - main file
root = tk.Tk()
root.title("2D Graphics System")

display_file = DisplayFile2D()
display_file.add_line(((-50, -50), (50, 50)))
display_file.add_point((50, 90))
#display_file.add_wireframe([(100, -100), (100, 100), (-100, 100), (-100, -100)])4
control_points = [((-50, -50), (100, 0), (100, 0), (100, 100)), ((-50, 50), (0, 100), (0, 100), (-100, 100))]
#display_file.add_curve(control_points, 'red')

object_list = tk.Listbox(root)

graphics_system = GraphicsSystem2D(root, display_file, object_list)
graphics_system.draw_display_file()

root.mainloop()
