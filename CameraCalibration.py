# function to calibrate the camera
import cv2
import numpy as np

def calibrate_camera_from_video(video_path, chessboard_size, square_size):
    # define the termination criteria for the calibration
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    # this assumes an 8x6 chessboard with each square being unit size
    #objp = np.zeros((6 * 8, 3), np.float32)
    #objp[:, :2] = np.mgrid[0:8, 0:6].T.reshape(-1, 2)

    objp = np.zeros((22*15, 3), np.float32)
    objp[:, :2] = np.mgrid[0:22, 0:15].T.reshape(-1, 2)


    # Arrays to store object points and image points from all images
    objpoints = []  # 3d point in real world space
    imgpoints = []  # 2d points in image plane.

    """
    Calibrates the camera from a video of a chessboard target.

    Args:
        video_path (str): The path to the video file.
        chessboard_size (tuple): The number of inner corners of the chessboard (width, height).
        square_size (float): The size of each square on the chessboard in units (e.g., mm).

    Returns:
        tuple: A tuple containing the camera matrix, distortion coefficients,
               rotation vectors, and translation vectors.
               Returns None if calibration fails.
    """
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Error: Could not open video file {video_path}")
        return None

    # Update objp based on the actual chessboard size
    objp = np.zeros((chessboard_size[0]*chessboard_size[1], 3), np.float32)
    objp[:,:2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2)
    objp = objp * square_size
    
    # -Frames/s
    fps = cap.get(cv2.CAP_PROP_FPS)
    max_seconds = 5
    max_frames = int(fps * max_seconds)

    frame_count = 0
    while(cap.isOpened()):
        ret, frame = cap.read()
        if not ret or frame_count >= max_frames:
            break

        frame_count += 1
        print(f"Processing frame {frame_count}")

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Find the chessboard corners
        ret, corners = cv2.findChessboardCorners(gray, chessboard_size, None)

        # If found, add object points, image points (after refining them)
        if ret == True:
            objpoints.append(objp)

            corners2 = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
            imgpoints.append(corners2)

            # Draw and display the corners (optional, for visualization)
            # cv2.drawChessboardCorners(frame, chessboard_size, corners2, ret)
            # cv2.imshow('img', frame)
            # cv2.waitKey(10) # Wait for 10ms to see the frame

    cap.release()
    # cv2.destroyAllWindows() # Uncomment if you were displaying frames

    if len(objpoints) == 0:
        print("No chessboard corners found in any frame. Calibration failed.")
        return None

    # Calibrate the camera
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

    if ret:
        print("Camera calibration successful.")
        print("Camera matrix:\n", mtx)
        print("Distortion coefficients:\n", dist)
        return mtx, dist, rvecs, tvecs
    else:
        print("Camera calibration failed.")
        return None

# Example usage:
# Replace 'path/to/your/video.mp4' with the actual path to your video file.
# Replace (8, 6) with the actual number of inner corners of your chessboard (width, height).
# Replace 25.0 with the actual size of one square on your chessboard in millimeters or desired units.
# calibration_result = calibrate_camera_from_video('path/to/your/video.mp4', (8, 6), 25.0)

# if calibration_result:
#     camera_matrix, dist_coeffs, rvecs, tvecs = calibration_result
#     # You can now use camera_matrix and dist_coeffs for undistorting images or other tasks.
