import sqlite3
from expense import Expense


DATABASE_NAME = "expenses.db"


# =========================
# DATABASE CONNECTION
# =========================

def get_connection():

    return sqlite3.connect(DATABASE_NAME)


# =========================
# CREATE DATABASE
# =========================

def create_database():

    connection = get_connection()

    cursor = connection.cursor()

    # Create table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT
        )
    """)

    # Check existing columns
    cursor.execute(
        "PRAGMA table_info(expenses)"
    )

    columns = [
        column[1]
        for column in cursor.fetchall()
    ]

    # Add date column if old database
    # doesn't have it
    if "date" not in columns:

        cursor.execute("""
            ALTER TABLE expenses
            ADD COLUMN date TEXT
        """)

    connection.commit()

    connection.close()


# =========================
# ADD EXPENSE
# =========================

def add_expense(expense, date):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO expenses
        (name, amount, category, date)

        VALUES (?, ?, ?, ?)
    """, (
        expense.name,
        expense.amount,
        expense.category,
        date
    ))

    connection.commit()

    connection.close()


# =========================
# GET ALL EXPENSES
# =========================

def get_expenses():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            name,
            amount,
            category,
            date

        FROM expenses

        ORDER BY id DESC
    """)

    expenses = cursor.fetchall()

    connection.close()

    return expenses


# =========================
# UPDATE EXPENSE
# =========================

def update_expense(
    expense_id,
    name,
    amount,
    category,
    date
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        UPDATE expenses

        SET
            name = ?,
            amount = ?,
            category = ?,
            date = ?

        WHERE id = ?
    """, (
        name,
        amount,
        category,
        date,
        expense_id
    ))

    connection.commit()

    connection.close()


# =========================
# DELETE EXPENSE
# =========================

def delete_expense(expense_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM expenses

        WHERE id = ?
    """, (expense_id,))

    connection.commit()

    connection.close()


# =========================
# SEARCH EXPENSES
# =========================

def search_expenses(
    search_text="",
    category="All Categories"
):

    connection = get_connection()

    cursor = connection.cursor()

    search_text = f"%{search_text}%"

    if category == "All Categories":

        cursor.execute("""
            SELECT
                id,
                name,
                amount,
                category,
                date

            FROM expenses

            WHERE name LIKE ?

            ORDER BY id DESC
        """, (search_text,))

    else:

        cursor.execute("""
            SELECT
                id,
                name,
                amount,
                category,
                date

            FROM expenses

            WHERE name LIKE ?
            AND category = ?

            ORDER BY id DESC
        """, (
            search_text,
            category
        ))

    expenses = cursor.fetchall()

    connection.close()

    return expenses


# =========================
# CATEGORY TOTALS
# =========================

def get_category_totals():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            category,
            SUM(amount)

        FROM expenses

        GROUP BY category
    """)

    totals = cursor.fetchall()

    connection.close()

    return totals


# =========================
# MONTHLY TOTAL
# =========================

def get_monthly_total(
    month
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            SUM(amount)

        FROM expenses

        WHERE date LIKE ?
    """, (
        f"{month}%",
    ))

    result = cursor.fetchone()

    connection.close()

    if result[0] is None:

        return 0

    return result[0]