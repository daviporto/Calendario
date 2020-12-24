import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from calendario import Ui_MainWindow


class MainWindow(qtw.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None, ):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.load()
        self.show()
        qtc.QDate(int('10'), int('10'), int(' 10'))


app = qtw.QApplication(sys.argv)
mw = MainWindow()
sys.exit(app.exec())
