import OpenGL.GL.shaders as gls
from OpenGL.GL import *


class Shader:
    def __init__(self, vertexShaderFileName, fragmentShaderFileName):
        with open(vertexShaderFileName, 'r') as file:
            vsSource = file.read()
        with open(fragmentShaderFileName, 'r') as file:
            fsSource = file.read()

        vsId = gls.compileShader(vsSource, GL_VERTEX_SHADER)
        fsId = gls.compileShader(fsSource, GL_FRAGMENT_SHADER)
        self.shaderId = gls.compileProgram(vsId, fsId)

    def bind(self):
        glUseProgram(self.shaderId)

    def unbind(self):
        glUseProgram(0)

    def setUniform(self,name,x,y=None,z=None,w=None):
        name_loc = glGetUniformLocation(self.shaderId, name)
        if y is None:
            glUniform1f(name_loc, x)
        elif z is None:
            glUniform2f(name_loc, x, y)
        elif w is None:
            glUniform3f(name_loc, x, y, z)
        else:
            glUniform4f(name_loc, x, y, z, w)