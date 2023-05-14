import cv2
import numpy as np
import utils

###########
path = "2.jpg"

############
widthImg = 700
heightImg = 700
img = cv2.imread(path)

# Image preprocessing
img = cv2.resize(img, (widthImg, heightImg))
imageCountours = img.copy()
imageBiggestCountours = img.copy()

imgGrey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # makes image grey
imgBlur = cv2.GaussianBlur(imgGrey, (5, 5), 1)  # makes image blur
imgCanny = cv2.Canny(imgBlur, 10, 50)  # makes image canny

# Defining all countours
countours, hierarchy = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
cv2.drawContours(imageCountours, countours, -1, (0, 255, 0), 10)

# Finding rectangles
rectCon = utils.rectCountour(countours)  # find us the biggest box
biggestCountor = utils.getCornerPoints(rectCon[0])  # get us the corner points of the biggest box
gradePoints = utils.getCornerPoints(rectCon[1])
# namePoints = utils.getCornerPoints(rectCon[2])

# print(biggestCountor)


# this draws the countors of 2 biggest boxes
if biggestCountor.size != 0 and gradePoints.size != 0:
    cv2.drawContours(imageBiggestCountours, biggestCountor, -1, (0, 255, 0), 20)
    cv2.drawContours(imageBiggestCountours, gradePoints, -1, (0, 0, 255), 20)

    biggestCountor = utils.reorder(biggestCountor)
    gradePoints = utils.reorder(gradePoints)

    pt1 = np.float32(biggestCountor)
    pt2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
    matrix = cv2.getPerspectiveTransform(pt1, pt2)
    imageWarpColored = cv2.warpPerspective(img,matrix,(widthImg,heightImg))

imgBlank = np.zeros_like(img)
imageArray = ([img, imgGrey, imgBlur, imgCanny], [imageCountours, imageBiggestCountours, imageWarpColored, imgBlank])
imageStacked = utils.stackImages(imageArray, 0.5)

cv2.imshow("Stacked Images", imageStacked)
cv2.waitKey(0)
