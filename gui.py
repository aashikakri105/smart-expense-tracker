import tkinter as tk
from tkinter import ttk, messagebox

from expense import Expense

from database import (
    create_database,
    add_expense,
    get_expenses,
    update_expense,
    delete_expense,
    get_total_expense
)


# ==========================================
# MONTHLY BUDGET
# ==========================================

BUDGET = 30000


# ==========================================
# DASHBOARD
# ==========================================

def update_dashboard():

    total = get_total_expense()

    remaining = BUDGET - total

    total_label.config(
        text=f"Total Spent\n₹{total:.2f}"
    )

    budget_label.config(
        text=f"Monthly Budget\n₹{BUDGET:.2f}"
    )

    remaining_label.config(
        text=f"Remaining\n₹{remaining:.2f}"
    )


# ==========================================
# CLEAR FIELDS
# ==========================================

def clear_fields():

    name_entry.delete(
        0,
        tk.END
    )

    amount_entry.delete(
        0,
        tk.END
    )

    category_combo.current(0)


# ==========================================
# ADD EXPENSE
# ==========================================

def add_expense_to_database():

    name = name_entry.get().strip()

    amount = amount_entry.get().strip()

    category = category_combo.get()

    # Check empty fields
    if not name or not amount or not category:

        messagebox.showwarning(
            "Missing Information",
            "Please fill in all fields."
        )

        return

    # Validate amount
    try:

        amount = float(amount)

        if amount <= 0:
            raise ValueError

    except ValueError:

        messagebox.showerror(
            "Invalid Amount",
            "Please enter a valid positive amount."
        )

        return

    # Create Expense object
    expense = Expense(
        name=name,
        amount=amount,
        category=category
    )

    # Save expense
    add_expense(expense)

    messagebox.showinfo(
        "Success",
        "Expense added successfully! ✅"
    )

    clear_fields()

    # Refresh table
    show_expenses()

    # Refresh dashboard
    update_dashboard()


# ==========================================
# SHOW EXPENSES
# ==========================================

def show_expenses():

    # Delete old rows
    for row in expense_table.get_children():

        expense_table.delete(row)

    # Get expenses from database
    expenses = get_expenses()

    # Database returns tuples:
    # (id, name, amount, category)

    for expense in expenses:

        expense_table.insert(
            "",
            tk.END,
            values=expense
        )


# ==========================================
# EDIT EXPENSE
# ==========================================

def edit_selected_expense():

    selected = expense_table.selection()

    # Check selection
    if not selected:

        messagebox.showwarning(
            "No Selection",
            "Please select an expense to edit."
        )

        return

    # Get selected row
    item = expense_table.item(
        selected[0]
    )

    values = item["values"]

    expense_id = values[0]

    name = name_entry.get().strip()

    amount = amount_entry.get().strip()

    category = category_combo.get()

    # Check empty fields
    if not name or not amount or not category:

        messagebox.showwarning(
            "Missing Information",
            "Please fill in all fields."
        )

        return

    # Validate amount
    try:

        amount = float(amount)

        if amount <= 0:
            raise ValueError

    except ValueError:

        messagebox.showerror(
            "Invalid Amount",
            "Please enter a valid amount."
        )

        return

    # Update database
    update_expense(
        expense_id,
        name,
        amount,
        category
    )

    messagebox.showinfo(
        "Success",
        "Expense updated successfully! ✅"
    )

    clear_fields()

    # Refresh
    show_expenses()

    update_dashboard()


# ==========================================
# DELETE EXPENSE
# ==========================================

def delete_selected_expense():

    selected = expense_table.selection()

    # Check selection
    if not selected:

        messagebox.showwarning(
            "No Selection",
            "Please select an expense to delete."
        )

        return

    # Get selected row
    item = expense_table.item(
        selected[0]
    )

    values = item["values"]

    expense_id = values[0]

    # Confirmation
    confirm = messagebox.askyesno(
        "Delete Expense",
        "Are you sure you want to delete this expense?"
    )

    if confirm:

        delete_expense(
            expense_id
        )

        messagebox.showinfo(
            "Success",
            "Expense deleted successfully! 🗑️"
        )

        clear_fields()

        # Refresh table
        show_expenses()

        # Refresh dashboard
        update_dashboard()


