import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QSpacerItem, QSizePolicy

class Field(QWidget):
    def __init__(self, rows, columns, filler):
        super(QWidget, self).__init__()
        self.rows = rows
        self.columns = columns
        self.filler = filler
        self.initGrid()

    def initGrid(self):
        grid = QGridLayout()
        self.setLayout(grid)
        grid.setSpacing(0)

        for width in range(self.rows):
            for height in range(self.columns):
                # Create button and its policy
                button = QPushButton()
                button.setMinimumSize(20, 20)
                button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
                grid.addWidget(button, width, height)
                button.setText(self.filler)
                button.clicked.connect(self.on_click(width, height))
        self.resize(400, 400)
        self.show()

    def on_click(self, width, height):
        return lambda: print(width, height)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    field = Field(10, 10, "?")
    sys.exit(app.exec())