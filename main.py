import sys


from main_window import MainWindow
from display import Display
from info import Info
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from variables import WINDOW_ICON_PATH
from styles import setupTheme
from buttons import Button, ButtonsGrid

if __name__ == '__main__':
    # Create application
    app = QApplication(sys.argv)
    setupTheme()
    window = MainWindow()


    # Set icon
    icon = QIcon(str(WINDOW_ICON_PATH))
    window.setWindowIcon(icon)
    app.setWindowIcon(icon)

    # Info
    info = Info('Your calculation')
    window.addWidgetToverticalayout(info)

    # Display
    display = Display()
    window.addWidgetToverticalayout(display)

    # Grid
    buttonsGrid = ButtonsGrid(display,info, window)
    window.verticalLayout.addLayout(buttonsGrid)

    # Runs all
    window.adjustFixedSize()
    window.show()
    app.exec()

