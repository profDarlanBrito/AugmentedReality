import cv2
import numpy as np
import OpenGL.GL as gl
import OpenGL.GLUT as glut
import OpenGL.GLU as glu
from mypyc.crash import catch_errors


def load_blender_model(filePathName:str):
    """
    Simple OBJ loader - you'd need a more robust one for complex models.
    This is just to demonstrate loading vertices and faces.
    """
    vertices = []
    faces = []
    try:
        with open(filePathName, 'r') as f:
            for line in f:
                if line.startswith('v '):
                    vertices.append(list(map(float, line.split()[1:4])))
                elif line.startswith('f '):
                    # OBJ faces can be 1-indexed, handle accordingly
                    faces.append([int(v.split('/')[0]) - 1 for v in line.split()[1:]])
        model_vertices = np.array(vertices, dtype=np.float32)
        model_faces = np.array(faces, dtype=np.int32)
        print(f"Loaded model with {len(model_vertices)} vertices and {len(model_faces)} faces.")
    except FileNotFoundError:
        print(f"Error: Model file not found at {filePathName}")
        exit()
    return model_vertices, model_faces
def draw_model(model_vertices, model_faces):
    """
    Draws the loaded 3D model using OpenGL.
    Assumes model_vertices and model_faces are populated.
    """
    if not model_vertices.size > 0 and not model_faces > 0:
        return
    try:
        gl.glBegin(gl.GL_QUADS)
    except:
        print("Error")
    gl.glColor3f(1.0, 0.5, 0.0) # Orange color for the model
    for face in model_faces:
        for vertex_idx in face:
            gl.glVertex3fv(model_vertices[vertex_idx])
    gl.glEnd()
