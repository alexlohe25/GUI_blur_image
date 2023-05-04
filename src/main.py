from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import sys
import os
import puremagic
import time

#////////////////////////////////////////////////
class ImageLabel(QLabel):
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignCenter)
        self.setText("\n\n Arrastra una imagen para procesarla \n\n")

    def setPixmap(self, image):
        scaled = image.scaled(720, 480, Qt.KeepAspectRatio)
        super().setPixmap(scaled)

    def showResults(self, images):
        i = images[-1]
        time.sleep(1)
        image = QPixmap(i)
        scaled = image.scaled(720, 480, Qt.KeepAspectRatio)
        super().setPixmap(scaled)

class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Blur it")
        self.resize(720, 480)
        self.setAcceptDrops(True)

        mainLayout = QVBoxLayout()
        self.photoViewer = ImageLabel()
        mainLayout.addWidget(self.photoViewer)
        self.setLayout(mainLayout)

        self.kernel = 0
        self.images = []

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        for f in files:
            isBMP = checkIfIsBMP(f)
            if isBMP:
                self.photoViewer.setPixmap(QPixmap(f))
                if blurItMessage(f):
                    # Set numero de kernel
                    self.setKernel()
                    print("{} sera blureado en {} mascaras".format(f, self.kernel))

                    # Comprueba si existe el enlace simbolico
                    os.system("if [ -f /mirror/GrayScale.bmp ]; then rm /mirror/GrayScale.bmp; fi")
                    # Crea un enlace simbolico
                    os.system("ln -s {} /mirror/GrayScale.bmp".format(f))
                    # Corre el codigo
                    status = os.system("su mpiu bash -c \"mpiexec -n {} -f machinefile ./mpi\"".format(self.kernel))
                    # status = 0
                    if status == 0:
                        blurredMessage(f)
                        resultPath = "/mirror/mpiu/images/"
                        result = resultPath + "blur_" + str(self.kernel) + ".bmp"
                        self.photoViewer.setPixmap(QPixmap(result))

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