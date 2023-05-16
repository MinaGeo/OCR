# import tkinter as tk
# import csv
# from tkinter import filedialog
# import main
#
# # Create the main window
# root = tk.Tk()
#
# # Set the window title
# root.title("Welcome to my App")
#
# # Set the minimum window size
# root.minsize(500, 200)
#
# # Set the background color
# root.configure(bg='#B799FF')
#
# # Create a list to store the screens
# screens = []
#
# # Create the label widget for the main screen
# main_label = tk.Label(root, text="Welcome to ASU Faculty of Engineering Optical Mark Recognition", bg='#E6FFFD',
#                       fg='#333333', font=('Arial', 16, 'bold'))
#
# # Create the Teacher button for the main screen
# teacher_button = tk.Button(root, text="Teacher", padx=20, pady=10, bg='#ACBCFF', fg='#FFFFFF',
#                            font=('Arial', 12, 'bold'))
#
# # Create the Student button for the main screen
# student_button = tk.Button(root, text="Student", padx=20, pady=10, bg='#ACBCFF', fg='#FFFFFF',
#                            font=('Arial', 12, 'bold'))
#
# # Define the function to create a new screen
# def create_screen(title, bg_color, remove_widgets=False):
#     # Create a new Toplevel window for the screen
#     screen = tk.Toplevel(root)
#
#     # Set the window title
#     screen.title(title)
#
#     # Set the minimum window size
#     screen.minsize(300, 150)
#
#     # Set the background color
#     screen.configure(bg=bg_color)
#
#     # Append the screen to the list of screens
#     screens.append(screen)
#
#     # Create the Back button
#     back_button = tk.Button(screen, text="Back", padx=20, pady=10, bg='#ACBCFF', fg='#FFFFFF',
#                             font=('Arial', 12, 'bold'), command=screen.destroy)
#
#     # Pack the Back button into the screen
#     back_button.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
#
#     if remove_widgets:
#         # Remove the main label from the main screen
#         main_label.pack_forget()
#
#
# # Define the function to open the teacher screen
# def open_teacher_screen():
#     # Create the Teacher screen and remove the main label
#     create_screen("Teacher Screen", '#E6FFFD', remove_widgets=True)
#
#     # Create the Enter Model Answer button
#     enter_model_answer_button = tk.Button(screens[-1], text="Enter Model Answer", padx=20, pady=10, bg='#ACBCFF', fg='#FFFFFF', font=('Arial', 12, 'bold'), command=select_model_answer_file)
#
#     # Create the Check Answer button
#     # check_answer_button = tk.Button(screens[-1], text="Check Answer", padx=20, pady=10, bg='#ACBCFF', fg='#FFFFFF', font=('Arial', 12, 'bold'), command=lambda: main.functionOpen(select_model_answer_file()))
#
#     # Pack the buttons into the screen
#     enter_model_answer_button.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
#     # check_answer_button.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
#
#
# # Define the function to select the model answer file
# def select_model_answer_file():
#     # Open the file dialog to select the model answer file
#     file_path = filedialog.askopenfilename()
#     main.functionOpen(file_path)
#     # Return the path of the selected file
#     # return file_path
#
#
# # Define the function to open the student screen
# def open_student_screen():
#     # Create the Student screen and remove the main label
#     create_screen("Student Screen", '#E6FFFD', remove_widgets=True)
#
#     # Create the Enter Student ID button
#     enter_student_id_button = tk.Button(screens[-1], text="Enter Student ID", padx=20, pady=10, bg='#ACBCFF', fg='#FFFFFF', font=('Arial', 12, 'bold'), command=check_student_id)
#
#     # Pack the button into the screen
#     enter_student_id_button.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
#
#
# # Define the function to check the student ID
# def check_student_id():
#     # Read the contents of the CSV file
#     with open('test.csv', 'r') as file:
#         reader = csv.reader(file)
#         student_grades = dict(reader)
#
#     # Create a dialog box to enter the Student ID
#     dialog = tk.Toplevel(screens[-1])
#
#     # Set the window title
#     dialog.title("Enter Student ID")
#
#     # Set the minimum window size
#     dialog.minsize(200, 100)
#
#     # Set the background color
#     dialog.configure(bg='#E6FFFD')
#
#     # Create the label and entry widgets
#     label = tk.Label(dialog, text="Enter your Student ID:", bg='#E6FFFD', fg='#333333', font=('Arial', 12, 'bold'))
#     entry = tk.Entry(dialog, bg='#FFFFFF', fg='#333333', font=('Arial', 12))
#
#     # Create the OK button
#     ok_button = tk.Button(dialog, text="OK", bg='#ACBCFF', fg='#FFFFFF', font=('Arial', 12, 'bold'), command=lambda: verify_student_id(entry.get(), student_grades, dialog))
#
#     # Pack the widgets into the dialog box
#     label.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
#     entry.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
#     ok_button.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
#
#
# # Define the function to verify the student ID
# def verify_student_id(student_id, student_grades, dialog):
#     if student_id in student_grades:
#         grade = student_grades[student_id]
#         dialog.destroy()
#         show_grade_screen(grade)
#     else:
#         tk.messagebox.showerror("Error", "Invalid student ID.")
#
#
# # Define the function to show the grade screen
# def show_grade_screen(grade):
#     # Create the Grade screen
#     create_screen("Grade Screen", '#E6FFFD')
#
#     # Create the Grade label
#     grade_label = tk.Label(screens[-1], text=f"Your grade is: {grade}", bg='#E6FFFD', fg='#333333', font=('Arial', 16, 'bold'))
#
#     # Pack the Grade label into the screen
#     grade_label.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
#
#
# # Pack the main label into the main window
# main_label.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
#
# # Pack the Teacher and Student buttons into the main window
# teacher_button.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
# student_button.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
#
# # Bind the Teacher button to the open_teacher_screen function
# teacher_button.configure(command=open_teacher_screen)
#
# # Bind the Student button to the open_student_screen function
# student_button.configure(command=open_student_screen)
#
# # Run the main loop
# root.mainloop()