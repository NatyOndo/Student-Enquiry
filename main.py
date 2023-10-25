
from tkinter import *
from tkinter import Text
import tkinter as tk
from tkinter import ttk
import re
from tkinter import messagebox
import sqlite3

root = Tk()
root.title("Student Enquiry System")
root.config(bg='#AAAAAA')
root.geometry('900x900')  # This sets the window size
root.iconbitmap('stud.ico')

# root.resizable(False, False)

# Connecting to the database
connection = sqlite3.connect("student_details.db")
cursor = connection.cursor()
def connectDb():
    cursor.execute("""CREATE TABLE studInformation(
                Student_Num INTEGER PRIMARY KEY,
                Name text NOT NULL,
                Surname text NOT NULL,
                Email varchar(30) NOT NULL,
                Query text)
                """)
    print("created")
    connection.commit()
    connection.close()

# Creating the Functions
import re


def logQuery():
    # verifying that all boxes are not empty
    if len(nameTxt.get("1.0", "end-1c").strip()) == 0 or len(surnameTxt.get("1.0", "end-1c").strip()) == 0 or len(
            emailTxt.get("1.0", "end-1c").strip()) == 0 or len(queryTxt.get("1.0", "end-1c").strip()) == 0:
        messagebox.showerror("Error", "Please fill all the boxes.")
        return

    email = emailTxt.get("1.0", "end-1c").strip()
    pattern = r"[^@]+@[^@]+\.[^@]+"
    if not re.match(pattern, email):
        messagebox.showerror("Error", "Invalid email format, insert a valid email.")
        # clear the text boxes
        emailTxt.delete("1.0", END)
        return

    name = nameTxt.get("1.0", "end-1c").strip()
    surname = surnameTxt.get("1.0", "end-1c").strip()
    query = queryTxt.get("1.0", "end-1c").strip()
    cursor.execute("SELECT * FROM studInformation WHERE Name = ? AND Surname = ? AND Email = ?", (name, surname, email))
    data = cursor.fetchall()

    if len(data) > 0:
        messagebox.showerror("Error", "You are already registered with the same name, surname and email.")
        # clear the text boxes
        nameTxt.delete("1.0", END)
        surnameTxt.delete("1.0", END)
        emailTxt.delete("1.0", END)
        queryTxt.delete("1.0", END)
    else:
        cursor.execute("INSERT INTO studInformation(Name, Surname, Email, Query) values(?,?,?,?)",
                       (name, surname, email, query))
        print("Information entered")
        connection.commit()

        # clear the text boxes
        nameTxt.delete("1.0", END)
        surnameTxt.delete("1.0", END)
        emailTxt.delete("1.0", END)
        queryTxt.delete("1.0", END)
        messagebox.showinfo("Confirmation", "Registered successfully")


def search():
    name = searchNameTxt.get("1.0", "end-1c")
    #Selecting name from studInformation table
    cursor.execute("SELECT * FROM studInformation WHERE Name LIKE ?", ('%'+str(name)+ '%',))
    data = cursor.fetchall()
    if len(data) == 0:
        messagebox.showerror("Error", "Name not registered.")
    else:
        studInformation.delete(*studInformation.get_children())
        for i in data:
            rows = [i[0], i[1], i[2], i[3], i[4]]
            studInformation.insert('', END, values=rows)
    # clearing the textbox
    searchNameTxt.delete("1.0", END)




def viewAll():
    cursor.execute("SELECT * FROM studInformation")
    result = cursor.fetchall()
    studInformation.delete(*studInformation.get_children())
    for i in result:
        rows = [i[0], i[1], i[2], i[3], i[4]]
        studInformation.insert('', END, values=rows)
    connection.commit()


def clearForm():
    #Clearing the treeview form
    for i in studInformation.get_children():
        studInformation.delete(i)


def deleteStudent():
    # Get the selected student from the treeview
    cc = studInformation.focus()
    content = studInformation.item(cc)
    pp = content['values'][0]

    # Ask user for confirmation before deleting
    confirm = messagebox.askyesno('Confirmation', 'Are you sure you want to delete student number {}?'.format(pp))

    # If user confirms deletion
    if confirm:
        # Delete student from the database
        cursor.execute('DELETE FROM studInformation WHERE Student_Num LIKE ?', ('%' + str(pp) + '%',))
        connection.commit()

        # Show success message
        messagebox.showinfo('Notification', 'StudentNumber{} deleted successfully...'.format(pp))

        # Refresh the treeview to reflect changes
        cursor.execute("SELECT * FROM studInformation")
        result = cursor.fetchall()
        studInformation.delete(*studInformation.get_children())
        for i in result:
            rows = [i[0], i[1], i[2], i[3], i[4]]
            studInformation.insert('', END, values=rows)


# ******************************************************************************.Frames
dataEntryFrame = Frame(root, bg='#00ADB5', relief=GROOVE, borderwidth=2)
dataEntryFrame.place(x=25, y=75, width=500, height=720)

titleLbl = Label(dataEntryFrame, text='Enter your details to log a query', font=('bold'), bg='#AAAAAA')
titleLbl.pack(side=TOP, fill=tk.X)

