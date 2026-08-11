from database import search_expenses, get_expenses, delete_expense


# =========================
# SEARCH TEST
# =========================

print("Search Results:")

expenses = search_expenses("pizza")

for expense in expenses:
    print(expense)


# =========================
# DELETE TEST
# =========================

print("\nBefore Delete:")

expenses = get_expenses()

for expense in expenses:
    print(expense)


delete_expense(1)


print("\nAfter Delete:")

expenses = get_expenses()

for expense in expenses:
    print(expense)