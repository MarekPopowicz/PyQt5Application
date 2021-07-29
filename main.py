import sys
import time
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QSplashScreen
import Gui.Components.constants as Const
from Data.db_manager import DBManager
from Gui.main_window import MainWindow

# init application object


app = QApplication(sys.argv)
app.setStyle('Fusion')

# create database and fill tables with initial data
DBManager()

# Create and display the splash screen
splash_pix = QPixmap(Const.SPLASH_IMAGE)

splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
splash.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
splash.setEnabled(False)


# splash = QSplashScreen(splash_pix)
# adding progress bar

# progressBar = QProgressBar(splash)
# progressBar.setMaximum(10)
# progressBar.setGeometry(10, splash_pix.height() - 50, splash_pix.width()-20, 30)

# splash.setMask(splash_pix.mask())


splash.show()

text = "<br/><h1><strong><font color = 'green'>Twoja Terenówka</font></strong></h1>" \
       "<h3>(c) 2021 Marek Popowicz</h3>" \
       "<h2>Witaj...</h2> "

splash.showMessage(text, Qt.AlignTop | Qt.AlignHCenter | Qt.AlignAbsolute)

for i in range(1, 10):
    # progressBar.setValue(i)
    t = time.time()
    while time.time() < t + 0.2:
        app.processEvents()

time.sleep(0.001)
splash.close()
window = MainWindow()
sys.exit(app.exec_())
