import ctypes
import os.path
from shader import Shader
import glfw
import numpy as np
from OpenGL.GL import *
import OpenGL.GL.shaders as gls

# vertices = [
#     [-0.8, -0.8, 1,1,0],
#     [0.0, -0.8, 1,1,0],
#     [-0.4, 0.0, 1,1,0],
#     [0.0, -0.8, 0,1,0],
#     [0.8, -0.8, 0,1,0],
#     [0.4, 0.0, 0,1,0],
#     [-0.4, 0.0, 0,0,1],
#     [0.4, 0.0, 0,0,1],
#     [0.0, 0.8, 0,0,1]
# ]

# vertices = [
#     [-0.8, -0.8, 1,0,0],
#     [0.0, -0.8, 1,1,0],
#     [0.8, -0.8, 0,1,0],
#     [-0.4, 0.0, 1,0,1],
#     [0.4, 0.0, 0,1,1],
#     [0.0, 0.8, 0,0,1],
# ]
#
# faces =[
#     [0,1,3],
#     [1,2,4],
#     [3,4,5]
# ]

vertices = [
    [-0.8,0.8],
    [0.8,-0.8],
    [0.8,0.8],
    [-0.8,-0.8]
]
faces = [
    [0,1,2],
    [0,1,3]
]
vaoId = 0 # New: Declare a VAO ID
#shaderId = 0
myShader = None

def init():
    global vertices, vaoId, myShader, faces
    glClearColor(1, 1, 1, 1)

    vertices_np = np.array(vertices, dtype=np.float32)

    # 1. Generate and bind VAO
    # A VAO stores the configuration of vertex attribute pointers
    # and the VBOs they refer to.
    vaoId = glGenVertexArrays(1)
    glBindVertexArray(vaoId)

    # 2. Generate and bind VBO
    # A VBO stores the actual vertex data.
    vboId = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vboId)

    # 3. Upload vertex data to VBO
    glBufferData(GL_ARRAY_BUFFER,
                 vertices_np.nbytes,
                 vertices_np,
                 GL_STATIC_DRAW)

    # 4. Specify vertex attribute pointers
    # This configuration is stored in the currently bound VAO (vaoId).
    # Attribute 0: position (2 floats)
    glVertexAttribPointer(0,
                          2,          # size (2 components for 2D position)
                          GL_FLOAT,   # type of components
                          GL_FALSE,   # normalized?
                          len(vertices[0]) * vertices_np.itemsize,      # stride (2 floats * 4 bytes/float)
                          ctypes.c_void_p(0)) # offset
    glVertexAttribPointer(1,
                          3,          # size (2 components for 2D position)
                          GL_FLOAT,   # type of components
                          GL_FALSE,   # normalized?
                          len(vertices[0]) * vertices_np.itemsize,      # stride (2 floats * 4 bytes/float)
                          ctypes.c_void_p(2*vertices_np.itemsize)) # offset
    faces_np = np.array(faces, dtype=np.uint32)
    eboId = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, eboId)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, faces_np.nbytes, faces_np, GL_STATIC_DRAW)

    glEnableVertexAttribArray(0)
    glEnableVertexAttribArray(1)

    # 5. Unbind VBO and VAO
    # It's good practice to unbind to avoid accidental modifications.
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)

    # with open('05_vertexShader.glsl','r') as file:
    #     vsSource = file.read()
    # with open('05_fragmentShader.glsl','r') as file:
    #     fsSource = file.read()

    # vsId = gls.compileShader(vsSource, GL_VERTEX_SHADER)
    # fsId = gls.compileShader(fsSource, GL_FRAGMENT_SHADER)
    # shaderId = gls.compileProgram(vsId, fsId)
    here = os.path.dirname(os.path.abspath(__file__))
    myShader = Shader(os.path.join(here,'05_vertexShader.glsl'),
                      os.path.join(here,'05_fragmentShader.glsl'))

def render():
    glClear(GL_COLOR_BUFFER_BIT)
    #glUseProgram(shaderId)
    # To draw, simply bind the VAO, and then make the draw call.
    # The VAO remembers all the VBOs and attribute configurations.
    myShader.bind()
    if glIsVertexArray(vaoId): # Check if it's a valid VAO
        glBindVertexArray(vaoId)
        # glDrawArrays(GL_TRIANGLES,
        #              0,
        #              len(vertices)) # Draw all vertices as a single set of triangles
        myShader.setUniform('color', 0,1,0)
        glDrawElements(GL_TRIANGLES,
                       len(faces[0]) * len(faces),
                       GL_UNSIGNED_INT,
                       None)
        glBindVertexArray(0)
    else:
        print("VAO is wrong or not generated correctly")
    myShader.unbind()

def keyboard(window, key, scancode, action, mods):
    if action == glfw.PRESS:
        if key == glfw.KEY_ESCAPE:
            glfw.set_window_should_close(window, True)

if __name__ == '__main__':
    print("Tests about openGL")
    if not glfw.init():
        print("Failed to initialize GLFW")
        exit()

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    # glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE) # Uncomment for macOS

    window = glfw.create_window(1000, 1000, '01-Intro', None, None)
    if not window:
        glfw.terminate()
        print("Failed to create GLFW window")
        exit()

    glfw.make_context_current(window)
    glfw.set_key_callback(window, keyboard)
    init()

    # Get and print any OpenGL errors after init
    error = glGetError()
    if error != GL_NO_ERROR:
        print(f"OpenGL error after init: {error}")

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

        # Get and print any OpenGL errors after render
        error = glGetError()
        if error != GL_NO_ERROR:
            print(f"OpenGL error during render loop: {error}")

    glfw.terminate()