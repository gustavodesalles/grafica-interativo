class OBJDescriptor:
    @staticmethod
    def write_obj_file(file_path, obj):
        with open(file_path, 'w') as f:
            f.write(f'g {obj.name}\n')
            if obj.type == 'Point':
                f.write(f'v {obj.coordinate_x} {obj.coordinate_y} 0.0\n')
            if obj.type == 'Line':
                f.write(f'v {obj.start_point[0]} {obj.start_point[1]} 0.0\n')
                f.write(f'v {obj.end_point[0]} {obj.end_point[1]} 0.0\n')
                f.write(f'l {1} {2}\n')
            else:
                for vertex in obj.point_list:
                    f.write(f'v {vertex[0]} {vertex[1]} 0.0\n')
                for i in range(1, len(obj.point_list) + 1):
                    f.write(f'l {i} {i % len(obj.point_list) + 1}\n')
                if obj.type == 'Wireframe':
                    # Marca se o wireframe é preenchido ou não
                    f.write(f'# Filled: {obj.filled}\n')
            # Escrever a cor como um comentário
            f.write(f'# Color: {obj.color}\n')
            f.write(f'# Type: {obj.type}\n')