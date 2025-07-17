import os.path

from src.GeometricFunctions import draw_3d_axis_on_chessboard
from src.PutImagesOnMarks import PutImagesOnMarks
from src.getFiducialLocation import getFiducialLocation
from src.CameraCalibration import calibrate_camera_from_images
import src.DataFunctions
import platform
from src.Config import parse_settings_file
import src.Model3DOperations

if __name__ == "__main__":
    Settings = parse_settings_file("config.yaml")
    if platform.system() == "Windows":
        print("Running on Windows")
    elif platform.system() == "Linux":
        print("Running on Linux")
    else:
        print(f"Running on unknown OS: {platform.system()}")
    if Settings["do fiducial mark"]:
        markImageName = os.path.join(Settings["directory fiducial image"], Settings["name fiducial image"])
        sourceImageName = os.path.join(Settings["directory 3d image"], Settings["name 3d image"])
        corners, ids, rejectedImgPoints = getFiducialLocation(markImageName)
        PutImagesOnMarks(ids, corners, sourceImageName, markImageName)

    if Settings["do calibration"]:
        resultado = calibrate_camera_from_images(Settings)  # ← chamada atualizada

        if resultado:
            camera_matrix, dist_coeffs, rvecs, tvecs = resultado
            rvecsnp = src.SaveData.concatenate_numpy_arrays_from_tuple(rvecs,1)
            tvecsnp = src.SaveData.concatenate_numpy_arrays_from_tuple(tvecs,1)
            calibration_data = {"camera_matrix":camera_matrix, "dist_coeffs": dist_coeffs, "rvecs": rvecsnp, "tvecs": tvecsnp}
            file_directory_name = os.path.join(Settings["directory data file"], Settings["data file name"])
            src.SaveData.save_multiple_numpy_to_yaml(calibration_data,file_directory_name)
            print("Calibração realizada com sucesso!")
        else:
            print("Calibração não foi bem sucedida.")
    if Settings["put 3D frame"]:
        image_location_name = os.path.join("fotosCalibration","teste1.jpeg")
        #draw_3d_axis_on_chessboard(image_location_name, Settings)
        file_directory_name = os.path.join("Models3D","Cubo1.obj")
        model_vertices, model_faces = src.Model3DOperations.load_blender_model(file_directory_name)
        src.Model3DOperations.draw_model(model_vertices, model_faces)