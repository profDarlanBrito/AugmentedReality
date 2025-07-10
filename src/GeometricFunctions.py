import os.path

import cv2
import numpy as np
import matplotlib.pyplot as plt
from dask.array import square

import src.DataFunctions


def draw_3d_axis_on_chessboard(image_path, Settings: dict):
    """
    Desenha um sistema de eixos coordenados 3D sobre um tabuleiro de xadrez
    em uma imagem usando OpenCV.

    Args:
        image_path (str): Caminho para a imagem do tabuleiro de xadrez.
        pattern_size (tuple): Número de cantos internos (largura, altura) do tabuleiro.
                              Ex: (7, 7) para um tabuleiro 8x8.
        square_size (float): Tamanho de um quadrado do tabuleiro em alguma unidade (e.g., cm, mm).
                             Isso define a escala do sistema de coordenadas 3D.
    """
    # 1. Carregar a imagem
    img = cv2.imread(image_path)
    if img is None:
        print(f"Erro: Não foi possível carregar a imagem em {image_path}")
        return

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 2. Definir os pontos do objeto 3D (cantos do tabuleiro no espaço 3D)
    # Estes são os pontos no sistema de coordenadas do mundo.
    # Assumimos que o tabuleiro está no plano Z=0.
    pattern_size = Settings["checkerboard size"]
    square_size = Settings["square size"]
    objp = np.zeros((pattern_size[0] * pattern_size[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:pattern_size[0], 0:pattern_size[1]].T.reshape(-1, 2) * square_size

    # 3. Encontrar os cantos do tabuleiro na imagem 2D
    ret, corners = cv2.findChessboardCorners(gray, pattern_size, None)

    if ret == True:
        # Aprimorar a precisão dos cantos sub-pixel
        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1),
                                    criteria=(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001))

        # 4. Definir parâmetros intrínsecos da câmera (exemplo - idealmente vêm de calibração)
        # Se você calibrou sua câmera, use seus próprios valores aqui!
        # Estes são valores de exemplo para demonstração.
        h, w = gray.shape
        # Matriz da Câmera (K)
        camera_matrix = np.array([
            [w * 0.8, 0, w / 2],  # fx, 0, cx
            [0, h * 0.8, h / 2],  # 0, fy, cy
            [0, 0, 1]             # 0, 0, 1
        ], dtype=np.float32)
        # Coeficientes de Distorção (D)
        dist_coeffs = np.zeros((5, 1), dtype=np.float32) # Assumindo sem distorção significativa para o exemplo
        filename = os.path.join(Settings["directory data file"], Settings["data file name"])
        listArrays = src.DataFunctions.load_multiple_numpy_from_yaml(filename)
        # converter o listarrays para cada matrix
        print("Matriz da Câmera de Exemplo:\n", camera_matrix)
        print("Coeficientes de Distorção de Exemplo:\n", dist_coeffs)

        # 5. Calcular a pose da câmera (rvec e tvec) usando solvePnP
        # solvePnP encontra a rotação (rvec) e translação (tvec) do sistema
        # de coordenadas do mundo para o sistema de coordenadas da câmera.
        ret, rvec, tvec = cv2.solvePnP(objp, corners2, camera_matrix, dist_coeffs)

        # 6. Definir os pontos do eixo 3D para projeção
        # Os eixos X, Y e Z se estenderão a partir do primeiro canto do tabuleiro (origem).
        # A escala dos eixos é definida pelo square_size.
        axis_points = np.float32([[0, 0, 0], [square_size*3, 0, 0],
                                  [0, square_size*3, 0], [0, 0, -square_size*3]]).reshape(-1, 3)

        # 7. Projetar os pontos do eixo 3D na imagem 2D
        # projectPoints transforma os pontos 3D (da origem e ao longo dos eixos)
        # em coordenadas 2D na imagem, usando a pose calculada.
        imgpts, jac = cv2.projectPoints(axis_points, rvec, tvec, camera_matrix, dist_coeffs)

        # 8. Desenhar os eixos projetados na imagem
        # A origem é o primeiro canto do tabuleiro (index 0 de imgpts).
        # Os pontos do eixo são imgpts[1] (X), imgpts[2] (Y), imgpts[3] (Z).
        origin_x, origin_y = int(imgpts[0][0][0]), int(imgpts[0][0][1])

        # Eixo X (vermelho)
        cv2.line(img, (origin_x, origin_y),
                 (int(imgpts[1][0][0]), int(imgpts[1][0][1])), (0, 0, 255), 5)
        # Eixo Y (verde)
        cv2.line(img, (origin_x, origin_y),
                 (int(imgpts[2][0][0]), int(imgpts[2][0][1])), (0, 255, 0), 5)
        # Eixo Z (azul - apontando para fora da imagem se positivo, para dentro se negativo)
        # Note que a convenção padrão do OpenCV para Z é para fora da câmera,
        # mas aqui estamos usando -square_size*3 para apontar "para cima" na visão do tabuleiro.
        cv2.line(img, (origin_x, origin_y),
                 (int(imgpts[3][0][0]), int(imgpts[3][0][1])), (255, 0, 0), 5)

        # Opcional: Desenhar os cantos detectados para depuração
        # cv2.drawChessboardCorners(img, pattern_size, corners2, ret)

        # 9. Mostrar a imagem com os eixos
        plt.figure(figsize=(10, 8))
        plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        plt.title('Tabuleiro com Eixos Coordenados 3D')
        plt.axis('off')
        plt.show()

    else:
        print("Não foi possível encontrar os cantos do tabuleiro. Verifique o caminho da imagem e o pattern_size.")

# --- Uso do programa ---
if __name__ == "__main__":
    # Certifique-se de ter uma imagem de tabuleiro de xadrez no mesmo diretório
    # ou forneça o caminho completo para a imagem.
    # Exemplo: 'chessboard.jpg'
    # Você pode baixar uma imagem de tabuleiro de xadrez online ou usar a sua.
    # Exemplo de imagem para usar: https://www.researchgate.net/profile/Irfan-Shahzad/publication/339460281/figure/fig2/AS:859942730248194@1582046944641/Example-of-Chess-Board-A-7x7-checkerboard-pattern-is-shown.png
    # Salve-a como 'chessboard_example.png'
    image_file = 'chessboard_example.png'
    # pattern_size = (largura, altura) do NÚMERO DE CANTOS INTERNOS
    # Um tabuleiro 8x8 tem 7x7 cantos internos.
    # square_size = tamanho de cada quadrado do tabuleiro em unidades arbitrárias
    # (isso afeta o comprimento dos eixos no sistema 3D).
    draw_3d_axis_on_chessboard(image_file, pattern_size=(7, 7), square_size=1.0)