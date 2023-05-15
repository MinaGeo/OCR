import cv2
import numpy as np
import utils
import pandas as pd

import csv

# set up input and output file paths
file_path = 'test.csv'
headers = ['ID', 'Score']

# add data to the rows

###########
path = "CaptureID.JPG"

############
rows = 10
columns = 5
widthImg = 700
heightImg = 700
questions = 10
choices = 5
id_eol = [1, 2, 0, 1, 4, 1, 2, 3, 2, 0]
webCamFeed = True
cameraNo = 0
#####################

# setting up the camera
cap = cv2.VideoCapture(cameraNo)
cap.set(10, 150)


def getAnswers(path, widthImg, heightImg):
    imgA = cv2.imread(path)
    # Image preprocessing
    imageCountoursA = imgA.copy()
    imageBiggestCountoursA = imgA.copy()
    imgGreyA = cv2.cvtColor(imgA, cv2.COLOR_BGR2GRAY)  # makes image grey
    imgBlurA = cv2.GaussianBlur(imgGreyA, (5, 5), 1)  # makes image blur
    imgCannyA = cv2.Canny(imgBlurA, 10, 50)  # makes image canny

    # Image preprocessing

    # Defining all countours
    countoursA, hierarchyA = cv2.findContours(imgCannyA, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(imageCountoursA, countoursA, -1, (0, 255, 0), 10)

    # Finding rectangles
    rectConA = utils.rectCountour(countoursA)  # find us the biggest box
    biggestCountorA = utils.getCornerPoints(rectConA[0])  # get us the corner points of the biggest box
    gradePointsA = utils.getCornerPoints(rectConA[2])

    # namePoints = utils.getCornerPoints(rectCon[2])
    # this draws the countors of 2 biggest boxes
    if biggestCountorA.size != 0 and gradePointsA.size != 0:
        cv2.drawContours(imageBiggestCountoursA, biggestCountorA, -1, (0, 255, 0), 20)
        cv2.drawContours(imageBiggestCountoursA, gradePointsA, -1, (0, 0, 255), 20)

        biggestCountorA = utils.reorder(biggestCountorA)
        gradePointsA = utils.reorder(gradePointsA)

        # for the mcqs
        pt1A = np.float32(biggestCountorA)
        pt2A = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
        matrixA = cv2.getPerspectiveTransform(pt1A, pt2A)
        imageWarpColoredA = cv2.warpPerspective(imgA, matrixA, (widthImg, heightImg))

        # for the grades
        ptG1A = np.float32(gradePointsA)
        ptG2A = np.float32([[0, 0], [325, 0], [0, 150], [325, 150]])
        matrixGA = cv2.getPerspectiveTransform(ptG1A, ptG2A)
        imageGradeDisplayA = cv2.warpPerspective(imgA, matrixGA, (325, 150))
        # cv2.imshow("Grade",imageGradeDisplay)

        # Applying threshold (byshoof el marked spots)
        imgWarpGrayA = cv2.cvtColor(imageWarpColoredA, cv2.COLOR_BGR2GRAY)
        imgThreshA = cv2.threshold(imgWarpGrayA, 180, 225, cv2.THRESH_BINARY_INV)[1]

        boxesA = utils.splitBoxes(imgThreshA, questions, choices)
        myPixelValA = np.zeros((questions, choices))
        countCA = 0
        countRA = 0

        for imageA in boxesA:
            totalPixelsA = cv2.countNonZero(imageA)
            myPixelValA[countRA][countCA] = totalPixelsA
            countCA += 1
            if countCA == choices:
                countRA += 1
                countCA = 0
            # print(myPixelVal)
            # el function deh bt7dd el answers ely mtzlla
            answers = []
        for xA in range(0, questions):
            arrA = myPixelValA[xA]
            myIndexValA = np.where(arrA == np.amax(arrA))
            answers.append(myIndexValA[0][0])
        print(answers)
        return answers


ans = getAnswers(path, widthImg, heightImg)

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
    imgFinal_ID = img.copy()
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
        idBox = utils.getCornerPoints(rectCon[1])
        gradePoints = utils.getCornerPoints(rectCon[2])

        # print(biggestCountor)

        # this draws the countors of 2 biggest boxes
        if biggestCountor.size != 0 and gradePoints.size != 0:
            cv2.drawContours(imageBiggestCountours, biggestCountor, -1, (0, 255, 0), 20)
            cv2.drawContours(imageBiggestCountours, gradePoints, -1, (0, 0, 255), 20)
            cv2.drawContours(imageBiggestCountours, idBox, -1, (255, 0, 0), 20)

            biggestCountor = utils.reorder(biggestCountor)
            gradePoints = utils.reorder(gradePoints)
            idBox = utils.reorder(idBox)

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

            # for the id
            id1 = np.float32(idBox)
            id2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
            matrixID = cv2.getPerspectiveTransform(id1, id2)
            imageID = cv2.warpPerspective(img, matrixID, (widthImg, heightImg))

            # Applying threshold (byshoof el marked spots)
            imgWarpGray = cv2.cvtColor(imageWarpColored, cv2.COLOR_BGR2GRAY)
            imgThresh = cv2.threshold(imgWarpGray, 180, 225, cv2.THRESH_BINARY_INV)[1]

            imgWarpGray_ID = cv2.cvtColor(imageID, cv2.COLOR_BGR2GRAY)
            imgThresh_ID = cv2.threshold(imgWarpGray_ID, 180, 225, cv2.THRESH_BINARY_INV)[1]

            boxes = utils.splitBoxes(imgThresh, questions, choices)
            idsBoxes = utils.splitIDBoxes(imgThresh_ID, rows, columns)
            # print(cv2.countNonZero(idsBoxes[1]))

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
            # el function deh bt7dd el answers ely mtzlla
            # Finding index values of the markings
            myIndex = []
            for x in range(0, questions):
                arr = myPixelVal[x]
                myIndexVal = np.where(arr == np.amax(arr))
                myIndex.append(myIndexVal[0][0])
            #
            # # Finding ids
            myIDVal = np.zeros((rows, columns))
            countC_ID = 0
            countR_ID = 0
            #
            for ids in idsBoxes:
                totalPixels_id = cv2.countNonZero(ids)
                myIDVal[countR_ID][countC_ID] = totalPixels_id
                countR_ID += 1
                if countR_ID == rows:
                    countC_ID += 1
                    countR_ID = 0
            #

            #
            #
            # grading_ID = []
            # for i_id in range(0, rows):
            #     if id_eol[i_id] == myIndex_ID[i_id]:
            #         grading_ID.append(1)
            #     else:
            #         grading_ID.append(0)
            # # print(grading_ID)

            # Grading, 3lshan ashoof el egabat ely sa7
            grading = []
            for x in range(0, questions):
                if ans[x] == myIndex[x]:
                    grading.append(1)
                else:
                    grading.append(0)
            # print(grading)
            myIndex_ID = []


            score = (sum(grading) / questions) * 100  # Final grade
            print(score)

            for x_ID in range(0, columns):
                arr_ID = myIDVal[x_ID]
                myIndexVal_ID = np.where(arr_ID == np.amax(arr_ID))
                myIndex_ID.append(myIndexVal_ID[0][0])
            print(myIndex_ID)

            if myIndex_ID[0] != 0 and myIndex_ID[1] != 0 and myIndex_ID[2] != 0 and myIndex_ID[3] != 0 and myIndex_ID[4] != 0:
                rows = [
                    [str(myIndex_ID[0]) + str(myIndex_ID[1]) + str(myIndex_ID[2]) + str(myIndex_ID[3]) + str(myIndex_ID[4]),score]]

                # write the rows to the CSV file
                with open(file_path, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(headers)
                    writer.writerows(rows)


            imageResults = imageWarpColored.copy()
            imageResultsID = imageID.copy()
            # Displaying answers
            imageResults = utils.showAnswers(imageResults, myIndex, grading, ans, questions, choices)
            # imageResultsID = utils.showAnswers(imageResultsID, myIndex_ID, grading_ID, id_eol, rows, columns)

            imageRawDrawing = np.zeros_like(imageWarpColored)
            imageRawDrawing = utils.showAnswers(imageRawDrawing, myIndex, grading, ans, questions,
                                                choices)  # b5ly el black screen 3aleha el egabat

            # imageRawDrawingID = np.zeros_like(imageID)
            # imageRawDrawingID = utils.showAnswers(imageRawDrawingID, myIndex_ID, grading_ID, id_eol, rows, columns)
            # Ha7ot el final egabat, feh awal sora 5ales
            Invmatrix = cv2.getPerspectiveTransform(pt2, pt1)
            ImageInvWarp = cv2.warpPerspective(imageRawDrawing, Invmatrix, (widthImg, heightImg))

            # Invmatrix_ID = cv2.getPerspectiveTransform(id2, id1)
            # ImageInvWarp_ID = cv2.warpPerspective(imageRawDrawingID, Invmatrix_ID, (widthImg, heightImg))

            # hazwed el grade
            imageRawGrade = np.zeros_like(imageGradeDisplay)
            cv2.putText(imageRawGrade, str(int(score)) + "%", (50, 100), cv2.FONT_HERSHEY_COMPLEX, 3, (0, 255, 255), 3)
            InvmatrixG = cv2.getPerspectiveTransform(ptG2, ptG1)
            imgInvGradeDisplay = cv2.warpPerspective(imageRawGrade, InvmatrixG, (widthImg, heightImg))

            imgFinal = cv2.addWeighted(imgFinal, 1, ImageInvWarp, 1, 0)
            imgFinal = cv2.addWeighted(imgFinal, 1, imgInvGradeDisplay, 1, 0)
            # imgFinal = cv2.addWeighted(imgFinal, 1, ImageInvWarp_ID, 1, 0)

            #
            # imgFinal_ID = cv2.addWeighted(imgFinal_ID, 1, ImageInvWarp_ID, 1, 0)
            # imgFinal_ID = cv2.addWeighted(imgFinal_ID, 1, imgInvGradeDisplay, 1, 0)

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
