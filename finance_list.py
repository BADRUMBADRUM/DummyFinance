import json

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QWidget,
)

from finance_object import FinanceObject


class Financelist(QWidget):
    updateRequested = pyqtSignal()

    def __init__(self):
        super().__init__()

        with open("data.json", "r") as f:
            data = json.load(f)

        self.expenseObjects = []
        self.incomeObjects = []

        self.expenseLabel = QLabel("Expenses")
        self.incomeLabel = QLabel("Income")

        self.expenseLayout = QVBoxLayout()
        self.expenseLayout.addWidget(self.expenseLabel)
        self.expenseLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.incomeLayout = QVBoxLayout()
        self.incomeLayout.addWidget(self.incomeLabel)
        self.incomeLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        for item in data["expenses"]:
            obj = FinanceObject()
            obj.setValues(item["id"], item["name"], item["amount"], "red")
            self.expenseLayout.addWidget(obj)
            self.expenseObjects.append(obj)
            obj.deleteRequested.connect(self.RemoveExpensesWidget)
            obj.updateRequested.connect(self.updateRequestedByChild)

        for item in data["income"]:
            obj = FinanceObject()
            obj.setValues(item["id"], item["name"], item["amount"], "green")
            self.incomeLayout.addWidget(obj)
            self.incomeObjects.append(obj)
            obj.deleteRequested.connect(self.RemoveIncomeWidget)
            obj.updateRequested.connect(self.updateRequestedByChild)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(self.expenseLayout)
        mainLayout.addLayout(self.incomeLayout)
        self.setLayout(mainLayout)

    def add_finance(self, id, name, amount, incomeOrExpense):
        print(f"values in addFinance: {id} {amount} {incomeOrExpense}")
        obj = FinanceObject()
        redOrGreen = "red"
        if incomeOrExpense == "Income":
            redOrGreen = "green"

        obj.setValues(id, name, amount, redOrGreen)
        obj.updateRequested.connect(self.updateRequestedByChild)
        if incomeOrExpense == "Income":
            self.incomeLayout.addWidget(obj)
            self.incomeObjects.append(obj)
            obj.deleteRequested.connect(self.RemoveIncomeWidget)
        else:
            self.expenseLayout.addWidget(obj)
            self.expenseObjects.append(obj)
            obj.deleteRequested.connect(self.RemoveExpensesWidget)

    def RemoveExpensesWidget(self, obj):
        self.expenseLayout.removeWidget(obj)
        self.expenseObjects.remove(obj)
        obj.erase_object()
        obj.deleteLater()

    def RemoveIncomeWidget(self, obj):
        self.incomeLayout.removeWidget(obj)
        self.incomeObjects.remove(obj)
        obj.erase_object()
        obj.deleteLater()

    def updateRequestedByChild(self):
        print("update requested by child")
        self.updateRequested.emit()

    def get_monthly_savings(self):
        expense = 0
        income = 0
        for value in self.expenseObjects:
            expense += value.financeAmount.value()

        for value in self.incomeObjects:
            income += value.financeAmount.value()

        monthly_savings = income - expense
        return monthly_savings
