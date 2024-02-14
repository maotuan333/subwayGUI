import sys
from PyQt6.QtWidgets import QApplication
from GUI import SubwayGUI
from config import logger

if __name__ == "__main__":
        app = QApplication(sys.argv)
        print("hi")
        window = SubwayGUI()
        window.show()
        e=app.exec()
        logger.info("subway gui finished")
        sys.exit(e)
