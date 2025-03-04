#include <iostream>
#include <./glad/glad.h>
#include <./GLFW/glfw3.h>

int main() {

    // Initializes glfw
    glfwInit();

    // Tells glfw what versions to run
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);

    // Tells glfw what package/profile to use in the program (core in this case)
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

    // Creates window object for OpenGL
    GLFWwindow* window = glfwCreateWindow(800, 800, "General Relativity Simulation", NULL, NULL);

    // Error checking
    if (window == NULL) {
        std::cout << "Failed to create GLFW window" << std::endl;
        glfwTerminate();
        return -1;
    }

    // Introduce window to current context
    glfwMakeContextCurrent(window);

    // Makes OpenGL window stay until it closes
    while (!glfwWindowShouldClose(window)) {
        glfwPollEvents();
    }

    glfwDestroyWindow(window); // Destroys glfw window
    glfwTerminate(); // Ends glfw when desired

    return 0;

}