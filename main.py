import cv2
import numpy as np
import utils

###########
path = "1.jpg"

############
widthImg = 700
heightImg = 700
questions = 5
choices = 5
ans = [1, 2, 0, 1, 4]
webCamFeed = True
cameraNo = 0
#####################

# setting up the camera
cap = cv2.VideoCapture(cameraNo)
cap.set(10, 150)

while True:
    if webCamFeed:
        success, img = cap.read()
    else:
        img = cv2.imread(path)

    # Image preprocessing
    img = cv2.resize(img, (widthImg, heightImg))
    imageCountours = img.copy()
    imageBiggestCountours = img.copy()
    imgFinal = img.copy()
    imgGrey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # makes image grey
    imgBlur = cv2.GaussianBlur(imgGrey, (5, 5), 1)  # makes image blur
    imgCanny = cv2.Canny(imgBlur, 10, 50)  # makes image canny

    try:

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

            # for the mcqs
            pt1 = np.float32(biggestCountor)
            pt2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
            matrix = cv2.getPerspectiveTransform(pt1, pt2)
            imageWarpColored = cv2.warpPerspective(img, matrix, (widthImg, heightImg))

            # for the grades
            ptG1 = np.float32(gradePoints)
            ptG2 = np.float32([[0, 0], [325, 0], [0, 150], [325, 150]])
            matrixG = cv2.getPerspectiveTransform(ptG1, ptG2)
            imageGradeDisplay = cv2.warpPerspective(img, matrixG, (325, 150))
            # cv2.imshow("Grade",imageGradeDisplay)

            # Applying threshold (byshoof el marked spots)
            imgWarpGray = cv2.cvtColor(imageWarpColored, cv2.COLOR_BGR2GRAY)
            imgThresh = cv2.threshold(imgWarpGray, 180, 225, cv2.THRESH_BINARY_INV)[1]

            boxes = utils.splitBoxes(imgThresh)
            # print(cv2.countNonZero(boxes[1]))

            # getting non zero pixel values of each box
            # btgebly el value bta3 el shaded parts, law heya shaded el value byb2a higher
            myPixelVal = np.zeros((questions, choices))
            countC = 0
            countR = 0

            for image in boxes:
                totalPixels = cv2.countNonZero(image)
                myPixelVal[countR][countC] = totalPixels
                countC += 1
                if countC == choices:
                    countR += 1
                    countC = 0
            # print(myPixelVal)

            # el function deh bt7dd el answers ely mtzlla

            # Finding index values of the markings
            myIndex = []
            for x in range(0, questions):
                arr = myPixelVal[x]
                myIndexVal = np.where(arr == np.amax(arr))
                myIndex.append(myIndexVal[0][0])


            # Grading, 3lshan ashoof el egabat ely sa7
            grading = []
            for x in range(0, questions):
                if ans[x] == myIndex[x]:
                    grading.append(1)
                else:
                    grading.append(0)
            # print(grading)

            score = (sum(grading) / questions) * 100  # Final grade
            print(score)

            imageResults = imageWarpColored.copy()
            # Displaying answers
            imageResults = utils.showAnswers(imageResults, myIndex, grading, ans, questions, choices)
            imageRawDrawing = np.zeros_like(imageWarpColored)
            imageRawDrawing = utils.showAnswers(imageRawDrawing, myIndex, grading, ans, questions,
                                                choices)  # b5ly el black screen 3aleha el egabat

            # Ha7ot el final egabat, feh awal sora 5ales
            Invmatrix = cv2.getPerspectiveTransform(pt2, pt1)
            ImageInvWarp = cv2.warpPerspective(imageRawDrawing, Invmatrix, (widthImg, heightImg))



            # hazwed el grade
            imageRawGrade = np.zeros_like(imageGradeDisplay)
            cv2.putText(imageRawGrade, str(int(score)) + "%", (50, 100), cv2.FONT_HERSHEY_COMPLEX, 3, (0, 255, 255), 3)
            InvmatrixG = cv2.getPerspectiveTransform(ptG2, ptG1)
            imgInvGradeDisplay = cv2.warpPerspective(imageRawGrade, InvmatrixG, (widthImg, heightImg))

            imgFinal = cv2.addWeighted(imgFinal, 1, ImageInvWarp, 1, 0)
            imgFinal = cv2.addWeighted(imgFinal, 1, imgInvGradeDisplay, 1, 0)

        imgBlank = np.zeros_like(img)
        imageArray = (
        [img, imgGrey, imgBlur, imgCanny], [imageCountours, imageBiggestCountours, imageWarpColored, imgThresh]
        , [imageResults, imageRawDrawing, ImageInvWarp, imgFinal])
    except:
        imgBlank = np.zeros_like(img)
        imageArray = ([img, imgGrey, imgBlur, imgCanny], [imgBlank, imgBlank, imgBlank, imgBlank]
                      , [imgBlank, imgBlank, imgBlank, imgBlank])

    labels = [["Original", "Grey", "Blur", "Canny"], ["Contours", "Biggest Con", "Warp",
                                                      "Threshold"], ["Result", "Raw Drawing", "Inv Warp", "Final"]]
    imageStacked = utils.stackImages(imageArray, 0.4)
    cv2.imshow("FinalResult", imgFinal)
    cv2.imshow("Stacked Images", imageStacked)
    if cv2.waitKey(1) & 0xFF == ord('s'):
        cv2.imwrite("FinalResult.jpg", imgFinal)
        cv2.waitKey(300)
