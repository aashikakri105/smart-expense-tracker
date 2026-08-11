from expense import Expense
import calendar
import datetime


def main():
    print("🏃 Program is running!")

    expense_file_path = "expense.csv"
    budget = 3000000

    expense = expense_kitna_hua()

    file_m_save_kro(expense, expense_file_path)

    summarize_expense(expense_file_path, budget)  #FOR DELETE EXPENSE SUMMARY


def expense_kitna_hua():
    print("\nHow much did you spend?")

    expense_name = input("What did you spend money on? ")

    expense_amount = float(
        input("How much did you spend? ₹")
    )

    print(
        f"Expense name: {expense_name}, Amount: ₹{expense_amount}"
    )

    expense_categories = [
        "🍕 Food",
        "🏚️ Home",
        "👔 Work",
        "🎉 Fun",
        "✨ Misc",
    ]

    while True:
        print("\nWhich category does this expense belong to?")

        for i, category_name in enumerate(expense_categories):
            print(f"{i + 1}. {category_name}")

        value_range = f"[1-{len(expense_categories)}]"

        selected_index = int(
            input(
                f"Please select a category {value_range}: "
            )
        )

        if selected_index in range(
            1, len(expense_categories) + 1
        ):

            selected_category = expense_categories[
                selected_index - 1
            ]

            print(f"Selected category: {selected_category}")

            new_expense = Expense(
                name=expense_name,
                category=selected_category,
                amount=expense_amount
            )

            return new_expense

        else:
            print("❌ Invalid category. Please try again.")


def file_m_save_kro(
    expense: Expense,
    expense_file_path
):
    print(
        f"Saving expense: {expense} "
        f"to {expense_file_path}"
    )

    with open(
        expense_file_path,
        "a",
        encoding="utf-8"
    ) as f:

        f.write(
            f"{expense.name},"
            f"{expense.amount},"
            f"{expense.category}\n"
        )


def summarize_expense(
    expense_file_path,
    budget
):
    print("\n========== Expense Summary ==========")

    expenses = []

    # Read CSV file using UTF-8
    with open(
        expense_file_path,
        "r",
        encoding="utf-8"
    ) as f:

        lines = f.readlines()

    for line in lines:

        expense_name, expense_amount, expense_category = (
            line.strip().split(",")
        )

        print(
            f"{expense_name} | "
            f"₹{expense_amount} | "
            f"{expense_category}"
        )

        line_expense = Expense(
            name=expense_name,
            amount=float(expense_amount),
            category=expense_category
        )

        expenses.append(line_expense)

    # Category-wise expense
    amount_by_category = {}

    for expense in expenses:

        key = expense.category

        if key in amount_by_category:
            amount_by_category[key] += expense.amount
        else:
            amount_by_category[key] = expense.amount

    print("\n========== Category-wise Expenses ==========")

    for key, amount in amount_by_category.items():
        print(f"{key}: ₹{amount:.2f}")

    # Total expense
    total_spent = sum(
        x.amount for x in expenses
    )

    print(
        f"\nTotal spent: ₹{total_spent:.2f}"
    )

    # Remaining Budget
    remaining_budget = budget - total_spent

    print(
        f"Remaining budget: ₹{remaining_budget:.2f}"
    )

    # Remaining days
    now = datetime.datetime.now()

    days_in_month = calendar.monthrange(
        now.year,
        now.month
    )[1]

    remaining_days = days_in_month - now.day

    print(
        f"Remaining days in this month: "
        f"{remaining_days}"
    )

    # Daily Budget
    if remaining_days > 0:

        daily_budget = (
            remaining_budget / remaining_days
        )

        print(
            red(
                f"Daily budget: ₹{daily_budget:.2f}"
            )
        )


def red(text):
    return f"\033[91m{text}\033[0m"


if __name__ == "__main__":
    main()