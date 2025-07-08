from PutImagesOnMarks import PutImagesOnMarks
from getFiducialLocation import getFiducialLocation
from CameraCalibration import calibrate_camera_from_images
import platform

if __name__ == "__main__":
    if platform.system() == "Windows":
        print("Running on Windows")
    elif platform.system() == "Linux":
        print("Running on Linux")
    else:
        print(f"Running on unknown OS: {platform.system()}")

    markImageName = './Images/FiducialMarkA4DifferentIDsSmall.png'
    sourceImageName = './Images/eu.jpg'
    corners, ids, rejectedImgPoints = getFiducialLocation(markImageName)
    PutImagesOnMarks(ids, corners, sourceImageName, markImageName)

    # Parâmetros para calibração com imagens
    chessboard_size = (8, 6)  # número de cantos internos (largura, altura)
    square_size = 25.0  # tamanho real de cada quadrado (em mm, cm ou unidade arbitrária)
    
    resultado = calibrate_camera_from_images(chessboard_size, square_size)  # ← chamada atualizada

    if resultado:
        camera_matrix, dist_coeffs, rvecs, tvecs = resultado
        print("Calibração realizada com sucesso!")
    else:
        print("Calibração não foi bem sucedida.")
