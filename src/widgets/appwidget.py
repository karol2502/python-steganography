from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Slot

from widgets.phasecoding.phasecodingwidget import PhaseCodingWidget
from widgets.lsb.lsbwidget import LSBWidget
from widgets.mainmenuwidget import MainMenuWidget

from  utils.appstate import AppState

class AppWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Add App state
        self.state = AppState.MainMenu

        self.resize(300, 200)

        self.setWindowTitle('Stenanography project')
        self.setWindowIcon(QtGui.QIcon('./assets/lock.png'))

        self.layout = QtWidgets.QVBoxLayout(self)

        self.widgets = { AppState.MainMenu : MainMenuWidget(), AppState.LSB: LSBWidget(), AppState.PhaseCoding: PhaseCodingWidget()}

        for key, widget in self.widgets.items():
            widget.changed_state.connect(self.change_state)

        self.layout.addWidget(self.widgets[self.state])

    @Slot(AppState)
    def change_state(self, state):
        if state in self.widgets:
            for i in reversed(range(self.layout.count())):
                self.layout.itemAt(i).widget().setParent(None)
            self.state = state
            self.layout.addWidget(self.widgets[self.state])
