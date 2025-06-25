from PutImagesOnMarks import PutImagesOnMarks
from getFiducialLocation import getFiducialLocation
from CameraCalibration import calibrate_camera_from_video
import platform

if __name__ == "__main__":
    if platform.system() == "Windows":
        print("Running on Windows")
    elif platform.system() == "Linux":
        print("Running on Linux")
    else:
        print(f"Running on unknown OS: {platform.system()}")
    #markImageName = './Images/FiducialMarkA4DifferentIDsSmall.png'
    #sourceImageName = './Images/eu.jpg'
    #corners, ids, rejectedImgPoints = getFiducialLocation(markImageName)
    #PutImagesOnMarks(ids, corners, sourceImageName, markImageName)

      # Parâmetros para calibração
    video_path = './videos/teste.mp4'  # ajuste o caminho para seu vídeo
    chessboard_size = (22, 15)  # tamanho do tabuleiro (número de cantos internos)
    square_size = 1.0  # tamanho do quadrado, em mm ou unidades que você usar

    resultado = calibrate_camera_from_video(video_path, chessboard_size, square_size)

    if resultado:
        camera_matrix, dist_coeffs, rvecs, tvecs = resultado
        print("Calibração realizada com sucesso!")
    else:
        print("Calibração não foi bem sucedida.")