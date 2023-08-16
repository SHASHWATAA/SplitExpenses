def calculate_expenses(expenses):
    # Create a dictionary to store the net amount owed by each person
    net_owed = {}

    # Calculate the total expenses paid by each person
    for expense, data in expenses.items():
        paid_by = data['Paid by']
        amount = data['Amount']
        divided_amongst = data['divided amongst']

        # Divide the expense equally among all the participants
        share = amount / len(divided_amongst)

        # Update the net_owed dictionary for each participant
        for person in divided_amongst:
            if person != paid_by:
                net_owed[person] = net_owed.get(person, 0) + share
            net_owed[paid_by] = net_owed.get(paid_by, 0) - share

    # Generate a list of transactions to settle the expenses
    transactions = []
    for person, amount in net_owed.items():
        if amount > 0:
            for debtor, debt in net_owed.items():
                if debt < 0:
                    settle_amount = min(amount, abs(debt))
                    amount -= settle_amount
                    net_owed[person] = amount
                    net_owed[debtor] += settle_amount
                    transactions.append((person, debtor, settle_amount))

    return transactions


# Calculate and print the transactions to settle the expenses
def calculate_owed_amount(expenses):
    people = set()

    for expense in expenses:
        people.add(expenses[expense]['Paid by'])
        for people_paid_for in expenses[expense]['Paid for']:
            people.add(people_paid_for)

    owed_amounts = {person: {"Total Owed": 0, "Debts": {other_item: 0 for other_item in people if other_item != person},
                             "Total Debt": 0} for person in people}

    for expense in expenses:
        expense_paid_by = expenses[expense]['Paid by']
        amount_owed_by_each = expenses[expense]['Amount'] / len(expenses[expense]['Paid for'])

        owed_amounts[expense_paid_by]['Total Owed'] = owed_amounts[expense_paid_by]['Total Owed'] + \
                                                      expenses[expense]['Amount'] - amount_owed_by_each

        for person in expenses[expense]['Paid for']:
            if person != expense_paid_by:
                owed_amounts[person]['Debts'][expense_paid_by] = owed_amounts[person]['Debts'][expense_paid_by] \
                                                                 + amount_owed_by_each

    for owed_amount in owed_amounts:
        data = owed_amounts[owed_amount]
        total_debts = 0

        for creditor in data['Debts']:
            total_debts = total_debts + data['Debts'][creditor]

        owed_amounts[owed_amount]['Total Debt'] = total_debts

    return owed_amounts


def settle_debts(debts):
    # define the debts and credits of each person
    debts_credits = debts

    # calculate the net balance for each person
    net_balances = {}
    for person, debt_credit in debts_credits.items():
        net_balances[person] = debt_credit['Total Owed'] - debt_credit['Total Debt']

    # sort the net balances in descending order
    sorted_net_balances = sorted(net_balances.items(), key=lambda x: x[1], reverse=True)

    # settle the debts
    while sorted_net_balances[0][1] > 0 and sorted_net_balances[-1][1] < 0:
        # find the person with the highest positive balance and the person with the lowest negative balance
        creditor = sorted_net_balances[0]
        debtor = sorted_net_balances[-1]

        # calculate the amount to be settled
        settle_amount = min(creditor[1], abs(debtor[1]))

        # print the settlement
        print(f"{debtor[0]} pays {creditor[0]} ${settle_amount:.2f}")

        # update the net balances
        sorted_net_balances[0] = (creditor[0], creditor[1] - settle_amount)
        sorted_net_balances[-1] = (debtor[0], debtor[1] + settle_amount)

        # resort the net balances
        sorted_net_balances = sorted(sorted_net_balances, key=lambda x: x[1], reverse=True)

    for person in debts:
        print(f'{person} is owed ${debts[person]["Total Owed"]} and owes ${debts[person]["Total Debt"]}')
    pass

expenses = {
    'Carpet': {
        'Paid by': 'Evan',
        'Amount': 48,
        'Paid for': ['Evan', 'Cherie', 'Sam', 'Ignacio', 'Sean']
    },
    'Carpet2': {
        'Paid by': 'Sean',
        'Amount': 12,
        'Paid for': ['Evan', 'Cherie', 'Sam', 'Ignacio', 'Sean']
    },
    'Dinner': {
        'Paid by': 'Ignacio',
        'Amount': 125,
        'Paid for': ['Evan', 'Cherie', 'Sam', 'Ignacio', 'Sean']
    },
    'breakfast': {
        'Paid by': 'Sam',
        'Amount': 50,
        'Paid for': ['Evan', 'Cherie', 'Sam', 'Ignacio', 'Sean']
    },
    'Movie': {
        'Paid by': 'Cherie',
        'Amount': 68,
        'Paid for': ['Evan', 'Cherie', 'Sam', 'Ignacio']
    },
}

# Given expenses dictionary
owed_amount = calculate_owed_amount(expenses)

settle_debts(owed_amount)
# print(owed_amount)
