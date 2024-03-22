import tkinter as tk
import numpy as np

class DisplayFile2D:
    def __init__(self):
        self.objects = {}  # Dicionário para armazenar objetos
        self.counters = {'point': 0, 'line': 0, 'wireframe': 0}  # Contadores para nomeação dos objetos

    def add_point(self, coordinates):
        name = f'Ponto{self.counters["point"] + 1}'
        self.objects[name] = ('point', coordinates)
        self.counters['point'] += 1

    def add_line(self, coordinates):
        name = f'Reta{self.counters["line"] + 1}'
        self.objects[name] = ('line', coordinates)
        self.counters['line'] += 1

    def add_wireframe(self, coordinates):
        name = f'Wireframe{self.counters["wireframe"] + 1}'
        self.objects[name] = ('wireframe', coordinates)
        self.counters['wireframe'] += 1

    def remove_object(self, name):
        if name in self.objects:
            del self.objects[name]


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

        # Desenhar a borda da viewport
        self.viewport_border = self.canvas.create_rectangle(*self.viewport, outline='red', dash=(5, 5))
        
        # Desenhar a borda da janela
        self.window_border = self.canvas.create_rectangle(*self.window, outline='blue')

        self.setup_object_list_interface()
        self.setup_remove_object_interface()
        self.setup_transformation_interface()
        self.setup_pan_interface()
        self.setup_zoom_interface()

    def transform_to_viewport(self, x, y):
        xmin, ymin, xmax, ymax = self.window
        xvmin, yvmin, xvmax, yvmax = self.viewport

        xv = ((x - xmin) / (xmax - xmin)) * (xvmax - xvmin) + xvmin
        yv = ((y - ymin) / (ymax - ymin)) * (yvmax - yvmin) + yvmin

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

    def setup_transformation_interface(self):
        self.label_transformation = tk.Label(self.master, text="Transformation")
        #self.label_transformation.place(x=650, y=150)
        self.label_transformation.pack()

        self.entry_transformation = tk.Entry(self.master)
        #self.entry_transformation.place(x=650, y=180)
        self.entry_transformation.pack()

        self.label_object_name = tk.Label(self.master, text="Object Name:")
        #self.label_object_name.place(x=650, y=300)
        self.label_object_name.pack()

        self.entry_object_name_transform = tk.Entry(self.master)
        #self.entry_object_name_transform.place(x=650, y=330)
        self.entry_object_name_transform.pack()

        self.label_params = tk.Label(self.master, text="Params (comma separated)")
        #self.label_params.place(x=650, y=210)
        self.label_params.pack()

        self.entry_params = tk.Entry(self.master)
        #self.entry_params.place(x=650, y=240)
        self.entry_params.pack()

        self.button_transform = tk.Button(self.master, text="Transform Object", command=self.transform_object)
        #self.button_transform.place(x=650, y=270)
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

def add_object():
    coordinates_str = entry_coordinates.get()
    coordinates = eval(coordinates_str)
    display_file.add_wireframe(coordinates)
    graphics_system.draw_display_file()

label_coordinates = tk.Label(root, text="Coordinates:")
label_coordinates.pack(side=tk.TOP)

entry_coordinates = tk.Entry(root)
entry_coordinates.pack(side=tk.TOP)

button_add_object = tk.Button(root, text="Add Object", command=add_object)
button_add_object.pack(side=tk.TOP)

root.mainloop()
