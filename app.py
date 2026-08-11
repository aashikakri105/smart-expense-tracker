from flask import Flask, render_template, request, redirect, Response
import csv
import io
from datetime import date

from database import (
    create_database,
    add_expense,
    get_expenses,
    update_expense,
    delete_expense,
    get_category_totals,
    search_expenses,
    get_monthly_total
)

from expense import Expense


app = Flask(__name__)


# =========================
# CREATE DATABASE
# =========================

create_database()


# =========================
# HOME PAGE
# =========================

@app.route("/")
def home():

    search_text = request.args.get(
        "search",
        ""
    )

    category = request.args.get(
        "category",
        "All Categories"
    )

    # Search / Filter
    if search_text or category != "All Categories":

        expenses = search_expenses(
            search_text,
            category
        )

    else:

        expenses = get_expenses()


    # =========================
    # TOTAL EXPENSE
    # =========================

    total_spent = sum(
        expense[2]
        for expense in expenses
    )


    # =========================
    # MONTHLY BUDGET
    # =========================

    budget = 30000


    # =========================
    # REMAINING BUDGET
    # =========================

    remaining = budget - total_spent


    # =========================
    # CURRENT MONTH
    # =========================

    current_month = date.today().strftime(
        "%Y-%m"
    )


    # =========================
    # MONTHLY TOTAL
    # =========================

    monthly_total = get_monthly_total(
        current_month
    )


    # =========================
    # CATEGORY TOTALS
    # =========================

    category_totals = get_category_totals()


    categories = [
        item[0]
        for item in category_totals
    ]


    amounts = [
        item[1]
        for item in category_totals
    ]


    # =========================
    # SEND DATA TO HTML
    # =========================

    return render_template(
        "index.html",

        expenses=expenses,

        total_spent=total_spent,

        budget=budget,

        remaining=remaining,

        monthly_total=monthly_total,

        current_month=current_month,

        categories=categories,

        amounts=amounts,

        search_text=search_text,

        selected_category=category
    )


# =========================
# ADD EXPENSE
# =========================

@app.route(
    "/add",
    methods=["POST"]
)
def add():

    name = request.form["name"]


    amount = float(
        request.form["amount"]
    )


    category = request.form["category"]


    # Get date from form
    expense_date = request.form.get(
        "date"
    )


    # If no date is selected,
    # use today's date
    if not expense_date:

        expense_date = date.today().isoformat()


    expense = Expense(
        name=name,
        amount=amount,
        category=category
    )


    add_expense(
        expense,
        expense_date
    )


    return redirect("/")


# =========================
# UPDATE EXPENSE
# =========================

@app.route(
    "/edit/<int:expense_id>",
    methods=["POST"]
)
def edit(expense_id):

    name = request.form["name"]


    amount = float(
        request.form["amount"]
    )


    category = request.form["category"]


    expense_date = request.form.get(
        "date"
    )


    if not expense_date:

        expense_date = date.today().isoformat()


    update_expense(
        expense_id,
        name,
        amount,
        category,
        expense_date
    )


    return redirect("/")


# =========================
# DELETE EXPENSE
# =========================

@app.route(
    "/delete/<int:expense_id>",
    methods=["POST"]
)
def delete(expense_id):

    delete_expense(
        expense_id
    )


    return redirect("/")


# =========================
# EXPORT CSV
# =========================

@app.route("/export")
def export_csv():

    expenses = get_expenses()


    output = io.StringIO()


    writer = csv.writer(
        output
    )


    # CSV Header

    writer.writerow([
        "ID",
        "Name",
        "Amount",
        "Category",
        "Date"
    ])


    # CSV Data

    for expense in expenses:

        writer.writerow([
            expense[0],
            expense[1],
            expense[2],
            expense[3],
            expense[4]
        ])


    response = Response(
        output.getvalue(),
        mimetype="text/csv"
    )


    response.headers[
        "Content-Disposition"
    ] = (
        "attachment; "
        "filename=expenses.csv"
    )


    return response


# =========================
# RUN APPLICATION
# =========================

if __name__ == "__main__":

    app.run(
        debug=True
    )