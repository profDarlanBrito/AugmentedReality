# Importar as bibliotecas
from typing import Any, Sequence

import cv2
import numpy as np
from cv2 import Mat, typing
from numpy import ndarray, dtype, generic


def getFiducialLocation(ImageName: str) -> tuple[Sequence[cv2.typing.MatLike], cv2.typing.MatLike, Sequence[cv2.typing.MatLike]]:
    # Carregar a imagem (substitua 'imagem.jpg' pelo caminho da sua imagem)
    # Você pode fazer upload da imagem ou usar um caminho de arquivo
    # Exemplo de upload:
    # from google.colab import files
    # uploaded = files.upload()
    # for filename in uploaded.keys():
    #   img = cv2.imread(filename)

    # Exemplo de leitura de um arquivo local no Colab (se a imagem já estiver lá)
    try:
        img = cv2.imread(ImageName)
        if img is None:
            raise FileNotFoundError("imagem.jpg not found.")
    except FileNotFoundError as e:
        print(f"Erro: {e}")
        print("Por favor, faça upload de uma imagem ou substitua 'imagem.jpg' pelo caminho correto.")
        # Criar uma imagem de placeholder caso a imagem não seja encontrada
        img = np.zeros((300, 400, 3), dtype=np.uint8)
        cv2.putText(img, "Imagem nao encontrada!", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)


    if img is not None:
        # Converter a imagem para tons de cinza
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Definir o detector de AprilTag
        # Substitua "DICT_APRILTAG_36h11" pelo dicionário que você está usando
        # Outras opções incluem: DICT_APRILTAG_16h5, DICT_APRILTAG_25h9, DICT_APRILTAG_36h10, DICT_ARUCO_ORIGINAL
        aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_APRILTAG_36h11)
        aruco_params = cv2.aruco.DetectorParameters()
        detector = cv2.aruco.ArucoDetector(aruco_dict, aruco_params)


        # Detectar AprilTags na imagem
        corners, ids, rejectedImgPoints = detector.detectMarkers(gray)

        # Desenhar os marcadores detectados na imagem original
        if ids is not None:
            print("AprilTags detectadas com IDs:", ids)
        else:
            print("Nenhuma AprilTag detectada.")

        # Exibir a imagem com os marcadores detectados
        #cv2.imshow('Fiducial Mark',img)
        #cv2.waitKey(0)
    return corners, ids, rejectedImgPoints