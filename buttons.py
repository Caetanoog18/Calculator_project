import math

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QGridLayout, QPushButton
from utils import isEmpty, isNumOrDot, isValidNumber
from variables import MEDIUM_FONT_SIZE
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from display import Display
    from main_window import MainWindow
    from info import Info


class Button(QPushButton):
    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)
        self.configStyle()

    def configStyle(self):
        font = self.font()
        font.setPixelSize(MEDIUM_FONT_SIZE)
        self.setFont(font)
        self.setMinimumSize(70,70)

        

class ButtonsGrid(QGridLayout):
    def __init__(self,display: 'Display',info: 'Info', window: 'MainWindow',
                 *args, **kwargs):
        super().__init__(*args,**kwargs)
        self._gridMask = [
            ['C', 'D', '^', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['N',  '0', '.', '='],
        ]
        self.display = display
        self.info = info
        self.window = window
        self._equation=''
        self._equationInitialValue = 'Your calculation'
        self._left = None
        self._right = None
        self._operator = None

        self.equation = self._equationInitialValue
        self._makeGrid()
        

    @property
    def equation(self):
        return self._equation
    
    @equation.setter
    def equation(self,value):
        self._equation = value
        self.info.setText(value)

    def vouApagarVocê(self, *args):
        print('Signal recebido por "vouApagarVocê" em', type(self).__name__, args)

    def _makeGrid(self):
        self.display.eqPressed.connect(self._eq)
        self.display.delPressed.connect(self._backspace)
        self.display.clearPressed.connect(self._clear)
        self.display.inputPressed.connect(self._insertToDisplay)
        self.display.operatorPressed.connect(self._configLeftOp)

        for rowNumber, rowData in enumerate(self._gridMask):
            for colNumber, buttonText in enumerate(rowData):
                button = Button(buttonText)

                if not isNumOrDot(buttonText) and not isEmpty(buttonText):
                     button.setProperty('cssClass', 'specialButton')
                     self._configSpecialButton(button)
                self.addWidget(button, rowNumber, colNumber)
                slot = self._makeSlot(self._insertToDisplay, buttonText)
                self._connectButtonClicked(button, slot)

    def _connectButtonClicked(self,button,slot):
        button.clicked.connect(slot) # type: ignore

    def _configSpecialButton(self,button):
        text = button.text()

        if text == 'C':
            self._connectButtonClicked(button, self._clear)

        if text in '+-/*^':
            self._connectButtonClicked(button, self._makeSlot(self._configLeftOp, text))

        if text == '=':
            self._connectButtonClicked(button, self._eq)

        if text == 'D':
            self._connectButtonClicked(button, self.display.backspace)

        if text == 'N':
            self._connectButtonClicked(button, self._invertNumber)

    @Slot()
    def _makeSlot(self,func, *args, **kwargs):
        @Slot(bool)
        def realSlot(_):
            func(*args,**kwargs)
        return realSlot

    @Slot()
    def _insertToDisplay(self, text):
        newDisplaValue = self.display.text() + text

        if not isValidNumber(newDisplaValue):
            return 
        
        self.display.insert(text)
        self.display.setFocus()


    @Slot()
    def _invertNumber(self):
        displayText = self.display.text()

        if not isValidNumber(displayText):
            return 
        number = -float(displayText)

        if number.is_integer():
            number = int(number) 

        self.display.setText(str(number))

    @Slot()
    def _clear(self):
        self._right = None
        self._left = None
        self._operator = None
        self.equation = self._equationInitialValue
        self.display.clear()
        self.display.setFocus()

    @Slot()
    def _configLeftOp(self, text):
        displayText = self.display.text()  # Must be my number_left
        self.display.clear()  # Clear display
        self.display.setFocus()

        # if you clicked in an operator before to click in a number
        if not isValidNumber(displayText) and self._left is None:
            self._showError('You didnt write anything')
            return 
        
        if self._left is None:
            self._left = float(displayText)

        self._operator = text
        self.equation = f'{self._left}{self._operator} ??'

    @Slot()
    def _eq(self):
        displayText = self.display.text()

        if not isValidNumber(displayText) or self._left is None:
            self._showError('Incomplete calculation')
            return 
        
        self._right = float(displayText)
        self.equation = f'{self._left} {self._operator} {self._right}'
        result = 'error'

        try:
            if '^' in self.equation and isinstance(self._left, float):
                result = math.pow(self._left, self._right)
            else:
                result = eval(self.equation)
        except ZeroDivisionError:
            self._showError('Zero division error')
        except OverflowError:
            self._showError('Math range error')

        self.display.clear()
        self.info.setText(f'{self.equation} = {result}')
        self._left = result
        self._right = None
        self.display.setFocus()

        if result == 'error':
            self._left = None

    @Slot()
    def _backspace(self):
        self.display.backspace()
        self.display.setFocus()

    def _makeDialog(self,text):
        msgBox = self.window.makeMsgBox()
        msgBox.setText(text)
        return msgBox

    def _showError(self, text):
        msgBox = self._makeDialog(text)
        msgBox.setText(text)
        msgBox.setIcon(msgBox.Icon.Critical)
        msgBox.exec()
        self.display.setFocus()

    def _showInfo(self, text):
        msgBox = self._makeDialog(text)
        msgBox.setText(text)
        msgBox.setIcon(msgBox.Icon.Information)
        msgBox.exec()
        self.display.setFocus()