import tkinter as tk
from tkinter import ttk, messagebox
import csv
from datetime import datetime

FILE_NAME = "expenses.csv"



def init_file():
    try:
        with open(FILE_NAME, "r"):
            pass
    except:
        with open(FILE_NAME, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Amount", "Category", "Note"])


# Add Expense 
def add_expense():
    amount = amount_entry.get()
    category = category_var.get()
    note = note_entry.get()

    if amount == "" or category == "":
        messagebox.showerror("Error", "Amount and Category required!")
        return

    try:
        amount = float(amount)
    except:
        messagebox.showerror("Error", "Amount must be numeric!")
        return

    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(FILE_NAME, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([date, amount, category, note])

    amount_entry.delete(0, tk.END)
    note_entry.delete(0, tk.END)

    load_data()
    update_total_label()
    messagebox.showinfo("Success", "Expense Added!")


# Load Data into Table 
def load_data(filter_cat=None):
    for row in table.get_children():
        table.delete(row)

    try:
        with open(FILE_NAME, "r") as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                if filter_cat:
                    if row[2].lower() == filter_cat.lower():
                        table.insert("", tk.END, values=row)
                else:
                    table.insert("", tk.END, values=row)
    except:
        pass


# - Delete Selected Expenses
def delete_expense():
    selected = table.selection()
    if not selected:
        messagebox.showerror("Error", "Select a row to delete")
        return

    values = table.item(selected)["values"]
    date_to_delete = values[0]

    rows = []
    with open(FILE_NAME, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] != date_to_delete:
                rows.append(row)

    with open(FILE_NAME, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(rows)

    load_data()
    update_total_label()
    messagebox.showinfo("Deleted", "Expense Deleted Successfully!")


#  Show Total 
def calculate_total():
    total = 0
    try:
        with open(FILE_NAME, "r") as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                total += float(row[1])
    except:
        pass
    messagebox.showinfo("Total Expense", f"Total Expense: {total} TK")


# Real-time Total Label
def update_total_label():
    total = 0
    try:
        with open(FILE_NAME, "r") as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                total += float(row[1])
    except:
        pass

    total_label.config(text=f"Total Expenses: {total} TK")


#  Monthly Report
def show_monthly():
    month = datetime.now().strftime("%Y-%m")
    total = 0

    with open(FILE_NAME, "r") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            if row[0].startswith(month):
                total += float(row[1])

    messagebox.showinfo("Monthly Report", f"This Month's Total: {total} TK")


#  Search by Category 
def search_category():
    cat = search_entry.get()
    if cat == "":
        load_data()
    else:
        load_data(cat)


# GUI PART 

root = tk.Tk()
root.title("Advanced Expense Tracker")
root.geometry("750x580")
root.resizable(False, False)

init_file()

title = tk.Label(root, text="Advanced Expense Tracker", font=("Arial", 18, "bold"))
title.pack(pady=10)

frame = tk.Frame(root)
frame.pack(pady=10)

# Amount
tk.Label(frame, text="Amount", font=("Arial", 12)).grid(row=0, column=0)
amount_entry = tk.Entry(frame, font=("Arial", 12))
amount_entry.grid(row=0, column=1, padx=10)

# Category
tk.Label(frame, text="Category", font=("Arial", 12)).grid(row=1, column=0)
category_var = tk.StringVar()
category_menu = ttk.Combobox(frame, textvariable=category_var, font=("Arial", 12),
                             values=("Food", "Travel", "Shopping", "Bills", "Health", "Other"))
category_menu.grid(row=1, column=1)

# Note
tk.Label(frame, text="Note", font=("Arial", 12)).grid(row=2, column=0)
note_entry = tk.Entry(frame, font=("Arial", 12))
note_entry.grid(row=2, column=1)

# Add Button
tk.Button(root, text="Add Expense", font=("Arial", 12), bg="#4CAF50", fg="white",
          command=add_expense).pack(pady=8)

# Search
search_frame = tk.Frame(root)
search_frame.pack()

tk.Label(search_frame, text="Search Category:", font=("Arial", 12)).grid(row=0, column=0)
search_entry = tk.Entry(search_frame, font=("Arial", 12))
search_entry.grid(row=0, column=1, padx=10)
tk.Button(search_frame, text="Search", command=search_category, bg="#2196F3", fg="white").grid(row=0, column=2)

# Table
columns = ("Date", "Amount", "Category", "Note")
table = ttk.Treeview(root, columns=columns, show="headings", height=12)

for col in columns:
    table.heading(col, text=col)
    table.column(col, width=160)

table.pack(pady=10)

load_data()

# Total Label (Real Time)
total_label = tk.Label(root, text="Total Expenses: 0 TK", font=("Arial", 14, "bold"))
total_label.pack(pady=5)
update_total_label()

# Bottom Buttons
bottom_frame = tk.Frame(root)
bottom_frame.pack(pady=10)

tk.Button(bottom_frame, text="Show Total", command=calculate_total, bg="#673AB7", fg="white",
          width=12).grid(row=0, column=0, padx=10)

tk.Button(bottom_frame, text="Delete Selected", command=delete_expense, bg="#E91E63", fg="white",
          width=12).grid(row=0, column=1, padx=10)

tk.Button(bottom_frame, text="Monthly Report", command=show_monthly, bg="#009688", fg="white",
          width=12).grid(row=0, column=2, padx=10)

root.mainloop()

