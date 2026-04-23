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
        

       self.priority_data=[
                     ["p1",2,8,0],
                       ["p2",1,5,1],
                        ["p3",4,7,3]
        ]

       self.show_table(self.priority_data)

       print("Priority running.")


    def run_srtf(self):
        self.data=[
                     ["p1",1,6,0],
                       ["p2",0,3,0],
                        ["p3",2,5,1]
        ]
        self.show_table(self.data)
        print("SRTF running")


    def compare(self):
     print("Comparing")

     if not hasattr(self, "priority_data") or not hasattr(self, "data"):
        self.ui.comparison.setText("Run Priority and SRTF first!")
        return

     p_wt = sum(row[1] for row in self.priority_data) / len(self.priority_data)
     s_wt = sum(row[1] for row in self.data) / len(self.data)

     best = "SRTF" if s_wt < p_wt else "Priority"

     self.ui.comparison.setText(
        f"Priority WT = {p_wt:.2f}\n"
        f"SRTF WT = {s_wt:.2f}\n"
        f"Best = {best}"
    )



    def show_table(self, data):
         self.ui.tableWidget.setRowCount(len(data))

         for row in range(len(data)):
          for col in range(len(data[row])):
            item = QTableWidgetItem(str(data[row][col]))
            self.ui.tableWidget.setItem(row, col, item)

app = QApplication(sys.argv)
win = Window()
win.show()
sys.exit(app.exec_())