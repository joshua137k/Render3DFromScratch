
import math

class Projection:
    def __init__(self,render):
        self.render=render
        self.camera_x=0
        self.camera_y=-50
        self.camera_z=-150
        self.rotation_x=0
        self.rotation_y=0
        self.rotation_z=0
        self.xproj=0
        self.yproj=0
    def project3DTo2D(self, point, size):
        x, y, z = point

        # Definir a distância do plano de projeção
        fov = self.render.fov

        # Aplicar a posição do cubo durante a projeção
        x -= self.camera_x
        y -= self.camera_y
        z -= self.camera_z
        x, z = x * math.cos(math.radians(self.rotation_z)) - z * math.sin(math.radians(self.rotation_z)), x * math.sin(math.radians(self.rotation_z)) + z * math.cos(math.radians(self.rotation_z))
        y, z = y * math.cos(math.radians(self.rotation_x)) - z * math.sin(math.radians(self.rotation_x)), y * math.sin(math.radians(self.rotation_x)) + z * math.cos(math.radians(self.rotation_x))

        if z > 0:
            f = self.render.fov / (z + 1e-5)
            x_proj, y_proj = x * f, y * f
            x_proj += self.render.width / 2
            y_proj += self.render.height / 2
            self.xproj,self.y_proj=int(x_proj), int(y_proj)
            return int(x_proj), int(y_proj)
        return None