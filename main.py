import cv2
import numpy as np
import utils
import tkinter as tk
import csv
from tkinter import filedialog

# set up input and output file paths
file_path = 'test.csv'
headers = ['ID', 'Score']

# add data to the rows

###########
# path = gui.select_model_answer_file()
# print("Path is ", path)
############
rows = 10
columns = 5
widthImg = 700
heightImg = 700
questions = 10
choices = 5
webCamFeed = True
cameraNo = 0

#####################

# setting up the camera
cap = cv2.VideoCapture(cameraNo)
cap.set(10, 150)


def getAnswers(pathA, widthImgA, heightImgA):
    imgA = cv2.imread(pathA)
    imgA = cv2.resize(imgA, (widthImgA, heightImgA))
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
    # this draws the countors of 2 biggest boxes
    if biggestCountorA.size != 0:
        cv2.drawContours(imageBiggestCountoursA, biggestCountorA, -1, (0, 255, 0), 20)

        biggestCountorA = utils.reorder(biggestCountorA)

        # for the mcqs
        pt1A = np.float32(biggestCountorA)
        pt2A = np.float32([[0, 0], [widthImgA, 0], [0, heightImgA], [widthImgA, heightImgA]])
        matrixA = cv2.getPerspectiveTransform(pt1A, pt2A)
        imageWarpColoredA = cv2.warpPerspective(imgA, matrixA, (widthImgA, heightImgA))

        # Applying threshold (byshoof el marked spots)
        imgWarpGrayA = cv2.cvtColor(imageWarpColoredA, cv2.COLOR_BGR2GRAY)
        imgThreshA = cv2.threshold(imgWarpGrayA, 150, 200, cv2.THRESH_BINARY_INV)[1]

        boxesA = utils.splitBoxes(imgThreshA, questions, choices)
        myPixelValA = np.zeros((questions, choices))
        countCA = 0
        countRA = 0
        # cv2.imshow("imgA",imgA)
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


def functionOpen(path):
    ans = getAnswers(path, 600, 600)
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
                imgThresh = cv2.threshold(imgWarpGray, 150, 200, cv2.THRESH_BINARY_INV)[1]

                imgWarpGray_ID = cv2.cvtColor(imageID, cv2.COLOR_BGR2GRAY)
                imgThresh_ID = cv2.threshold(imgWarpGray_ID, 150, 200, cv2.THRESH_BINARY_INV)[1]

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
                    # if totalPixels > 4000:
                    myPixelVal[countR][countC] = totalPixels
                    # else:
                        # myPixelVal[countR][countC] = 0
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
                myIDVal = np.zeros((5, 10))
                countC_ID = 0
                countR_ID = 0
                #
                for ids in idsBoxes:
                    totalPixels_id = cv2.countNonZero(ids)
                    myIDVal[countC_ID][countR_ID] = totalPixels_id
                    countR_ID += 1
                    if countR_ID == 10:
                        countC_ID += 1
                        countR_ID = 0

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

                for x_ID in range(0, 5):
                    arr_ID = myIDVal[x_ID]
                    myIndexVal_ID = np.where(arr_ID == np.amax(arr_ID))
                    myIndex_ID.append(myIndexVal_ID[0][0])
                print(myIndex_ID)

                imageResults = imageWarpColored.copy()
                imageResultsID = imageID.copy()
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
                cv2.putText(imageRawGrade, str(int(score)) + "%", (50, 100), cv2.FONT_HERSHEY_COMPLEX, 3, (0, 255, 255),
                            3)
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
        # imageStacked = utils.stackImages(imageArray, 0.4)
        cv2.imshow("FinalResult", imgFinal)
        # cv2.imshow("Stacked Images", imageStacked)
        if cv2.waitKey(1) & 0xFF == ord('s'):
            # get input values for id and score
            # create a list of rows to append to the CSV file
            rowsCSV = [
                [str(myIndex_ID[0]) + str(myIndex_ID[1]) + str(myIndex_ID[2]) + str(myIndex_ID[3]) + str(myIndex_ID[4]),
                 score]]

            # append the rows to the CSV file
            with open(file_path, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(rowsCSV)

            # cv2.imwrite("FinalResult.jpg", imgFinal)
            cv2.waitKey(300)
        if cv2.waitKey(1) & 0xFF == ord('t'):
            cv2.waitKey(300)
            break


# Create the main window
root = tk.Tk()

# Set the window title
root.title("Welcome to my App")

# Set the minimum window size
root.minsize(500, 200)

# Set the background color
root.configure(bg='#B799FF')

# Create a list to store the screens
screens = []

# Create the label widget for the main screen
main_label = tk.Label(root, text="Welcome to ASU Faculty of Engineering Optical Mark Recognition", bg='#E6FFFD',
                      fg='#333333', font=('Arial', 16, 'bold'))

# Create the Teacher button for the main screen
teacher_button = tk.Button(root, text="Teacher", padx=20, pady=10, bg='#ACBCFF', fg='#FFFFFF',
                           font=('Arial', 12, 'bold'))

# Create the Student button for the main screen
student_button = tk.Button(root, text="Student", padx=20, pady=10, bg='#ACBCFF', fg='#FFFFFF',
                           font=('Arial', 12, 'bold'))


# Define the function to create a new screen
def create_screen(title, bg_color, remove_widgets=False):
    # Create a new Toplevel window for the screen
    screen = tk.Toplevel(root)
    # Set the window title
    screen.title(title)
    # Set the minimum window size
    screen.minsize(300, 150)
    # Set the background color
    screen.configure(bg=bg_color)
    # Append the screen to the list of screens
    screens.append(screen)
    # Create the Back button
    back_button = tk.Button(screen, text="Back", padx=20, pady=10, bg='#ACBCFF', fg='#FFFFFF',
                            font=('Arial', 12, 'bold'), command=screen.destroy)
    # Pack the Back button into the screen
    back_button.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
    if remove_widgets:
        # Remove the main label from the main screen
        main_label.pack_forget()


# Define the function to open the teacher screen
def open_teacher_screen():
    # Create the Teacher screen and remove the main label
    create_screen("Teacher Screen", '#E6FFFD', remove_widgets=True)
    enter_model_answer_button = tk.Button(screens[-1], text="Enter Model Answer", padx=20, pady=10, bg='#ACBCFF',
                                          fg='#FFFFFF', font=('Arial', 12, 'bold'), command=select_model_answer_file)
    enter_model_answer_button.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)


