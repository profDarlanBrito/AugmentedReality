from PutImagesOnMarks import PutImagesOnMarks
from getFiducialLocation import getFiducialLocation
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