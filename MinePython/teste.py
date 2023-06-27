import pygame
from pygame.locals import *
from math import sin, cos, radians

# Inicialização do Pygame
pygame.init()

# Configurações da janela
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Variáveis de posição e rotação da câmera
camera_x, camera_y, camera_z = 0, 0, -5
camera_yaw, camera_pitch = 0, 0





def project3DTo2D(x,y,z):
    x -= camera_x
    y -= camera_y
    z -= camera_z

    x, z = x * cos(radians(camera_yaw)) - z * sin(radians(camera_yaw)), x * sin(radians(camera_yaw)) + z * cos(radians(camera_yaw))
    y, z = y * cos(radians(camera_pitch)) - z * sin(radians(camera_pitch)), y * sin(radians(camera_pitch)) + z * cos(radians(camera_pitch))

    if z > 0:
        f = 200 / z
        x, y = x * f, y * f
        return ((width / 2 + int(x), height / 2 + int(y)))
    return None


# Função para desenhar o cubo
# Função para desenhar o cubo
def draw_cube():
    vertices = [
        (1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, -1, -1),
        (1, -1, 1), (1, 1, 1), (-1, -1, 1), (-1, 1, 1)
    ]

    faces = [
        (0, 1, 2, 3),  # Face frontal
        (4, 5, 6, 7),  # Face traseira
        (0, 1, 5, 4),  # Face superior
        (2, 3, 7, 6),  # Face inferior
        (0, 3, 7, 4),  # Face esquerda
        (1, 2, 6, 5)   # Face direita
    ]

    # Projeção dos pontos 3D para 2D
    projected_points = []
    for vertex in vertices:
        x, y, z = vertex
        v = project3DTo2D(x, y, z)
        if v != None:
            projected_points.append(v)

    # Desenho das faces do cubo
    print(projected_points)
    if len(projected_points)>7:
        for face in faces:
            points = []
            for vertex_index in face:
                x, y = projected_points[vertex_index]
                points.append((x, y))
            pygame.draw.polygon(screen, (255, 255, 255), points)
    # ...

# Loop principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Capturar as teclas pressionadas
    keys = pygame.key.get_pressed()
    if keys[K_w]:
        camera_x += sin(radians(camera_yaw))
        camera_z += cos(radians(camera_yaw))
    if keys[K_s]:
        camera_x -= sin(radians(camera_yaw))
        camera_z -= cos(radians(camera_yaw))
    if keys[K_a]:
        camera_x += sin(radians(camera_yaw - 90))
        camera_z += cos(radians(camera_yaw - 90))
    if keys[K_d]:
        camera_x -= sin(radians(camera_yaw - 90))
        camera_z -= cos(radians(camera_yaw - 90))
    if keys[K_q]:
        camera_y += 1
    if keys[K_e]:
        camera_y -= 1

    # Capturar o movimento do mouse
    mouse_movement = pygame.mouse.get_rel()
    camera_yaw += mouse_movement[0] * 0.2
    camera_pitch += mouse_movement[1] * 0.2

    # Limpar a tela
    screen.fill((0, 0, 0))

    # Desenhar o cubo
    draw_cube()

    # Atualizar a tela
    pygame.display.flip()
    clock.tick(60)

# Encerrar o Pygame
pygame.quit()


# Encerrar o Pygame
pygame.quit()

