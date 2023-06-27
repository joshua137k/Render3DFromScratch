import pygame as pg
from pygame.locals import *
import sys
import math
from mesh import Mesh
from camera import Projection






class Cube(Mesh):
    def __init__(self,render, position=(0,0,0), size=(1,1,1), rotation=(0,0,0)):
        super().__init__(render,position, size, rotation)

        self.add_point((-1, -1, -1))
        self.add_point((1, -1, -1))
        self.add_point((1, 1, -1))
        self.add_point((-1, 1, -1))
        self.add_point((-1, -1, 1))
        self.add_point((1, -1, 1))
        self.add_point((1, 1, 1))
        self.add_point((-1, 1, 1))

        self.add_face((0, 1, 2))
        self.add_face((0, 2, 3))
        self.add_face((3, 2, 6))
        self.add_face((3, 6, 7))
        self.add_face((7, 6, 5))
        self.add_face((7, 5, 4))
        self.add_face((4, 5, 1))
        self.add_face((4, 1, 0))
        self.add_face((1, 5, 6))
        self.add_face((1, 6, 2))
        self.add_face((4, 0, 3))
        self.add_face((4, 3, 7))

        self.add_color((255, 255, 255))
        self.add_color((255, 0, 0))
        self.add_color((0, 255, 0))
        self.add_color((25, 0, 90))
        self.add_color((0, 0, 255))
        self.add_color((90, 90, 90))



class EngineRender:
    def __init__(self):
        pg.init()
        pg.mouse.set_pos((0,0))
        pg.mouse.set_visible(False)
        self.width, self.height = 800, 600
        self.aspect_ratio = self.width / self.height
        self.intervalo=200
        self.FPS = 60
        self.screen = pg.display.set_mode((self.width, self.height))
        self.clock = pg.time.Clock()
        self.fov = 200
        self.vrp_x, self.vrp_y, self.vrp_z = 0, 0, 0
        self.cor_texto = (0,0,0)  # Branco
        self.tamanho_fonte = 20
        self.fonte = pg.font.Font(None, self.tamanho_fonte)
        self.texto=""
        self.create_objects()


    def create_objects(self):
        self.projection = Projection(self)
        self.cubes=[]

        for i in range(3):
            self.cubes.append( Cube(self,(0,0,i*20),(100,10,10)) )
        for i in range(3):
            self.cubes.append(Cube(self,(0,-i*20-22,30),(10,10,10)))
        for i in range(3):
            for j in range(3):
                self.cubes.append(Cube(self,(i*20-22,-4*20,j*20+8),(10,10,10)))
        #Arrumar a profundidade por ordem
        
        self.cubes = sorted(self.cubes, key=lambda cube: self.cubes.index(cube))
       #print(sorted_cubes)



    def draw(self):
        camera_position = (self.projection.camera_x, self.projection.camera_y, self.projection.camera_z)
        self.texto=f"{self.projection.camera_x}{self.projection.camera_y}{self.projection.camera_z}"
        self.screen.fill(pg.Color('darkslategray'))
        superficie_texto = self.fonte.render(self.texto, True, self.cor_texto)
        self.screen.blit(superficie_texto,(0,0))
        for i in self.cubes:
            if self.calculate_distance(camera_position,i.position)<400:
                i.update()
    def calculate_distance(self, point1, point2):
        x1, y1, z1 = point1
        x2, y2, z2 = point2
        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)
        return distance

    def control(self):
        mouse_movement = pg.mouse.get_rel()
        keys = pg.key.get_pressed()
        if keys[K_a]:
            self.projection.camera_x -= 1
            
        if keys[K_d]:
            self.projection.camera_x += 1
        if keys[K_UP]:
            self.projection.camera_y -= 1
        if keys[K_DOWN]:
            self.projection.camera_y += 1
        if keys[K_w]:
            self.projection.camera_x += math.sin(math.radians(self.projection.rotation_z))
            self.projection.camera_z += math.cos(math.radians(self.projection.rotation_z))
        if keys[K_s]:
            self.projection.camera_z -= 1
        self.projection.rotation_z += mouse_movement[0] * 0.2
        if keys[K_ESCAPE]:
            pg.quit()
            sys.exit()


    def run(self):
        while True:
            self.draw()
            [exit() for i in pg.event.get() if i.type == pg.QUIT]

            
            # Mover o VRP com as teclas de seta
            self.control()

            pg.display.set_caption(str(self.clock.get_fps()))
            pg.display.flip()
            self.clock.tick(self.FPS)


if __name__ == '__main__':
    app = EngineRender()
    app.run()