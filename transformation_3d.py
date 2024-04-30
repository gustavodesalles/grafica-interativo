import numpy as np

class Transformation3D:
    @staticmethod
    def translation(tx, ty, tz):
        return np.array([
            [1, 0, 0, tx],
            [0, 1, 0, ty],
            [0, 0, 1, tz],
            [0, 0, 0, 1]
        ])

    @staticmethod
    def rotation_x(angle):
        theta = np.radians(angle)
        cos_theta = np.cos(theta)
        sin_theta = np.sin(theta)
        return np.array([
            [1, 0, 0, 0],
            [0, cos_theta, -sin_theta, 0],
            [0, sin_theta, cos_theta, 0],
            [0, 0, 0, 1]
        ])

    @staticmethod
    def rotation_y(angle):
        theta = np.radians(angle)
        cos_theta = np.cos(theta)
        sin_theta = np.sin(theta)
        return np.array([
            [cos_theta, 0, sin_theta, 0],
            [0, 1, 0, 0],
            [-sin_theta, 0, cos_theta, 0],
            [0, 0, 0, 1]
        ])

    @staticmethod
    def rotation_z(angle):
        theta = np.radians(angle)
        cos_theta = np.cos(theta)
        sin_theta = np.sin(theta)
        return np.array([
            [cos_theta, -sin_theta, 0, 0],
            [sin_theta, cos_theta, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

    @staticmethod
    def scale(sx, sy, sz, center):
        cx, cy, cz = center
        translation_matrix = Transformation3D.translation(-cx, -cy, -cz)
        inv_translation_matrix = Transformation3D.translation(cx, cy, cz)
        scale_matrix = np.array([
            [sx, 0, 0, 0],
            [0, sy, 0, 0],
            [0, 0, sz, 0],
            [0, 0, 0, 1]
        ])
        return np.dot(inv_translation_matrix, np.dot(scale_matrix, translation_matrix))

    @staticmethod
    def arbitrary_rotation_x(angle, center):
        cx, cy, cz = center
        translation_matrix = Transformation3D.translation(-cx, -cy, -cz)
        rotation_matrix = Transformation3D.rotation_x(angle)
        inv_translation_matrix = Transformation3D.translation(cx, cy, cz)
        return np.dot(inv_translation_matrix, np.dot(rotation_matrix, translation_matrix))

    @staticmethod
    def arbitrary_rotation_y(angle, center):
        cx, cy, cz = center
        translation_matrix = Transformation3D.translation(-cx, -cy, -cz)
        rotation_matrix = Transformation3D.rotation_y(angle)
        inv_translation_matrix = Transformation3D.translation(cx, cy, cz)
        return np.dot(inv_translation_matrix, np.dot(rotation_matrix, translation_matrix))

    @staticmethod
    def arbitrary_rotation_z(angle, center):
        cx, cy, cz = center
        translation_matrix = Transformation3D.translation(-cx, -cy, -cz)
        rotation_matrix = Transformation3D.rotation_z(angle)
        inv_translation_matrix = Transformation3D.translation(cx, cy, cz)
        return np.dot(inv_translation_matrix, np.dot(rotation_matrix, translation_matrix))
