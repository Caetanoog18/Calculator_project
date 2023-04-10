from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QMessageBox


class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget | None = None, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)

        # Configuring the basic layout
        self.cw = QWidget()
        self.verticalLayout = QVBoxLayout()
        self.cw.setLayout(self.verticalLayout)
        self.setCentralWidget(self.cw)

        # Window title
        self.setWindowTitle('Calculadora')

    def adjustFixedSize(self):
        # Last thing to be done
        self.adjustSize()
        self.setFixedSize(self.width(), self.height())

    def addWidgetToverticalayout(self,widget: QWidget):
        self.verticalLayout.addWidget(widget)
        self.adjustFixedSize

    def makeMsgBox(self):
        return QMessageBox(self)