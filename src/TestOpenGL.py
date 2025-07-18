from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import pywavefront

# Variáveis globais
model = None
rotation_y = 0.0

def load_model(file_path):
    """Carrega o modelo 3D de um arquivo .obj."""
    global model
    try:
        model = pywavefront.Wavefront(file_path, collect_faces=True)
        print(f"Modelo {file_path} carregado com sucesso!")
    except Exception as e:
        print(f"Erro ao carregar o modelo: {e}")
        model = None

def init_gl():
    """Inicializa as configurações do OpenGL."""
    glClearColor(0.2, 0.2, 0.2, 1.0)  # Cor de fundo cinza escuro
    glEnable(GL_DEPTH_TEST)  # Habilita o teste de profundidade para renderização 3D
    glEnable(GL_LIGHTING)    # Habilita a iluminação
    glEnable(GL_LIGHT0)      # Habilita a luz 0
    glLightfv(GL_LIGHT0, GL_POSITION, [1.0, 1.0, 1.0, 0.0]) # Posição da luz
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])   # Cor difusa da luz

def display():
    """Função de callback para desenhar na tela."""
    global rotation_y
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(0, 0, 5, 0, 0, 0, 0, 1, 0) # Posição da câmera (olho, centro, cima)

    glRotatef(rotation_y, 0.5, 1, 0) # Rotaciona o modelo em torno do eixo Y

    if model:
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_NORMAL_ARRAY)

        for name, material in model.materials.items():
            glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, material.ambient)
            glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, material.diffuse)
            glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, material.specular)
            shininess = material.shininess/255*128
            glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, shininess)

            glPushMatrix()
            # Ajuste a escala e a translação do modelo conforme necessário
            # Exemplo: glScalef(0.1, 0.1, 0.1)
            # Exemplo: glTranslatef(0.0, -1.0, 0.0)

            glBegin(GL_TRIANGLES)
            for face in model.mesh_list[0].faces:
                for vertex_id in face:
                    # Verifica se o índice do vértice é válido para as normais e vértices
                    if vertex_id < len(model.parser.normals) and vertex_id < len(material.vertices):
                        glNormal3f(*model.parser.normals[vertex_id])
                        glVertex3f(*model.vertices[vertex_id])
            glEnd()
            glPopMatrix()

        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_NORMAL_ARRAY)

    glutSwapBuffers()

def reshape(width, height):
    """Função de callback para redimensionar a janela."""
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, (width / height), 0.1, 50.0) # Ângulo de visão, proporção, near, far
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def animate(value):
    """Função de callback para animação."""
    global rotation_y
    rotation_y += 1.0 # Incrementa a rotação
    if rotation_y > 360:
        rotation_y -= 360
    glutPostRedisplay() # Solicita um redesenho da tela
    glutTimerFunc(50, animate, 0) # Chama a função novamente após 50ms

def keyboard_input(key, x, y):
    """Função de callback para entrada do teclado."""
    if key == b'\x1b': # Tecla ESC
        glutLeaveMainLoop() # Sai do loop principal do GLUT


if __name__ == "__main__":
    # --- Configuração do Modelo ---
    model_path = os.path.join("../Models3D","Plane.obj")  # <--- Altere para o caminho do seu modelo .obj
    load_model(model_path)

    if model is None:
        print("Não foi possível carregar o modelo. Saindo.")
        exit()

    # --- Configuração do GLUT ---
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"Visualizador de Modelo 3D Simples")

    init_gl()

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard_input)
    glutTimerFunc(50, animate, 0) # Inicia a animação

    glutMainLoop()
