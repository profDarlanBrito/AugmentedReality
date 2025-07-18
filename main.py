import os
import platform

from src.GeometricFunctions import draw_3d_axis_on_chessboard
from src.PutImagesOnMarks import PutImagesOnMarks
from src.getFiducialLocation import getFiducialLocation
from src.CameraCalibration import calibrate_camera_from_images
from src.Config import parse_settings_file
import src.Model3DOperations

if __name__ == "__main__":
    # Carrega configurações do arquivo
    Settings = parse_settings_file("config.yaml")

    print(f"Running on {platform.system()}")

    # --- Etapa 1: Marcação Fiducial ---
    if Settings.get("do fiducial mark"):
        mark_image_name = os.path.join(Settings["directory fiducial image"], Settings["name fiducial image"])
        source_image_name = os.path.join(Settings["directory 3d image"], Settings["name 3d image"])
        corners, ids, rejected_img_points = getFiducialLocation(mark_image_name)
        PutImagesOnMarks(ids, corners, source_image_name, mark_image_name)

    # --- Etapa 2: Calibração da câmera ---
    if Settings.get("do calibration"):
        resultado = calibrate_camera_from_images(Settings)
        if resultado:
            camera_matrix, dist_coeffs, rvecs, tvecs = resultado
            rvecs_np = src.SaveData.concatenate_numpy_arrays_from_tuple(rvecs, axis=1)
            tvecs_np = src.SaveData.concatenate_numpy_arrays_from_tuple(tvecs, axis=1)

            calibration_data = {
                "camera_matrix": camera_matrix,
                "dist_coeffs": dist_coeffs,
                "rvecs": rvecs_np,
                "tvecs": tvecs_np
            }

            file_directory_name = os.path.join(Settings["directory data file"], Settings["data file name"])
            src.SaveData.save_multiple_numpy_to_yaml(calibration_data, file_directory_name)
            print("Calibração realizada com sucesso!")
        else:
            print("Calibração não foi bem-sucedida.")

    # --- Etapa 3: Exibir modelo 3D ---
    if Settings.get("put 3D frame"):
        file_directory_name = os.path.join("Models3D", "Cubo1.obj")  # Ajuste para outro modelo, se necessário
        model_vertices, model_faces = src.Model3DOperations.load_blender_model(file_directory_name)

        # Nova função com pyglet
        src.Model3DOperations.run_pyglet_window(model_vertices, model_faces)