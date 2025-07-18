import pyglet
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

def load_blender_model(filePathName: str):
    vertices = []
    faces = []
    try:
        with open(filePathName, 'r') as f:
            for line in f:
                if line.startswith('v '):
                    vertices.append(list(map(float, line.split()[1:4])))
                elif line.startswith('f '):
                    faces.append([int(v.split('/')[0]) - 1 for v in line.split()[1:]])
        model_vertices = np.array(vertices, dtype=np.float32)
        print(f"Loaded model with {len(model_vertices)} vertices and {len(faces)} faces.")
    except FileNotFoundError:
        print(f"Error: Model file not found at {filePathName}")
        exit()
    return model_vertices, faces

def draw_model(model_vertices, model_faces):
    glColor3f(1.0, 0.5, 0.0)  # cor laranja
    for face in model_faces:
        glBegin(GL_POLYGON)
        for vertex_idx in face:
            glVertex3fv(model_vertices[vertex_idx])
        glEnd()

def setup_projection(width, height): #FUNÇÃO COM ERRO RESIDUAL
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, width / float(height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def run_pyglet_window(model_vertices, model_faces):
    window = pyglet.window.Window(800, 600, "3D Model Viewer", resizable=True)

    # Habilita teste de profundidade
    glEnable(GL_DEPTH_TEST)

    # Inicializa projeção
    setup_projection(window.width, window.height)

    @window.event
    def on_resize(width, height):
        glViewport(0, 0, width, height)
        setup_projection(width, height)

    @window.event
    def on_draw():
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        # Move e rotaciona a câmera
        glTranslatef(0.0, 0.0, -5.0)
        glRotatef(30, 1, 0, 0)
        glRotatef(30, 0, 1, 0)
        draw_model(model_vertices, model_faces)

    pyglet.app.run()
