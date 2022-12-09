import sys
from PySide6 import QtCore, QtWidgets, QtGui

class Field(QtWidgets.QWidget): # Extend QtWidget to Field
    def __init__(self):
        super().__init__() # inherit QtWidget constructor
        



if __name__ == "__main__": # Only run on direct execution
    app = QtWidgets.QApplication([])

    widget = Field()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())
