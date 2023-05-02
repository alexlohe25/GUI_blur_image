from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import sys
import os

#////////////////////////////////////////////////

class MainWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Blur it")
        self.resize(720, 480)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

# esta funcion hay que modificarla para que mande a llmar el mpich
    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        for f in files:
            blurItMessage(f, " va a ser blureado")
            os.system("echo {} && sleep 5".format(f))
            blurItMessage(f, " ha sido blureado")

def blurItMessage(file, message):
    alert = QMessageBox()
    alert.setText(file + message)
    alert.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = MainWidget()
    ui.show()
    sys.exit(app.exec_())