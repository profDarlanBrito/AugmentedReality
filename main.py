from PutImagesOnMarks import PutImagesOnMarks
from getFiducialLocation import getFiducialLocation

if __name__ == "__main__":
    markImageName = './images/FiducialMarkA4DifferentIDs.png'
    sourceImageName = './images/eu.jpg'
    corners, ids, rejectedImgPoints = getFiducialLocation(markImageName)
    PutImagesOnMarks(ids, corners, sourceImageName, markImageName)