# Define the function to select the model answer file
def select_model_answer_file():
    # Open the file dialog to select the model answer file
    file_path = filedialog.askopenfilename()
    functionOpen(file_path)


# Define the function to open the student screen
def open_student_screen():
    # Create the Student screen and remove the main label
    create_screen("Student Screen", '#E6FFFD', remove_widgets=True)
    enter_student_id_button = tk.Button(screens[-1], text="Enter Student ID", padx=20, pady=10, bg='#ACBCFF',
                                        fg='#FFFFFF', font=('Arial', 12, 'bold'), command=check_student_id)
    enter_student_id_button.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)


# Define the function to check the student ID
def check_student_id():
    with open('test.csv', 'r') as file:
        reader = csv.reader(file)
        student_grades = dict(reader)
    dialog = tk.Toplevel(screens[-1])
    dialog.title("Enter Student ID")
    dialog.minsize(200, 100)
    # Set the background color
    dialog.configure(bg='#E6FFFD')
    # Create the label and entry widgets
    label = tk.Label(dialog, text="Enter your Student ID:", bg='#E6FFFD', fg='#333333', font=('Arial', 12, 'bold'))
    entry = tk.Entry(dialog, bg='#FFFFFF', fg='#333333', font=('Arial', 12))
    # Create the OK button
    ok_button = tk.Button(dialog, text="OK", bg='#ACBCFF', fg='#FFFFFF', font=('Arial', 12, 'bold'),
                          command=lambda: verify_student_id(entry.get(), student_grades, dialog))
    # Pack the widgets into the dialog box
    label.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
    entry.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
    ok_button.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)


# Define the function to verify the student ID
def verify_student_id(student_id, student_grades, dialog):
    if student_id in student_grades:
        grade = student_grades[student_id]
        dialog.destroy()
        show_grade_screen(grade)
    else:
        tk.messagebox.showerror("Error", "Invalid student ID.")


# Define the function to show the grade screen
def show_grade_screen(grade):
    # Create the Grade screen
    create_screen("Grade Screen", '#E6FFFD')

    # Create the Grade label
    grade_label = tk.Label(screens[-1], text=f"Your grade is: {grade}", bg='#E6FFFD', fg='#333333',
                           font=('Arial', 16, 'bold'))

    # Pack the Grade label into the screen
    grade_label.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)


# Pack the main label into the main window
main_label.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

# Pack the Teacher and Student buttons into the main window
teacher_button.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
student_button.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

# Bind the Teacher button to the open_teacher_screen function
teacher_button.configure(command=open_teacher_screen)

# Bind the Student button to the open_student_screen function
student_button.configure(command=open_student_screen)
# Run the main loop
root.mainloop()
