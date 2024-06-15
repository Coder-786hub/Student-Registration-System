from tkinter import *
from datetime import date
from tkinter import messagebox, filedialog
from tkinter.ttk import Combobox
from PIL import Image, ImageTk
import os
import shutil
import mysql.connector
from mysql.connector import Error

# Set up colors
background = "#06283D"
framebg = "#EDEDED"
framefg = "#06283D"

# Create the main window
root = Tk()
root.title("Student Registration System")
root.geometry("1250x700+210+100")
root.config(bg=background)
root.iconbitmap("Registration Form/icon.ico")

def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            database="PROJECT",
            user="root",
            password="Aftab@786"
        )
        if connection.is_connected():
            return connection
    except Error as e:
        messagebox.showerror("Database Error", f"Error connecting to MySQL: {e}")
        return None

def generate_registration_no():
    connection = connect_to_db()
    if connection is None:
        return None

    cursor = connection.cursor()
    cursor.execute("SELECT MAX(registration_no) FROM admin")
    max_reg_no = cursor.fetchone()[0]
    cursor.close()
    connection.close()

    return 1 if max_reg_no is None else max_reg_no + 1

def save():
    if (not name.get() or not dob.get() or not radio.get() or
        not class1.get() or not religion.get() or not skills.get() or
        not father.get() or not mother.get() or not father_occu.get() or
        not mother_occu.get()):
        messagebox.showerror("Error", "All fields are required")
        return

    registration_no = Registration.get()
    if registration_no is None:
        return

    connection = connect_to_db()
    if connection is None:
        return

    cursor = connection.cursor()
    insert_query = """
    INSERT INTO admin (registration_no, name, dob, gender, class, religion, skill, father_name, mother_name, father_occupation, mother_occupation)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    data_tuple = (registration_no, name.get(), dob.get(), "Male" if radio.get() == 1 else "Female", class1.get(), religion.get(), skills.get(), father.get(), mother.get(), father_occu.get(), mother_occu.get())

    try:
        cursor.execute(insert_query, data_tuple)
        connection.commit()
        messagebox.showinfo("Success", "Data Submitted Successfully")
    except Error as e:
        messagebox.showerror("Database Error", f"Error inserting data: {e}")
    finally:
        cursor.close()
        connection.close()

    with open("records.txt", "a") as a:
        a.write(f"{data_tuple}\n")

    if filename:
        try:
            if not os.path.exists("student images"):
                os.makedirs("student images")
            shutil.copy(filename, f"student images/{name.get()}.jpg")
        except Exception as e:
            messagebox.showerror("File Error", f"Error saving image: {e}")

    Registration.set(generate_registration_no())
    clear()

def Exit():
    root.destroy()

def showimage():
    global filename
    global img
    filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select image file",
                                          filetype=(("JPG File", "*.jpg"), ("PNG File", "*.png"), ("All File", "*.*")))
    if filename:
        img = Image.open(filename)
        resized_image = img.resize((190, 190))
        photo2 = ImageTk.PhotoImage(resized_image)
        lb1.config(image=photo2)
        lb1.image = photo2

def clear():
    name.set("")
    dob.set("")
    radio.set(0)
    class1.set("Select class")
    religion.set("")
    skills.set("")
    father.set("")
    mother.set("")
    father_occu.set("")
    mother_occu.set("")
    Registration.set(generate_registration_no())
    lb1.config(image='')

def selecttion():
    pass

def search_student():
    reg_no = search.get()
    if not reg_no:
        messagebox.showerror("Error", "Please enter a registration number")
        return

    connection = connect_to_db()
    if connection is None:
        return

    cursor = connection.cursor()
    query = "SELECT * FROM admin WHERE registration_no = %s"
    try:
        cursor.execute(query, (reg_no,))
        result = cursor.fetchone()
        if result:
            Registration.set(result[0])
            name.set(result[1])
            dob.set(result[2])
            radio.set(1 if result[3] == "Male" else 2)
            class1.set(result[4])
            religion.set(result[5])
            skills.set(result[6])
            father.set(result[7])
            mother.set(result[8])
            father_occu.set(result[9])
            mother_occu.set(result[10])
            # Displaying the image if saved
            image_path = f"student images/{result[1]}.jpg"
            if os.path.exists(image_path):
                img = Image.open(image_path)
                resized_image = img.resize((190, 190))
                photo2 = ImageTk.PhotoImage(resized_image)
                lb1.config(image=photo2)
                lb1.image = photo2
            else:
                lb1.config(image='')
                lb1.image = None
        else:
            messagebox.showinfo("Not Found", "No student found with this registration number")
    except Error as e:
        messagebox.showerror("Database Error", f"Error fetching data: {e}")
    finally:
        cursor.close()
        connection.close()

def update_student():
    if (not name.get() or not dob.get() or not radio.get() or
        not class1.get() or not religion.get() or not skills.get() or
        not father.get() or not mother.get() or not father_occu.get() or
        not mother_occu.get()):
        messagebox.showerror("Error", "All fields are required")
        return

    registration_no = Registration.get()
    if registration_no is None:
        return

    connection = connect_to_db()
    if connection is None:
        return

    cursor = connection.cursor()
    update_query = """
    UPDATE admin 
    SET name=%s, dob=%s, gender=%s, class=%s, religion=%s, skill=%s, father_name=%s, mother_name=%s, father_occupation=%s, mother_occupation=%s
    WHERE registration_no=%s
    """
    data_tuple = (name.get(), dob.get(), "Male" if radio.get() == 1 else "Female", class1.get(), religion.get(), skills.get(), father.get(), mother.get(), father_occu.get(), mother_occu.get(), registration_no)

    try:
        cursor.execute(update_query, data_tuple)
        connection.commit()
        messagebox.showinfo("Success", "Data Updated Successfully")
    except Error as e:
        messagebox.showerror("Database Error", f"Error updating data: {e}")
    finally:
        cursor.close()
        connection.close()

    with open("records.txt", "a") as a:
        a.write(f"Updated: {data_tuple}\n")

    if filename:
        try:
            if not os.path.exists("student images"):
                os.makedirs("student images")
            shutil.copy(filename, f"student images/{name.get()}.jpg")
        except Exception as e:
            messagebox.showerror("File Error", f"Error saving image: {e}")

    clear()

# Top frames
Label(root, text="Email: aftabcomputertechnology@gmail.com", width=10, height=3, bg="#f0687c", anchor='e').pack(side=TOP, fill=X)
Label(root, text="STUDENT REGISTRATION", width=10, height=2, bg="#c36464", fg="#fff", font='arial 20 bold').pack(side=TOP, fill=X)

# Search box to update
search = StringVar()
Entry(root, textvariable=search, width=15, bd=2, font='arial 20').place(x=820, y=70)
imageicon = PhotoImage(file="Registration Form/search.png")
srch = Button(root, text="Search", compound=LEFT, image=imageicon, width=113, height=35, bg="#68ddfa", font="arial 13 bold", command=search_student)
srch.place(x=1070, y=70)

img3 = PhotoImage(file="Registration Form/update.png")
update_button = Button(root, bg="white", image=img3, command=update_student)
update_button.place(x=100, y=70)

# Registration and date
Label(root, text="Registration No", font="arial 13", fg=framebg, bg=background).place(x=30, y=150)
Label(root, text="Date", font="arial 13", fg=framebg, bg=background).place(x=500, y=150)

Registration = StringVar()
Date = StringVar()

reg_entry = Entry(root, textvariable=Registration, width=15, font="arial 10")
reg_entry.place(x=160, y=150)
Registration.set(generate_registration_no())

today = date.today()
d1 = today.strftime("%d/%m/%Y")
Date_entry = Entry(root, textvariable=Date, width=15, font="arial 10")
Date_entry.place(x=560, y=150)
Date.set(d1)

# Student details
obj = LabelFrame(root, text="Student's Details", font=20, bd=2, width=900, bg=framebg, fg=framefg, height=250, relief=GROOVE)
obj.place(x=30, y=200)

# Labels
Label(obj, text="Full Name:", font="arial 13", bg=framebg, fg=framefg).place(x=30, y=50)
Label(obj, text="Date of Birth:", font="arial 13", bg=framebg, fg=framefg).place(x=30, y=100)
Label(obj, text="Gender:", font="arial 13", bg=framebg, fg=framefg).place(x=30, y=150)
Label(obj, text="Class:", font="arial 13", bg=framebg, fg=framefg).place(x=500, y=50)
Label(obj, text="Religion:", font="arial 13", bg=framebg, fg=framefg).place(x=500, y=100)
Label(obj, text="Skills:", font="arial 13", bg=framebg, fg=framefg).place(x=500, y=150)

# Entry fields
name = StringVar()
dob = StringVar()
radio = IntVar()
class1 = StringVar()
religion = StringVar()
skills = StringVar()

Entry(obj, textvariable=name, font="arial 13", bg=framebg, fg=framefg).place(x=160, y=50)
Entry(obj, textvariable=dob, font="arial 13", bg=framebg, fg=framefg).place(x=160, y=100)
Radiobutton(obj, text="Male", variable=radio, value=1, font="arial 13", bg=framebg, fg=framefg, command=selecttion).place(x=150, y=150)
Radiobutton(obj, text="Female", variable=radio, value=2, font="arial 13", bg=framebg, fg=framefg, command=selecttion).place(x=220, y=150)

class1 = Combobox(obj, values=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "B.A", "M.A", "BCA", "MCA", "B.com", "M.com", "BBA", "MBA", "B.tech", "M.tech", "B.pharma", "D.pharma", "M.pharma"], font="arial 13 bold", state="readonly")
class1.place(x=590, y=50)
class1.set("Select class")
Entry(obj, textvariable=religion, font="arial 13", bg=framebg, fg=framefg).place(x=590, y=100)
Entry(obj, textvariable=skills, font="arial 13", bg=framebg, fg=framefg).place(x=590, y=150)

# Parents details
obj2 = LabelFrame(root, text="Parent's Details", font=20, bd=2, width=900, bg=framebg, fg=framefg, height=220, relief=GROOVE)
obj2.place(x=30, y=470)

Label(obj2, text="Father's Name:", font="arial 13", bg=framebg, fg=framefg).place(x=30, y=50)
Label(obj2, text="Mother's Name:", font="arial 13", bg=framebg, fg=framefg).place(x=500, y=50)
Label(obj2, text="Occupation:", font="arial 13", bg=framebg, fg=framefg).place(x=30, y=100)
Label(obj2, text="Occupation:", font="arial 13", bg=framebg, fg=framefg).place(x=500, y=100)

# Entry fields for parents
father = StringVar()
mother = StringVar()
father_occu = StringVar()
mother_occu = StringVar()

Entry(obj2, textvariable=father, font="arial 13", bg=framebg, fg=framefg).place(x=160, y=50)
Entry(obj2, textvariable=mother, font="arial 13", bg=framebg, fg=framefg).place(x=690, y=50)
Entry(obj2, textvariable=father_occu, font="arial 13", bg=framebg, fg=framefg).place(x=160, y=100)
Entry(obj2, textvariable=mother_occu, font="arial 13", bg=framebg, fg=framefg).place(x=690, y=100)

# Image
f = Frame(root, bd=3, bg="black", width=200, height=200, relief=GROOVE)
f.place(x=1000, y=150)

img = PhotoImage(file="Registration Form/upload.png")
lb1 = Label(f, bg="black", image=img)
lb1.place(x=0, y=0)

# Buttons
Button(root, text="Upload", width=19, height=2, font="arial 12 bold", bg="lightblue", command=showimage).place(x=1000, y=370)
Button(root, text="Save", width=19, height=2, font="arial 12 bold", bg="lightgreen", command=save).place(x=1000, y=450)
Button(root, text="Reset", width=19, height=2, font="arial 12 bold", bg="lightpink", command=clear).place(x=1000, y=530)
Button(root, text="Exit", width=19, height=2, font="arial 12 bold", bg="grey", command=Exit).place(x=1000, y=610)

root.mainloop()