# ==========================================
# SELECT TABLE ROW
# ==========================================

def fill_fields_from_table(event):

    selected = expense_table.selection()

    if not selected:
        return

    item = expense_table.item(
        selected[0]
    )

    values = item["values"]

    # Database tuple:
    # ID, Name, Amount, Category

    name = values[1]

    amount = values[2]

    category = values[3]

    # Clear fields
    name_entry.delete(
        0,
        tk.END
    )

    amount_entry.delete(
        0,
        tk.END
    )

    # Fill fields
    name_entry.insert(
        0,
        name
    )

    amount_entry.insert(
        0,
        amount
    )

    category_combo.set(
        category
    )


# ==========================================
# PIE CHART
# ==========================================

def show_expense_chart():

    import matplotlib.pyplot as plt

    # Get expenses
    expenses = get_expenses()

    # Check data
    if not expenses:

        messagebox.showinfo(
            "No Data",
            "No expenses available for chart."
        )

        return

    # Category-wise totals
    category_totals = {}

    for expense in expenses:

        # IMPORTANT:
        # Database returns tuple:
        #
        # (id, name, amount, category)

        expense_id, expense_name, amount, category = expense

        amount = float(amount)

        if category in category_totals:

            category_totals[category] += amount

        else:

            category_totals[category] = amount

    # Create figure
    plt.figure(
        figsize=(7, 7)
    )

    # Pie chart
    plt.pie(
        category_totals.values(),
        labels=category_totals.keys(),
        autopct="%1.1f%%",
        startangle=90
    )

    plt.title(
        "Expense by Category"
    )

    plt.tight_layout()

    plt.show()


# ==========================================
# MAIN
# ==========================================

