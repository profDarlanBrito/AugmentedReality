# Importar as bibliotecas
import cv2
import numpy as np

def PutImagesOnMarks(ids, corners, sourceImgName: str, MarkImgName: str):
    img = cv2.imread(MarkImgName)
    (imgH, imgW) = img.shape[:2]
    source = cv2.imread(sourceImgName)
    img = cv2.aruco.drawDetectedMarkers(img, corners, ids)
    ids = ids.flatten()
    refPts = []
    # loop over the IDs of the ArUco markers in top-left, top-right,
    # bottom-right, and bottom-left order
    for i in (0, 1, 3, 2):
        # grab the index of the corner with the current ID and append the
        # corner (x, y)-coordinates to our list of reference points
        j = np.squeeze(np.where(ids == i))
        corner = np.squeeze(corners[j])
        refPts.append(corner)

    # unpack our ArUco reference points and use the reference points to
    # define the *destination* transform matrix, making sure the points
    # are specified in top-left, top-right, bottom-right, and bottom-left
    # order
    (refPtTL, refPtTR, refPtBR, refPtBL) = refPts
    dstMat = [refPtTL[0], refPtTR[1], refPtBR[2], refPtBL[3]]
    dstMat = np.array(dstMat)
    # grab the spatial dimensions of the source image and define the
    # transform matrix for the *source* image in top-left, top-right,
    # bottom-right, and bottom-left order
    (srcH, srcW) = source.shape[:2]
    srcMat = np.array([[0, 0], [srcW, 0], [srcW, srcH], [0, srcH]])
    # compute the homography matrix and then warp the source image to the
    # destination based on the homography
    (H, _) = cv2.findHomography(srcMat, dstMat)
    warped = cv2.warpPerspective(source, H, (imgW, imgH))
    # construct a mask for the source image now that the perspective warp
    # has taken place (we'll need this mask to copy the source image into
    # the destination)
    mask = np.zeros((imgH, imgW), dtype="uint8")
    cv2.fillConvexPoly(mask, dstMat.astype("int32"), (255, 255, 255),
                       cv2.LINE_AA)
    # this step is optional, but to give the source image a black border
    # surrounding it when applied to the source image, you can apply a
    # dilation operation
    rect = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    mask = cv2.dilate(mask, rect, iterations=2)
    # create a three channel version of the mask by stacking it depth-wise,
    # such that we can copy the warped source image into the input image
    maskScaled = mask.copy() / 255.0
    maskScaled = np.dstack([maskScaled] * 3)
    # copy the warped source image into the input image by (1) multiplying
    # the warped image and masked together, (2) multiplying the original
    # input image with the mask (giving more weight to the input where
    # there *ARE NOT* masked pixels), and (3) adding the resulting
    # multiplications together
    warpedMultiplied = cv2.multiply(warped.astype("float"), maskScaled)
    imageMultiplied = cv2.multiply(img.astype(float), 1.0 - maskScaled)
    output = cv2.add(warpedMultiplied, imageMultiplied)
    output = output.astype("uint8")
    # show the input image, source image, output of our augmented reality
    cv2.imshow("Input", img)
    cv2.imshow("Source", source)
    cv2.imshow("OpenCV AR Output", output)
    cv2.waitKey(0)