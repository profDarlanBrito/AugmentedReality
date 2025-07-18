import pyglet
import pywavefront
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

def load_blender_model(filePathName: str):
    try:
        model = pywavefront.Wavefront(filePathName, collect_faces=True)
        print(f"Modelo {filePathName} carregado com sucesso!")
    except Exception as e:
        print(f"Erro ao carregar o modelo: {e}")
        model = None
    return model
