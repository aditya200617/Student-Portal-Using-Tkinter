from tkinter import *
from tkinter import messagebox,ttk
import csv
import os

DATA_FILE = "students.csv"
students = []

root = Tk()

root.geometry("1000x750")
root.title("Add / Edit Student")
root.config(bg="white")



def add_student():
    name = name_entry.get()
    email = email_entry.get()
    password = pass_entry.get()
    if name == "" or email == "":
        messagebox.showerror("Error","Please fill Name and Email")
    else:
        student_table.insert("","end",values=(len(student_table.get_children())+1,name,email,password))
        clear_fields()
    students.append({'name': name, 'email': email, 'password': password})
    refresh_table()
    clear_fields()
    save_data()

def delete_student():
    selected_item = student_table.selection()
    if not selected_item:
        messagebox.showwarning("Warning","Please select a row to delete")
        return
    for item in selected_item:
        student_table.delete(item)  

def clear_fields():
    name_entry.delete(0,END)
    email_entry.delete(0,END)
    pass_entry.delete(0,END)

def update_student():
    selected = student_table.focus()
    if selected:
        current_data = student_table.item(selected)['values']
        student_table.item(selected, values=(current_data[0],name_entry.get(),email_entry.get(),pass_entry.get()))
        clear_fields()

def get_data_from_table(event):
    selected_row = student_table.focus()
    data = student_table.item(student_table.focus())['values']
    if data:
        name_entry.delete(0,END)
        name_entry.insert(0,data[1])
        email_entry.delete(0,END)
        email_entry.insert(0,data[2])
        pass_entry.delete(0,END)
        pass_entry.insert(0,data[3])

def save_data(show_message=True):
    with open(DATA_FILE, mode='w', newline='') as f:
        print("Saving data to CSV...")
        writer = csv.writer(f)
        writer.writerow(["name", "email", "password"])
        print(students,"studentss ------")
        for student in students:
            print(f"Writing student: {student}")
            writer.writerow([student['name'], student['email'], student['password']])
    if show_message:
        messagebox.showinfo("Saved", "Student data saved to CSV successfully.")
    else:
        messagebox.showwarning("Delete", "Student data Deleted to CSV successfully.")


def refresh_table():
    for row in student_table.get_children():
        student_table.delete(row)
    for i, student in enumerate(students, start=1):
        student_table.insert('', 'end', values=(i, student['name'], student['email'], student['password']))


def load_data():
    global students
    students.clear()
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, mode='r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                students.append(row)
        refresh_table()

def edit_student():
    selected = student_table.selection()
    if not selected:
        messagebox.showwarning("Selection Error", "Please select a student to edit.")
        return

    global edit_index
    edit_index = int(student_table.item(selected[0])['values'][0]) - 1
    print("------", edit_index)
    print("================ students", students)
    student = students[edit_index]
    print("================ student", student)
    name_var.set(student['name'])
    email_var.set(student['email'])
    password_var.set(student['password'])

name_var = StringVar()
email_var = StringVar()
password_var = StringVar()
edit_index = None


left_frame = Frame(root, bg="white", padx=20)
left_frame.place(x=0, y=0, width=300, height=500)

Label(left_frame,text="Add / Edit Student",font=("Arial",16,"bold"),bg="white").pack(pady=20)

Label(left_frame, text="Name:", bg="white").pack(anchor="w")
name_entry = Entry(left_frame, font=("Arial", 12), bd=1, relief="solid", textvariable=name_var)
name_entry.pack(fill="x", pady=5)

Label(left_frame, text="Email:", bg="white").pack(anchor="w")
email_entry = Entry(left_frame, font=("Arial", 12), bd=1, relief="solid", textvariable=email_var)
email_entry.pack(fill="x", pady=5)

Label(left_frame, text="Password:", bg="white").pack(anchor="w")
pass_entry = Entry(left_frame, font=("Arial", 12), bd=1, relief="solid", show="*", textvariable=password_var)
pass_entry.pack(fill="x", pady=5)


Button(left_frame, text="Add Student", bg="blue", fg="black", font=("Arial", 10, "bold"), command=add_student).pack(fill="x", pady=5)

Button(left_frame, text="Update Student", bg="blue", fg="black", font=("Arial", 10, "bold"),command=update_student ).pack(fill="x", pady=5)

Button(left_frame, text="Clear", bg="red", fg="black", font=("Arial", 10, "bold"),command=clear_fields).pack(fill="x", pady=5)



right_frame = Frame(root, bg="white", bd=1, relief="solid")
right_frame.place(x=320, y=50, width=650, height=400)

Label(right_frame, text="Student Information", font=("Arial", 14, "bold"), bg="#F0F0F0").pack(fill="x")


cols = ("ID", "Name", "Email", "Password")
student_table = ttk.Treeview(right_frame, columns=cols, show='headings')
for col in cols:
    student_table.heading(col, text=col)
    student_table.column(col, width=100, anchor="center")
student_table.pack(fill="both", expand=True)


btn_frame = Frame(root, bg="white")
btn_frame.place(x=320, y=470, width=650, height=50)

Button(btn_frame, text="Edit", bg="orange", width=12,command=edit_student).pack(side="left", padx=10)
Button(btn_frame, text="Delete", bg="red", fg="black", width=12, command=delete_student).pack(side="left", padx=10)
Button(btn_frame, text="Save", bg="purple", fg="black", width=12,command=save_data).pack(side="left", padx=10)
Button(btn_frame, text="Exit", bg="grey", fg="black", width=12, command=root.quit).pack(side="left", padx=10)


load_data()
root.mainloop()