import pygame as pg
import math


class Mesh:
    def __init__(self,render, position, size, rotation):
        self.render=render
        self.position = position
        self.size = size
        self.rotation = rotation
        self.points = []
        self.faces = []
        self.normals = []
        self.colors = []


    def add_point(self, point):
        self.points.append(point)


    def add_face(self, face):
        self.faces.append(face)


    def add_normal(self, normal):
        self.normals.append(normal)


    def add_color(self, color):
        self.colors.append(color)


    def setup(self):
            # Aplicar a rotação do cubo em torno dos eixos X, Y e Z
        rotation_x = self.rotation[0]
        rotation_y = self.rotation[1]
        rotation_z = self.rotation[2]

        rotation_matrix_x = [
            [1, 0, 0],
            [0, math.cos(rotation_x), -math.sin(rotation_x)],
            [0, math.sin(rotation_x), math.cos(rotation_x)]
        ]

        rotation_matrix_y = [
            [math.cos(rotation_y), 0, -math.sin(rotation_y)],
            [0, 1, 0],
            [math.sin(rotation_y), 0, math.cos(rotation_y)]
        ]

        rotation_matrix_z = [
            [math.cos(rotation_z), -math.sin(rotation_z), 0],
            [math.sin(rotation_z), math.cos(rotation_z), 0],
            [0, 0, 1]
        ]

        # Calcular a posição final do cubo
        self.position = (
            self.position[0],
            self.position[1],
            self.position[2] 
        )

        # Calcular os vetores normais das faces
        self.normals= []
        for face in self.faces:
            p0 = self.points[face[0]]
            p1 = self.points[face[1]]
            p2 = self.points[face[2]]
            v1 = (p1[0] - p0[0], p1[1] - p0[1], p1[2] - p0[2])
            v2 = (p2[0] - p0[0], p2[1] - p0[1], p2[2] - p0[2])
            normal = (
                v1[1] * v2[2] - v1[2] * v2[1],
                v1[2] * v2[0] - v1[0] * v2[2],
                v1[0] * v2[1] - v1[1] * v2[0]
            )
            self.normals.append(normal)

        return rotation_matrix_x,rotation_matrix_y,rotation_matrix_z
    
    
    def update(self):
        rotation_matrix_x, rotation_matrix_y, rotation_matrix_z = self.setup()
        # Transformar os pontos 3D para 2D e desenhar as faces visíveis
        k = 0


        for face, normal in zip(self.faces, self.normals):
            projected_points = []
            for i in face:
                point = self.points[i]
                rotated_point = [
                    point[0] * self.size[0],
                    point[1] * self.size[1],
                    point[2] * self.size[2]
                ]

                # Aplicar as rotações
                rotated_point = (
                    rotated_point[0] * rotation_matrix_x[0][0] + rotated_point[1] * rotation_matrix_x[0][1] + rotated_point[2] * rotation_matrix_x[0][2],
                    rotated_point[0] * rotation_matrix_x[1][0] + rotated_point[1] * rotation_matrix_x[1][1] + rotated_point[2] * rotation_matrix_x[1][2],
                    rotated_point[0] * rotation_matrix_x[2][0] + rotated_point[1] * rotation_matrix_x[2][1] + rotated_point[2] * rotation_matrix_x[2][2]
                )
                rotated_point = (
                    rotated_point[0] * rotation_matrix_y[0][0] + rotated_point[1] * rotation_matrix_y[0][1] + rotated_point[2] * rotation_matrix_y[0][2],
                    rotated_point[0] * rotation_matrix_y[1][0] + rotated_point[1] * rotation_matrix_y[1][1] + rotated_point[2] * rotation_matrix_y[1][2],
                    rotated_point[0] * rotation_matrix_y[2][0] + rotated_point[1] * rotation_matrix_y[2][1] + rotated_point[2] * rotation_matrix_y[2][2]
                )
                rotated_point = (
                    rotated_point[0] * rotation_matrix_z[0][0] + rotated_point[1] * rotation_matrix_z[0][1] + rotated_point[2] * rotation_matrix_z[0][2],
                    rotated_point[0] * rotation_matrix_z[1][0] + rotated_point[1] * rotation_matrix_z[1][1] + rotated_point[2] * rotation_matrix_z[1][2],
                    rotated_point[0] * rotation_matrix_z[2][0] + rotated_point[1] * rotation_matrix_z[2][1] + rotated_point[2] * rotation_matrix_z[2][2]
                )
                rotated_point = [
                    rotated_point[0] + self.position[0],
                    rotated_point[1] + self.position[1],
                    rotated_point[2] + self.position[2]
                ]

                projected_point = self.render.projection.project3DTo2D(rotated_point, self.size)
                if projected_point is not None:
                    projected_points.append(projected_point)

            # Verificar se a face é visível utilizando o teste do produto vetorial
            if len(projected_points) > 2:
                v1 = (
                    projected_points[1][0] - projected_points[0][0],
                    projected_points[1][1] - projected_points[0][1]
                )
                v2 = (
                    projected_points[2][0] - projected_points[0][0],
                    projected_points[2][1] - projected_points[0][1]
                )
                cross_product = v1[0] * v2[1] - v1[1] * v2[0]

                if cross_product > 0:
                    pg.draw.polygon(self.render.screen, self.colors[int(k)], projected_points)
                    pg.draw.polygon(self.render.screen, (0, 0, 0), projected_points, 1)
            k += 0.5

            # Atualizar o backup dos pontos projetados para a face atual

