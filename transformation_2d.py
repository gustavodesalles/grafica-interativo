import numpy as np


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
