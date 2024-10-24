from PySide6.QtWidgets import QApplication
import sys
from main_window import MainWindow
from display import Display
from info import Info
from styles import setupTheme
from buttons import ButtonsGrid

app = QApplication(sys.argv)

setupTheme(app)

window = MainWindow()
info = Info("Sua conta")
window.addWidgetToVLayout(info)

display = Display()
display.setPlaceholderText("0")
window.addWidgetToVLayout(display)

buttonsGrid = ButtonsGrid(display, info, window)
window.vLayout.addLayout(buttonsGrid)

window.adjustFixedSize()
window.show()
app.exec()