nameLbl = Label(dataEntryFrame, text='Name', font=('bold'), bg="#AEE6E6")
nameLbl.pack(padx=2, pady=2)
nameTxt = Text(dataEntryFrame)
nameTxt.config(width=20, height=1)
nameTxt.pack(fill=tk.X, padx=10, pady=10)


surnameLbl = Label(dataEntryFrame, text='Surname', font=('bold'), bg="#AEE6E6")
surnameLbl.pack(padx=2, pady=2)
surnameTxt = Text(dataEntryFrame)
surnameTxt.config(width=20, height=1)
surnameTxt.pack(fill=tk.X, padx=10, pady=10)

emailLbl = Label(dataEntryFrame, text='Email', font=('bold'), bg="#AEE6E6")
emailLbl.pack(padx=2, pady=2)
emailTxt = Text(dataEntryFrame) # Adding a textbox
emailTxt.config(width=20, height=1)
emailTxt.pack(fill=tk.X, padx=10, pady=10)

queryLbl = Label(dataEntryFrame, text='Student Query', font=('bold'), bg="#AEE6E6")
queryLbl.pack(padx=2, pady=2)
queryTxt = Text(dataEntryFrame) # Adding a textbox
queryTxt.config(width=20, height=2)
queryTxt.pack(fill=tk.X, padx=10, pady=10)

#creating the submit button
submitButton = Button(dataEntryFrame, text='Submit', font=('bold'), bg='#AAAAAA', command=logQuery)
submitButton.pack(fill=tk.X, padx=10, pady=10)

title2Lbl = Label(dataEntryFrame, text='Enter name to search', font=('bold'), bg="#AEE6E6")
title2Lbl.pack(padx=10, pady=10)
searchNameTxt = Text(dataEntryFrame)
searchNameTxt.config(width=20, height=1)
searchNameTxt.pack(fill=tk.X, padx=10, pady=10)

searchButton = Button(dataEntryFrame, text='Search', font=('bold'), bg='#AAAAAA', command=search)
searchButton.pack(fill=tk.X, padx=10, pady=10)
viewAllButton = Button(dataEntryFrame, text='View All', font=('bold'), bg='#AAAAAA', command=viewAll)
viewAllButton.pack(fill=tk.X, padx=10, pady=10)
clearButton = Button(dataEntryFrame, text='Clear Form', bg='#AAAAAA', font=('bold'), command=clearForm)
clearButton.pack(fill=tk.X, padx=10, pady=10)
deleteButton = Button(dataEntryFrame, text='Delete', bg='#AAAAAA', font=('bold'), command=deleteStudent)
deleteButton.pack(fill=tk.X, padx=10, pady=10)

showDataFrame = Frame(root, relief=GROOVE, borderwidth=2)
showDataFrame.place(x=550, y=80, width=990, height=720)

# ******************************************************************************.Show data Frame

style = ttk.Style()

#Defining the style of the frame header
style.configure('Treeview.Heading', font=('calibri', 15, 'bold'), foreground='Black')

#Creating scrollbars
x_Scroll = Scrollbar(showDataFrame, orient=HORIZONTAL)
y_Scroll = Scrollbar(showDataFrame, orient=VERTICAL)
studInformation = ttk.Treeview(showDataFrame, columns=('Student Num', 'Student Name', 'Surname', 'Email', 'Query'),
                               yscrollcommand=y_Scroll.set, xscrollcommand=x_Scroll.set)

x_Scroll.config(command=studInformation.xview)
y_Scroll.config(command=studInformation.yview)
x_Scroll.pack(side=BOTTOM, fill=X)
y_Scroll.pack(side=RIGHT, fill=Y)

#Setting heading titles
studInformation.heading('Student Num', text='Student Number', anchor="center")
studInformation.heading('Student Name', text='Student Name', anchor="center")
studInformation.heading('Surname', text='Surname', anchor="center")
studInformation.heading('Email', text='Email', anchor="center")
studInformation.heading('Query', text='Query', anchor="center")

# This will make titles to appear from the top-beginning of the frame
studInformation['show'] = 'headings'

#This will make the columns to expand to fill the available space
studInformation.column("Student Num", stretch=True)
studInformation.column("Student Name", stretch=True)
studInformation.column("Surname", stretch=True)
studInformation.column("Email", stretch=True)
studInformation.column("Query", stretch=True)

#Setting the width of each column
studInformation.column('Student Num', width=80)
studInformation.column('Student Name', width=80)
studInformation.column('Surname', width=80)
studInformation.column('Email', width=150)
studInformation.column('Query', width=180)

#This adds the treeview widget to the window and fills the available space
studInformation.pack(fill=BOTH, expand=True)

# *********************************************************************************.Slider
txt = 'STUDENT ENQUIRY SYSTEM'
sliderLabel = tk.Label(root, bg='#AAAAAA', text=txt, font=('calibri', 30, 'bold'), relief=GROOVE, borderwidth=4)
sliderLabel.pack(fill=tk.X, ipady=2)

root.mainloop()

