import math
from PySide6.QtWidgets import QPushButton, QGridLayout
from PySide6.QtCore import Slot
from variables import MEDIUM_FONT_SIZE
from utils import isNumOrDot, isEmpty, isValidNumber, convertToNumber
from display import Display
from typing import TYPE_CHECKING
if TYPE_CHECKING: 
    from display import Display
    from info import Info
    from main_window import MainWindow

class Button(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configStyle()

    def configStyle(self):
        font = self.font()
        font.setPixelSize(MEDIUM_FONT_SIZE)
        self.setFont(font)
        self.setMinimumSize(75, 75)

class ButtonsGrid(QGridLayout):
    def __init__(self, display: 'Display', info: 'Info', window: 'MainWindow', 
                 *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._gridMask = [
            ['C', '⌫', '^', '÷'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['N',  '0', '.', '='],
        ]
        self.display = display
        self.info = info
        self.window = window
        self._equation = ''
        self._equationInitialValue = '0'
        self._left = None
        self._right = None
        self._op = None

        self.equation = self._equationInitialValue
        self._makeGrid()

    @property
    def equation(self):
        return self._equation
    
    @equation.setter
    def equation(self, value):
        self._equation = value
        self.info.setText(value)

    def _makeGrid(self):
        self.display.eqPressed.connect(self._eq)
        self.display.delPressed.connect(self._backspace)
        self.display.clearPressed.connect(self._clear)
        self.display.inputPressed.connect(self._insertToDisplay)
        self.display.operatorPressed.connect(self._configLeftOp)

        for rowNumber, rowData in enumerate(self._gridMask):
            for column_number, buttonText in enumerate(rowData):
                button = Button(buttonText)
                button.setProperty('cssClass', 'normalButton')

                if not isNumOrDot(buttonText) and not isEmpty(buttonText):
                    button.setProperty('cssClass', 'specialButton')
                    self._configSpacialButton(button)

                self.addWidget(button, rowNumber, column_number)
                slot = self._makeSlot(self._insertToDisplay, buttonText)
                self._connectButtonClicked(button, slot)

    def _connectButtonClicked(self, button, slot):
        button.clicked.connect(slot)

    def _configSpacialButton(self, button):
        text = button.text()
        print('Texto do botao especial:', text)

        if text == 'C':
            self._connectButtonClicked(button, self._clear)

        if text == '⌫':
            self._connectButtonClicked(button, self._backspace)

        if text == 'N':
            self._connectButtonClicked(button, self._invertNumber)


        if text in '+-÷*^':
            if text == "÷":
                text = "/"
                
            self._connectButtonClicked(
                button, 
                self._makeSlot(self._configLeftOp, text))
            
        if text == '=':
            self._connectButtonClicked(button, self._eq)
                
    @Slot()
    def _makeSlot(self, func, *args, **kwargs):
        @Slot(bool)
        def realSlot(_):
            func(*args, **kwargs)
        return realSlot
    
    @Slot()
    def _invertNumber(self):
        displayText = self.display.text()
        
        if not isValidNumber(displayText):
            return

        number = convertToNumber(displayText) * -1
        self.display.setText(str(number))
        self.display.setFocus()
    
    @Slot()
    def _insertToDisplay(self, text):
        newDisplayValue = self.display.text() + text
        
        if not isValidNumber(newDisplayValue):
            return

        self.display.insert(text)
        self.display.setFocus()

    @Slot()
    def _clear(self):
        self._right = None
        self._op = None
        self._left = None
        self.equation = self._equationInitialValue
        self.display.clear()
        self.display.setFocus()

    @Slot()
    def _configLeftOp(self, text):
        displayText = self.display.text()
        self.display.clear()
        self.display.setFocus()

        if not isValidNumber(displayText) and self._left is None:
            self._showError("Nada foi digitado!")
            return
        if self._left is None:
            self._left = convertToNumber(displayText)

        self._op = text
        self.equation = f"{self._left} {self._op} "

    @Slot()
    def _eq(self):
        displayText = self.display.text()

        if not isValidNumber(displayText) or self._left is None:
            self._showError("Conta incompleta!")
            return
        
        self._right = convertToNumber(displayText)
        self.equation = f"{self._left} {self._op} {self._right}"
        result = "error"

        try:
            if '^' in self.equation and isinstance(self._left, int | float):
                result = math.pow(self._left, self._right)
                result = convertToNumber(str(result))
            else:
                result = eval(self.equation)
        except ZeroDivisionError:
            self._showError('Não é possivel dividir por zero!')
        except OverflowError:
            self._showError('Não é possivel realizar essa conta!')
        
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

    def _makeDialog(self, text):
        msgBox = self.window.makeMsgBox()
        msgBox.setText(text)
        return msgBox

    def _showError(self, text):
        msgBox = self._makeDialog(text)
        msgBox.setIcon(msgBox.Icon.Critical)
        msgBox.exec()
        self.display.setFocus()

    def _showInfo(self, text):
        msgBox = self._makeDialog(text)
        msgBox.setIcon(msgBox.Icon.Information)
        msgBox.exec()
        self.display.setFocus()