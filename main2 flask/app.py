from flask import Flask, render_template, request
from waitress import serve

app = Flask(__name__)


@app.route('/')
def index():
    with open('names.txt', 'r') as f:
        names = f.read().splitlines()
    return render_template('index.html', names=names)


@app.route('/calculate', methods=['POST'])
def calculate():
    names_expenses = request.form.getlist('names_expenses[]')
    names_expenses = [(name.strip(), float(expense) if expense else 0) for name, expense in
                      zip(names_expenses[::2], names_expenses[1::2]) if name]

    total_expenses = sum(expense for name, expense in names_expenses)
    split_cost = total_expenses / len(names_expenses)

    balances = {name: expense - split_cost for name, expense in names_expenses}

    debtors = sorted([(name, balance) for name, balance in balances.items() if balance < 0], key=lambda x: x[1])
    creditors = sorted([(name, balance) for name, balance in balances.items() if balance > 0], key=lambda x: x[1],
                       reverse=True)

    result_text = "<ul>"
    while debtors and creditors:
        debtor, debt = debtors.pop(0)
        creditor, credit = creditors.pop(0)
        payment = min(abs(debt), abs(credit))
        result_text += f'<li>{debtor} to {creditor} ${payment:.2f}</li>'
        debt += payment
        credit -= payment
        if debt < 0:
            debtors.insert(0, (debtor, debt))
        if credit > 0:
            creditors.insert(0, (creditor, credit))
    result_text += "</ul>"

    return result_text


if __name__ == '__main__':
    # app.run()
    serve(app, host='0.0.0.0', port=5000)
