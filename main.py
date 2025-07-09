from src.PutImagesOnMarks import PutImagesOnMarks
from src.getFiducialLocation import getFiducialLocation
from src.CameraCalibration import calibrate_camera_from_images
import platform
from src.Config import parse_settings_file

if __name__ == "__main__":
    Settings = parse_settings_file("../config.yaml")
    if platform.system() == "Windows":
        Settings["calibration folder"] = "../" + Settings["calibration folder"]
        print("Running on Windows")
    elif platform.system() == "Linux":
        print("Running on Linux")
    else:
        print(f"Running on unknown OS: {platform.system()}")
    if Settings["do fiducial mark"]:
        markImageName = './Images/FiducialMarkA4DifferentIDsSmall.png'
        sourceImageName = './Images/eu.jpg'
        corners, ids, rejectedImgPoints = getFiducialLocation(markImageName)
        PutImagesOnMarks(ids, corners, sourceImageName, markImageName)

    if Settings["do calibration"]:
        resultado = calibrate_camera_from_images(Settings)  # ← chamada atualizada

        if resultado:
            camera_matrix, dist_coeffs, rvecs, tvecs = resultado
            print("Calibração realizada com sucesso!")
        else:
            print("Calibração não foi bem sucedida.")