def main():

    global name_entry
    global amount_entry
    global category_combo
    global expense_table

    global total_label
    global budget_label
    global remaining_label

    # Create database
    create_database()

    # Main window
    window = tk.Tk()

    window.title(
        "Smart Expense & Budget Manager"
    )

    window.geometry(
        "900x800"
    )

    # ======================================
    # TITLE
    # ======================================

    title_label = tk.Label(
        window,
        text="💰 Smart Expense Manager",
        font=("Arial", 24, "bold")
    )

    title_label.pack(
        pady=20
    )

    # ======================================
    # DASHBOARD
    # ======================================

    dashboard_frame = tk.Frame(
        window
    )

    dashboard_frame.pack(
        pady=10
    )

    # Total Spent
    total_label = tk.Label(
        dashboard_frame,
        text="Total Spent\n₹0.00",
        font=("Arial", 14, "bold"),
        width=20,
        height=3,
        relief="groove"
    )

    total_label.grid(
        row=0,
        column=0,
        padx=10
    )

    # Budget
    budget_label = tk.Label(
        dashboard_frame,
        text=f"Monthly Budget\n₹{BUDGET:.2f}",
        font=("Arial", 14, "bold"),
        width=20,
        height=3,
        relief="groove"
    )

    budget_label.grid(
        row=0,
        column=1,
        padx=10
    )

    # Remaining
    remaining_label = tk.Label(
        dashboard_frame,
        text=f"Remaining\n₹{BUDGET:.2f}",
        font=("Arial", 14, "bold"),
        width=20,
        height=3,
        relief="groove"
    )

    remaining_label.grid(
        row=0,
        column=2,
        padx=10
    )

    # ======================================
    # INPUT FRAME
    # ======================================

    input_frame = tk.Frame(
        window
    )

    input_frame.pack(
        pady=15
    )

    # Expense Name
    name_label = tk.Label(
        input_frame,
        text="Expense Name:"
    )

    name_label.grid(
        row=0,
        column=0,
        padx=10,
        pady=8,
        sticky="w"
    )

    name_entry = tk.Entry(
        input_frame,
        width=40
    )

    name_entry.grid(
        row=0,
        column=1,
        padx=10,
        pady=8
    )

    # Amount
    amount_label = tk.Label(
        input_frame,
        text="Amount:"
    )

    amount_label.grid(
        row=1,
        column=0,
        padx=10,
        pady=8,
        sticky="w"
    )

    amount_entry = tk.Entry(
        input_frame,
        width=40
    )

    amount_entry.grid(
        row=1,
        column=1,
        padx=10,
        pady=8
    )

    # Category
    category_label = tk.Label(
        input_frame,
        text="Category:"
    )

    category_label.grid(
        row=2,
        column=0,
        padx=10,
        pady=8,
        sticky="w"
    )

    category_combo = ttk.Combobox(
        input_frame,
        values=[
            "🍕 Food",
            "🏚️ Home",
            "👔 Work",
            "🎉 Fun",
            "✨ Misc"
        ],
        state="readonly",
        width=37
    )

    category_combo.grid(
        row=2,
        column=1,
        padx=10,
        pady=8
    )

    category_combo.current(0)

    # ======================================
    # BUTTON FRAME
    # ======================================

    button_frame = tk.Frame(
        window
    )

    button_frame.pack(
        pady=15
    )

    # Add
    add_button = tk.Button(
        button_frame,
        text="➕ Add Expense",
        width=18,
        command=add_expense_to_database
    )

    add_button.grid(
        row=0,
        column=0,
        padx=5
    )

    # Edit
    edit_button = tk.Button(
        button_frame,
        text="✏️ Edit Selected",
        width=18,
        command=edit_selected_expense
    )

    edit_button.grid(
        row=0,
        column=1,
        padx=5
    )

    # Delete
    delete_button = tk.Button(
        button_frame,
        text="🗑️ Delete Selected",
        width=18,
        command=delete_selected_expense
    )

    delete_button.grid(
        row=0,
        column=2,
        padx=5
    )

    # Clear
    clear_button = tk.Button(
        button_frame,
        text="Clear",
        width=18,
        command=clear_fields
    )

    clear_button.grid(
        row=0,
        column=3,
        padx=5
    )

    # Chart
    chart_button = tk.Button(
        button_frame,
        text="📊 View Chart",
        width=18,
        command=show_expense_chart
    )

    chart_button.grid(
        row=1,
        column=0,
        columnspan=4,
        pady=10
    )

    # ======================================
    # HISTORY TITLE
    # ======================================

    history_label = tk.Label(
        window,
        text="📋 Expense History",
        font=("Arial", 18, "bold")
    )

    history_label.pack(
        pady=10
    )

    # ======================================
    # TABLE
    # ======================================

    table_frame = tk.Frame(
        window
    )

    table_frame.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=10
    )

    columns = (
        "ID",
        "Name",
        "Amount",
        "Category"
    )

    expense_table = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings",
        height=12
    )

    # Headings

    expense_table.heading(
        "ID",
        text="ID"
    )

    expense_table.heading(
        "Name",
        text="Name"
    )

    expense_table.heading(
        "Amount",
        text="Amount"
    )

    expense_table.heading(
        "Category",
        text="Category"
    )

    # Column sizes

    expense_table.column(
        "ID",
        width=50,
        anchor="center"
    )

    expense_table.column(
        "Name",
        width=220
    )

    expense_table.column(
        "Amount",
        width=130,
        anchor="center"
    )

    expense_table.column(
        "Category",
        width=200
    )

    # ======================================
    # SCROLLBAR
    # ======================================

    scrollbar = ttk.Scrollbar(
        table_frame,
        orient="vertical",
        command=expense_table.yview
    )

    expense_table.configure(
        yscrollcommand=scrollbar.set
    )

    expense_table.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    # ======================================
    # TABLE CLICK
    # ======================================

    expense_table.bind(
        "<ButtonRelease-1>",
        fill_fields_from_table
    )

    # ======================================
    # LOAD DATA
    # ======================================

    show_expenses()

    update_dashboard()

    # ======================================
    # START GUI
    # ======================================

    window.mainloop()


# ==========================================
# RUN PROGRAM
# ==========================================

if __name__ == "__main__":
    main()