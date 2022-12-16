import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QSpacerItem, QSizePolicy

class Field(QWidget, server):
    def __init__(self, rows, columns):
        super(QWidget, self).__init__()
        self.rows = rows
        self.columns = columns
        self.initShootingPhase()

    def initShootingPhase(self):
        grid = QGridLayout()
        self.setLayout(grid)
        grid.setSpacing(0)

        for width in range(self.rows):
            for height in range(self.columns):
                button = QPushButton()
                grid.addWidget(button, width, height)
                button.setText()
                button.clicked.connect(self.on_click(width, height))
        self.show()

    def on_click(self, width, height):
        print("Clicked", width, height)
        return lambda: self.on_click(width, height)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    field = Field(10, 10)
    sys.exit(app.exec())