import json

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (
    QDoubleSpinBox,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QWidget,
)

from app.config import DATA_FILE


class FinanceObject(QWidget):
    deleteRequested = pyqtSignal(object)
    updateRequested = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.id = 0
        self.incomeOrExpense = "Income"
        self.financeName = QLineEdit()
        self.financeName.setPlaceholderText("Finance name")
        self.financeAmount = QDoubleSpinBox()
        self.financeAmount.setDecimals(2)
        self.financeAmount.setMinimum(0.00)
        self.financeAmount.setMaximum(100000)
        self.financeAmount.setPrefix("$ ")
        self.financeAmount.setSingleStep(0.50)

        self.eraseButton = QPushButton("Delete")
        self.eraseButton.setStyleSheet("""
            padding: 4px 8px;
            """)
        self.eraseButton.clicked.connect(lambda: self.deleteRequested.emit(self))

        self.editButton = QPushButton("Edit")
        self.editButton.setStyleSheet("""
            padding: 4px 8px;
            """)
        self.editButton.clicked.connect(self.edit_button_clicked)

        layout = QHBoxLayout()
        layout.addWidget(self.financeName)
        layout.addWidget(self.financeAmount)
        layout.addWidget(self.editButton)
        layout.addWidget(self.eraseButton)
        self.setLayout(layout)

    def setValues(self, id, name, amount, color):
        self.id = id
        self.financeName.setText(name)
        self.financeName.setEnabled(False)
        self.financeAmount.setValue(amount)
        self.financeAmount.setEnabled(False)
        cssColor = ""
        if color == "red":
            self.incomeOrExpense = "Expense"
            cssColor = "#fb4934"
        else:
            self.incomeOrExpense = "Income"
            cssColor = "#8ec07c"
        self.financeAmount.setStyleSheet("color: " + cssColor + ";")

    def edit_button_clicked(self):
        if not self.financeName.isEnabled():
            self.financeName.setEnabled(True)
            self.financeAmount.setEnabled(True)
            self.editButton.setText("Save")
        else:
            self.save_object_values()
            self.financeName.setEnabled(False)
            self.financeAmount.setEnabled(False)
            self.editButton.setText("Edit")
            self.updateRequested.emit()

    def save_object_values(self):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)

        entry = {
            "id": self.id,
            "name": self.financeName.text(),
            "amount": self.financeAmount.value(),
        }

        key = "income" if self.incomeOrExpense == "Income" else "expenses"
        for i, entry in enumerate(data[key]):
            if entry["id"] == self.id:
                data[key][i] = entry
                break

        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)

    def erase_object(self):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)

        key = "income" if self.incomeOrExpense == "Income" else "expenses"
        for i, entry in enumerate(data[key]):
            if entry["id"] == self.id:
                del data[key][i]
                break

        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)

        self.updateRequested.emit()
