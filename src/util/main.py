import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from test import Ui_MainWindow


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.priorityButton.clicked.connect(self.run_priority)
        self.ui.SRTFButton.clicked.connect(self.run_srtf)
        self.ui.compareButton.clicked.connect(self.compare)

    def run_priority(self):
        print("Priority running.")

        self.ui.tableWidget.setRowCount(1)

        self.ui.tableWidget.setItem(0,0,QTableWidgetItem("P1"))
        self.ui.tableWidget.setItem(0,1,QTableWidgetItem("2"))
        self.ui.tableWidget.setItem(0,2,QTableWidgetItem("8"))
        self.ui.tableWidget.setItem(0,3,QTableWidgetItem("0"))

    def run_srtf(self):
        print("SRTF running")

    def compare(self):
        print("Comparing")


app = QApplication(sys.argv)
win = Window()
win.show()
sys.exit(app.exec_())