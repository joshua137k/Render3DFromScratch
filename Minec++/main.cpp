#include <SFML/Graphics.hpp>
#include <SFML/Window/Keyboard.hpp>
#include <iostream>
#include <cmath>
#include <vector>



struct vec3d {
    float x;
    float y;
    float z;

    // Método para calcular o produto escalar
    float dot(const vec3d& other) const {
        return x * other.x + y * other.y + z * other.z;
    }
};

struct vec2d
{
	float x, y;
};

// Cria uma janela SFML
sf::RenderWindow window(sf::VideoMode(800, 600), "Triângulo SFML");

// Variáveis de posição e rotação
int width = 800 , height = 600;
int fov = 200;
float theta = 0.0f;
// Definir a distância do plano de projeção
float epsilon = 1e-5;
vec3d vrp = {40, 0.0,0.0};


//Função para projetar os pontos 3D para 2D
vec2d project3DTo2D(vec3d pos){
    

    // Calcular a proporção da tela para manter a perspectiva correta
    float aspect_ratio = width / height;

    // Aplicar a posição do cubo durante a projeção
    pos.x += vrp.x;
    pos.y += vrp.y;
    pos.z += vrp.z;

    // Verificar se o ponto está atrás do VRP
    if (pos.z == -fov)
        return vec2d{-1.0,-1.0};
    if (pos.z < -fov)
        return vec2d{-1.0,-1.0};

    // Calcular as coordenadas X e Y projetadas
    float x_proj = pos.x * fov / (pos.z + fov + epsilon);
    float y_proj = pos.y * fov / (pos.z + fov + epsilon);

    // Ajustar a posição na tela levando em conta o centro da tela
    x_proj += width / 2;
    y_proj += height / 2;
    //std::cout << "px:"<<pos.x<<" py:"<<pos.y<<" pz:"<<pos.z<<"| projX:"<<x_proj<<" projY:"<<y_proj<<std::endl;
    return vec2d{(x_proj), (y_proj)};
}



// Função para desenhar um cubo
void draw_cube(vec3d position,int size){
    
    // Definir os pontos do cubo
    vec3d points[8] = {
        vec3d{-1.0, -1.0, -1.0}, vec3d{1.0, -1.0, -1.0}, vec3d{1.0, 1.0, -1.0}, vec3d{-1.0, 1.0, -1.0},
        vec3d{-1.0, -1.0, 1.0}, vec3d{1.0, -1.0, 1.0}, vec3d{1.0, 1.0, 1.0}, vec3d{-1.0, 1.0, 1.0}
    };

    // Definir as faces do cubo como triângulos
    vec3d faces[12] = {
        vec3d{0, 1, 2}, vec3d{0, 2, 3},  // face frontal
        vec3d{3, 2, 6}, vec3d{3, 6, 7},  // face de trás
        vec3d{7, 6, 5}, vec3d{7, 5, 4},  // face superior
        vec3d{4, 5, 1}, vec3d{4, 1, 0},  // face inferior
        vec3d{1, 5, 6}, vec3d{1, 6, 2},  // face direita
        vec3d{4, 0, 3}, vec3d{4, 3, 7}   // face esquerda
    };




    // Aplicar a rotação do cubo em torno do eixo Y
    vec3d rotation_matrix[3] = {
        vec3d{cosf(theta), 0.0f, -sinf(theta)},
        vec3d{0.0f, 1.0f, 0.0f},
        vec3d{sinf(theta), 0.0f, cosf(theta)}
    };


    std::vector<vec3d> rotated_points;
    for (const auto& point : points) {
        vec3d rotated_point = {
            point.x * size ,
            point.y * size ,
            point.z * size 
        };
        // Aplicar a rotação multiplicando o ponto pela matriz de rotação
        rotated_point = {
          
            rotation_matrix[0].dot(rotated_point),
            rotation_matrix[1].dot(rotated_point),
            rotation_matrix[2].dot(rotated_point)
        };
        rotated_point = {
            position.x + rotated_point.x,
            position.y + rotated_point.y,
            position.z + rotated_point.z
        };
        rotated_points.push_back(rotated_point);
    };

    //# Desenhar as faces do cubo como triângulos
    for (const auto& face : faces) {
        
        std::vector<vec2d> projected_points;
        for (const auto& element : {face.x, face.y, face.z}) {
            vec2d projected_point = project3DTo2D(rotated_points[element]);
            //std::cout<< projected_point.x <<" , "<<projected_point.y<<std::endl;
            if (projected_point.x !=-1.0 && projected_point.y !=-1.0)
                projected_points.push_back(projected_point);
        };
        if (projected_points.size() == 3){
            sf::ConvexShape triangle;
            triangle.setPointCount(3);
            triangle.setPoint(0, sf::Vector2f(projected_points[0].x, projected_points[0].y)); // Define o primeiro ponto (topo)
            triangle.setPoint(1, sf::Vector2f(projected_points[1].x, projected_points[1].y)); // Define o segundo ponto (canto inferior esquerdo)
            triangle.setPoint(2, sf::Vector2f(projected_points[2].x, projected_points[2].y)); // Define o terceiro ponto (canto inferior direito)
            triangle.setFillColor(sf::Color::Red);
            window.draw(triangle);

        };
    };


}




int main()
{
    

    // Cria um objeto de triângulo
    
    // Loop principal
    while (window.isOpen())
    {


        // Processa eventos
        sf::Event event;
        while (window.pollEvent(event))
        {
            if (event.type == sf::Event::Closed)
                window.close();
        }
        // Capturar o estado das teclas pressionadas
        if (sf::Keyboard::isKeyPressed(sf::Keyboard::Left))
            vrp.x += 1.0f;
        if (sf::Keyboard::isKeyPressed(sf::Keyboard::Right))
            vrp.x -= 1.0f;
        if (sf::Keyboard::isKeyPressed(sf::Keyboard::Up))
            vrp.y += 1.0f;
        if (sf::Keyboard::isKeyPressed(sf::Keyboard::Down))
            vrp.y -= 1.0f;
        if (sf::Keyboard::isKeyPressed(sf::Keyboard::W))
            vrp.z -= 1.0f;
        if (sf::Keyboard::isKeyPressed(sf::Keyboard::S))
            vrp.z += 1.0f;

        // Limpa a janela
        window.clear(sf::Color(173, 216, 230));
        
        theta+=0.01f;
        //std::cout<<theta<<std::endl;
        // Desenha o triângulo na janela
        draw_cube(vec3d{40,0,0},50);

        // Mostra a janela
        window.display();
        sf::sleep(sf::milliseconds(1));
    }

    return 0;
}
