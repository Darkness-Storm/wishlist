import sys

from PyQt5 import QtWidgets

app = QtWidgets.QApplication(sys.argv)


from main_window import MainWindow

window = MainWindow()
window.show()
sys.exit(app.exec_())
