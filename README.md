import tkinter as tk
from tkinter import ttk, messagebox
import csv
from datetime import datetime

FILE_NAME = "expenses.csv"


# ---------- Initialize CSV if missing ----------
def init_file():
    try:
        with open(FILE_NAME, "r"):
            pass
    except:
        with open(FILE_NAME, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Amount", "Category", "Note"])


# ---------- Add Expense ----------
def add_expense():
    amount = amount_entry.get().strip()
    category = category_var.get().strip()
    note = note_entry.get().strip()

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


# ---------- Load Data into Table (with optional filter function) ----------
def load_data(filter_func=None):
    for row in table.get_children():
        table.delete(row)

    try:
        with open(FILE_NAME, "r") as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                if filter_func:
                    if filter_func(row):
                        table.insert("", tk.END, values=row)
                else:
                    table.insert("", tk.END, values=row)
    except FileNotFoundError:
        pass


# ---------- Delete Selected Expense ----------
def delete_expense():
    selected = table.selection()
    if not selected:
        messagebox.showerror("Error", "Select a row to delete")
        return

    # delete all selected rows (support multiple selection)
    dates_to_delete = [table.item(s)["values"][0] for s in selected]

    rows = []
    with open(FILE_NAME, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            # keep header
            if reader.line_num == 1:
                rows.append(row)
                continue
            if row[0] not in dates_to_delete:
                rows.append(row)

    with open(FILE_NAME, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(rows)

    load_data()
    update_total_label()
    messagebox.showinfo("Deleted", "Selected expense(s) deleted successfully!")


# ---------- Show Total ----------
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


# ---------- Real-time Total Label ----------
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


# ---------- Monthly Report ----------
def show_monthly():
    month = datetime.now().strftime("%Y-%m")
    total = 0

    try:
        with open(FILE_NAME, "r") as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                if row[0].startswith(month):
                    total += float(row[1])
    except FileNotFoundError:
        pass

    messagebox.showinfo("Monthly Report", f"This Month's Total: {total} TK")


# ---------- Search: matches if keyword in any column ----------
def row_matches_keyword(row, keyword):
    key = keyword.lower()
    return (key in row[0].lower()) or (key in str(row[1]).lower()) or (key in row[2].lower()) or (key in row[3].lower())


# ---------- Search Handler (from entry/button) ----------
def perform_search():
    kw = search_var.get().strip()
    if kw == "":
        load_data()
        update_total_label()
        return

    def filter_func(row):
        return row_matches_keyword(row, kw)

    load_data(filter_func)
    # update total label to reflect filtered rows' sum
    total = 0
    try:
        with open(FILE_NAME, "r") as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                if filter_func(row):
                    total += float(row[1])
    except:
        pass
    total_label.config(text=f"Filtered Total: {total} TK")


# ---------- Live Search on key release ----------
def on_search_keyrelease(event):
    perform_search()


# ---------- Clear Search ----------
def clear_search():
    search_var.set("")
    load_data()
    update_total_label()


# ---------------- GUI PART ----------------

root = tk.Tk()
root.title("Advanced Expense Tracker with Search")
root.geometry("800x620")
root.resizable(False, False)

init_file()

title = tk.Label(root, text="Advanced Expense Tracker", font=("Arial", 18, "bold"))
title.pack(pady=10)

frame = tk.Frame(root)
frame.pack(pady=8)

# Amount
tk.Label(frame, text="Amount", font=("Arial", 12)).grid(row=0, column=0, sticky="e", padx=6, pady=4)
amount_entry = tk.Entry(frame, font=("Arial", 12), width=20)
amount_entry.grid(row=0, column=1, padx=6, pady=4)

# Category
tk.Label(frame, text="Category", font=("Arial", 12)).grid(row=1, column=0, sticky="e", padx=6, pady=4)
category_var = tk.StringVar()
category_menu = ttk.Combobox(frame, textvariable=category_var, font=("Arial", 12), width=18,
                             values=("Food", "Travel", "Shopping", "Bills", "Health", "Other"))
category_menu.grid(row=1, column=1, padx=6, pady=4)

# Note
tk.Label(frame, text="Note", font=("Arial", 12)).grid(row=2, column=0, sticky="e", padx=6, pady=4)
note_entry = tk.Entry(frame, font=("Arial", 12), width=45)
note_entry.grid(row=2, column=1, columnspan=3, padx=6, pady=4)

# Add Button
tk.Button(root, text="Add Expense", font=("Arial", 12), bg="#4CAF50", fg="white",
          command=add_expense, width=20).pack(pady=6)

# Search Frame
search_frame = tk.Frame(root)
search_frame.pack(pady=6, fill="x", padx=10)

tk.Label(search_frame, text="Search:", font=("Arial", 12)).pack(side="left", padx=(0,6))
search_var = tk.StringVar()
search_entry = tk.Entry(search_frame, textvariable=search_var, font=("Arial", 12), width=40)
search_entry.pack(side="left", padx=(0,6))
search_entry.bind("<KeyRelease>", on_search_keyrelease)  # live search

tk.Button(search_frame, text="Search", command=perform_search, bg="#2196F3", fg="white").pack(side="left", padx=6)
tk.Button(search_frame, text="Clear", command=clear_search, bg="#9E9E9E", fg="white").pack(side="left", padx=6)

# Table (with scrollbar)
table_frame = tk.Frame(root)
table_frame.pack(pady=8)

columns = ("Date", "Amount", "Category", "Note")
table = ttk.Treeview(table_frame, columns=columns, show="headings", height=14, selectmode="extended")

for col in columns:
    table.heading(col, text=col)
    table.column(col, width=180, anchor="w")

vsb = ttk.Scrollbar(table_frame, orient="vertical", command=table.yview)
table.configure(yscrollcommand=vsb.set)
vsb.pack(side="right", fill="y")
table.pack(side="left", fill="both", expand=True)

load_data()

# Total Label (Real Time)
total_label = tk.Label(root, text="Total Expenses: 0 TK", font=("Arial", 14, "bold"))
total_label.pack(pady=6)
update_total_label()

# Bottom Buttons
bottom_frame = tk.Frame(root)
bottom_frame.pack(pady=10)

tk.Button(bottom_frame, text="Show Total", command=calculate_total, bg="#673AB7", fg="white",
          width=15).grid(row=0, column=0, padx=8)

tk.Button(bottom_frame, text="Delete Selected", command=delete_expense, bg="#E91E63", fg="white",
          width=15).grid(row=0, column=1, padx=8)

tk.Button(bottom_frame, text="Monthly Report", command=show_monthly, bg="#009688", fg="white",
          width=15).grid(row=0, column=2, padx=8)

root.mainloop()
