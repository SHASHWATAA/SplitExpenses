expenses = {
    'Shash': 98,
    'Soum': 60,
    'Rujj': 0,
    'Uni': 0,
}


total_expenses = sum(expenses.values())
split_cost = total_expenses / len(expenses)

balances = {person: spent - split_cost for person, spent in expenses.items()}

debtors = sorted([(person, balance) for person, balance in balances.items() if balance < 0], key=lambda x: x[1])
creditors = sorted([(person, balance) for person, balance in balances.items() if balance > 0], key=lambda x: x[1],
                   reverse=True)

while debtors and creditors:
    debtor, debt = debtors.pop(0)
    creditor, credit = creditors.pop(0)
    payment = min(abs(debt), abs(credit))
    print(f'{debtor} to {creditor} ${payment:.2f}')
    debt += payment
    credit -= payment
    if debt < 0:
        debtors.insert(0, (debtor, debt))
    if credit > 0:
        creditors.insert(0, (creditor, credit))
