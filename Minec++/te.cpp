#include <iostream>

struct vec3d {
    float x, y, z;
};

int main() {
    vec3d myVec3d = {1.0, 2.0, 3.0};

    // Iterando sobre os elementos do vec3d
    for (const auto& element : {myVec3d.x, myVec3d.y, myVec3d.z}) {
        std::cout << element << " cu ";
    }
    std::cout << std::endl;

    return 0;
}