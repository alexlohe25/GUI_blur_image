from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import sys
import os
import puremagic

#////////////////////////////////////////////////

class MainWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Blur it")
        self.resize(720, 480)
        self.setAcceptDrops(True)
        self.kernel = 0

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

# esta funcion hay que modificarla para que mande a llmar el mpich
    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        for f in files:
            isBMP = checkIfIsBMP(f)
            if isBMP:
                print(isBMP)
                if blurItMessage(f):
                    print(isBMP)
                    self.setKernel()
                    print("{} sera blureado en {} mascaras".format(f, self.kernel))
                    os.system("mpiexec -n {} -host 127.0.0.1 ./mpi_hello".format(f))
                    blurredMessage(f)

    def setKernel(self):
        i, okPressed = QInputDialog.getInt(self, "Set kernel mask","Amount:", 1, 1, 50, 1)
        if okPressed:
            self.kernel = i

def blurItMessage(file):
    alert = QMessageBox()
    alert.setText(file + " va a ser blureado")
    alert.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

    return_value = alert.exec()
    if return_value == QMessageBox.Ok:
        return True
    
    else:
        return False

def blurredMessage(file):
    alert = QMessageBox()
    alert.setText(file + " ha sido blureado")
    alert.exec_()

def checkIfIsBMP(file):
    format = puremagic.from_file(file)
    if format == ".bmp":
        return True
    else:
        alert = QMessageBox()
        alert.setText(file + " no es una imagen en formato BMP")
        alert.exec_()
        return False

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = MainWidget()
    ui.show()
    sys.exit(app.exec_())