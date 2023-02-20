from config import *
import sys
from PyQt6.QtWidgets import QApplication
from GUI import SubwayGUI

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SubwayGUI()
    window.show()
    e = app.exec()
    MATLAB_ENGINE.exit()
    sys.exit(e)
