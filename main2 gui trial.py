import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QHBoxLayout


class ExpenseSplitterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.names_expenses = []
        self.init_ui()

    def init_ui(self):
        self.main_layout = QVBoxLayout()

        for _ in range(4):
            self.add_row()

        self.add_row_button = QPushButton("Add Row")
        self.add_row_button.clicked.connect(self.add_row)
        self.main_layout.addWidget(self.add_row_button)

        self.calculate_button = QPushButton("Calculate")
        self.calculate_button.clicked.connect(self.calculate_expenses)
        self.main_layout.addWidget(self.calculate_button)



        self.result_label = QLabel()
        self.main_layout.addWidget(self.result_label)

        container = QWidget()
        container.setLayout(self.main_layout)
        self.setCentralWidget(container)

        self.setWindowTitle("Expense Splitter")
        self.setGeometry(100, 100, 400, 300)

    def add_row(self):
        row_layout = QHBoxLayout()

        name_line_edit = QLineEdit()
        name_line_edit.setPlaceholderText("Enter name")
        row_layout.addWidget(name_line_edit)

        expense_line_edit = QLineEdit()
        expense_line_edit.setPlaceholderText("Enter expense")
        row_layout.addWidget(expense_line_edit)

        self.names_expenses.append((name_line_edit, expense_line_edit))
        self.main_layout.insertLayout(len(self.main_layout) - 3, row_layout)

        name_line_edit.setFocus()  # Set focus to the new name input

    def calculate_expenses(self):
        self.names_expenses = [(name_edit.text().strip(), expense_edit.text()) for name_edit, expense_edit in
                               self.names_expenses]
        self.names_expenses = [(name, float(expense) if expense.replace(".", "", 1).isdigit() else 0) for name, expense
                               in self.names_expenses if name]

        total_expenses = sum(expense for name, expense in self.names_expenses)
        split_cost = total_expenses / len(self.names_expenses)

        balances = {name: expense - split_cost for name, expense in self.names_expenses}

        debtors = sorted([(name, balance) for name, balance in balances.items() if balance < 0], key=lambda x: x[1])
        creditors = sorted([(name, balance) for name, balance in balances.items() if balance > 0], key=lambda x: x[1],
                           reverse=True)

        result_text = ""
        while debtors and creditors:
            debtor, debt = debtors.pop(0)
            creditor, credit = creditors.pop(0)
            payment = min(abs(debt), abs(credit))
            result_text += f'{debtor} to {creditor} ${payment:.2f}\n'
            debt += payment
            credit -= payment
            if debt < 0:
                debtors.insert(0, (debtor, debt))
            if credit > 0:
                creditors.insert(0, (creditor, credit))

        self.result_label.setText(result_text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ExpenseSplitterApp()
    window.show()
    sys.exit(app.exec_())
