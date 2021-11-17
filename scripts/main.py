import sys
from PyQt5.QtWidgets import QApplication
from window import main


app = QApplication(sys.argv)
QApplication.setApplicationName('FAX')
main()
app.exec_()
