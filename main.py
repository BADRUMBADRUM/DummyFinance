#!/usr/bin/env python3
import sys

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from app.add_finance_widget import FinanceWindow
from app.finance_list import Financelist


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Dummy Finance")

        self.button = QPushButton("Add finance")
        self.button.clicked.connect(self.the_button_was_clicked)
        self.setMouseTracking(True)

        self.addFinanceWindow = FinanceWindow()
        self.addFinanceWindow.hide()
        self.addFinanceWindow.addButton.clicked.connect(self.add_button_was_clicked)

        self.financeList = Financelist()
        self.financeList.show()
        self.financeList.updateRequested.connect(self.update_monthly_savings)

        self.monthlySavings = QLabel()
        self.update_monthly_savings()

        layout = QVBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.addFinanceWindow)
        layout.addWidget(self.financeList, stretch=1)
        layout.addWidget(self.monthlySavings, alignment=Qt.AlignmentFlag.AlignCenter)
        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)
        self.setFixedSize(QSize(1000, 800))

    def the_button_was_clicked(self):
        self.addFinanceWindow.show()
        print(self.button)

    def add_button_was_clicked(self):
        print("add button was clicked")
        if self.addFinanceWindow.ValidateFinance():
            self.financeList.add_finance(
                self.addFinanceWindow.id,
                self.addFinanceWindow.financeName.text(),
                self.addFinanceWindow.financeAmount.value(),
                self.addFinanceWindow.incomeOrExpense.currentText(),
            )
            self.addFinanceWindow.ClearValuesAndHideWidget()
            self.update_monthly_savings()

    def update_monthly_savings(self):
        monthly_savings = self.financeList.get_monthly_savings()
        color = ""
        if monthly_savings < 0:
            color = "#fb4934"
        else:
            color = "#8ec07c"

        self.monthlySavings.setText(f"Monthly savings: ${monthly_savings:,.2f}")
        self.monthlySavings.setStyleSheet(f"""
            background-color: #282828;
            border-radius: 8px;
            color: {color};
            padding: 4px 8px;
            """)
        self.monthlySavings.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed
        )
        self.monthlySavings.adjustSize()
        self.monthlySavings.setAlignment(Qt.AlignmentFlag.AlignCenter)


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet("""
    * {
        color: #fbf1c7;
        font-size: 20px;
    }
    QPushButton{
        border: solid;
        border-radius: 8px;
        background-color: #282828;
    }
    QPushButton:hover{
        background-color: #504945;
    }
    """)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
