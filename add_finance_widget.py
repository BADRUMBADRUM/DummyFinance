import json

from PyQt5.QtWidgets import (
    QComboBox,
    QDoubleSpinBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

dataFileName = "data.json"


class FinanceWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.label = QLabel("Add finance")

        self.id = 0
        self.incomeOrExpense = QComboBox()
        self.incomeOrExpense.addItem("Expense")
        self.incomeOrExpense.addItem("Income")
        self.financeName = QLineEdit()
        self.financeName.setPlaceholderText("Finance name")
        self.financeAmount = QDoubleSpinBox()
        self.financeAmount.setDecimals(2)
        self.financeAmount.setMinimum(0.00)
        self.financeAmount.setMaximum(100000)
        self.financeAmount.setPrefix("$ ")
        self.financeAmount.setSingleStep(0.50)

        horizontalLayout1 = QHBoxLayout()
        horizontalLayout1.addWidget(self.incomeOrExpense)
        horizontalLayout1.addWidget(self.financeName)
        horizontalLayout1.addWidget(self.financeAmount)

        self.addButton = QPushButton("Add")
        self.addButton.clicked.connect(self.CheckAndAddFinance)
        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.clicked.connect(self.ClearValuesAndHideWidget)

        horizontalLayout2 = QHBoxLayout()
        horizontalLayout2.addWidget(self.addButton)
        horizontalLayout2.addWidget(self.cancelButton)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addLayout(horizontalLayout1)
        layout.addLayout(horizontalLayout2)
        self.setLayout(layout)

    def ClearValuesAndHideWidget(self):
        self.financeName.setText("")
        self.financeAmount.setValue(0.00)
        self.hide()

    def ValidateFinance(self):
        if self.financeName.text() == "":
            print("No finance name was given")
            self.ClearValuesAndHideWidget()
            return False

        if self.financeAmount.value() < 1.00:
            print(
                "Finance value: "
                + self.financeAmount.value().__str__()
                + " is too small "
            )
            self.ClearValuesAndHideWidget()
            return False

        return True

    def CheckAndAddFinance(self):
        if not self.ValidateFinance():
            return

        with open(dataFileName, "r") as f:
            data = json.load(f)

        if self.incomeOrExpense.currentText() == "Income":
            target_list = data["income"]
        else:
            target_list = data["expenses"]

        if target_list:
            max_id = max(item.get("id", 0) for item in target_list)
        else:
            max_id = 0

        self.id = max_id + 1
        new_entry = {
            "id": self.id,
            "name": self.financeName.text(),
            "amount": self.financeAmount.value(),
        }

        if self.incomeOrExpense.currentText() == "Income":
            data["income"].append(new_entry)
        else:
            data["expenses"].append(new_entry)

        with open(dataFileName, "w") as f:
            json.dump(data, f, indent=4)

        print("Finance added succesfully")
