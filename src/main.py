from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import sys
import os
import puremagic

#////////////////////////////////////////////////
class ImageLabel(QLabel):
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignCenter)
        self.setText("\n\n Drag an image to process it \n\n")

    def setPixmap(self, image):
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
        self.hosts = []
        self.spaws = []
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
                    self.setImageToBlur(f)
                    # Set numero de kernel
                    self.setKernel()
                    self.testHosts()
                    if len(self.hosts) > 0:
                        for i in self.hosts:
                            self.setSpawFoHost(i)
                    else:
                        message("No connected hosts found")
                    hosts = ""
                    for i, host in enumerate(self.hosts):
                        hosts += host + ":" + str(self.spaws[i])
                        if i < len(self.hosts)-1:
                            hosts += ","
                    print("{} will be blurred in {} masks".format(f, self.kernel))
                    self.blurImage(f, hosts)

    def setKernel(self):
        i, okPressed = QInputDialog.getInt(self, "Set kernel mask","Amount:", 1, 1, 50, 1)
        if okPressed:
            self.kernel = i
    
    def testHosts(self):
        machinefile_path = "/mirror/mpiu/machinefile"
        machinefile = open(machinefile_path, "r")
        for host in machinefile:
            if host != "\n":
                host = host.split(":")[0]
                if os.system("ping -c 4 " + host) == 0:
                    self.hosts.append(host)
        machinefile.close()
    
    def setSpawFoHost(self, host):
        i, okPressed = QInputDialog.getInt(self, "Set spaw for {}".format(host),"Amount:", 0, 0, 50, 1)
        if okPressed:
            self.spaws.append(i)

    def setImageToBlur(self, file):
        # Comprueba si existe el enlace simbolico
        os.system("if [ -f /mirror/GrayScale.bmp ]; then rm /mirror/GrayScale.bmp; fi")
        # Crea un enlace simbolico
        os.system("ln -s {} /mirror/GrayScale.bmp".format(file))

    def blurImage(self, file, hosts):
        # Corre el codigo
        status = os.system("su mpiu bash -c \"mpiexec -n {} -host {} ./mpi\"".format(self.kernel, hosts))
        if status == 0:
            message(file + " has been blurred")
            resultPath = "/mirror/mpiu/images/"
            result = resultPath + "blur_" + str(self.kernel) + ".bmp"
            self.photoViewer.setPixmap(QPixmap(result))

def blurItMessage(file):
    alert = QMessageBox()
    alert.setWindowTitle("Blur it")
    alert.setText(file + " will be blurred")
    alert.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

    return_value = alert.exec()
    if return_value == QMessageBox.Ok:
        return True
    
    else:
        return False

def message(message):
    alert = QMessageBox()
    alert.setWindowTitle("Blur it")
    alert.setText(message)
    alert.exec_()

def checkIfIsBMP(file):
    format = puremagic.from_file(file)
    if format == ".bmp":
        return True
    else:
        alert = QMessageBox()
        alert.setText(file + " is not an image in BMP format")
        alert.exec_()
        return False

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = MainWidget()
    ui.show()
    sys.exit(app.exec_())