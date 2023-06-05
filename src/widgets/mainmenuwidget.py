import sys
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Signal, QCoreApplication

from utils.appstate import AppState

class MainMenuWidget(QtWidgets.QWidget):
    changed_state = Signal(AppState)

    def __init__(self):
        super().__init__()

        # Create layout
        self.layout = QtWidgets.QVBoxLayout(self)

        # Create buttons
        self.lsb = QtWidgets.QPushButton("LSB")
        self.lsb.setFixedWidth(100)
        self.lsb.clicked.connect(lambda: self.change_state(AppState.LSB))

        self.phase_coding = QtWidgets.QPushButton("Phase coding")
        self.phase_coding.setFixedWidth(100)
        self.phase_coding.clicked.connect(lambda: self.change_state(AppState.PhaseCoding))

        self.exit = QtWidgets.QPushButton("Exit")
        self.exit.setFixedWidth(100)
        self.exit.clicked.connect(sys.exit)

        # Add buttons to layout
        self.layout.addWidget(self.lsb)
        self.layout.addWidget(self.phase_coding)
        self.layout.addWidget(self.exit)

    def change_state(self, state):
        self.changed_state.emit(state)