import sys
from PySide6 import QtWidgets

from widgets.appwidget import AppWidget

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = AppWidget()
    widget.show()

    sys.exit(app.exec())