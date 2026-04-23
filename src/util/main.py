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
        

        priority_data=[
                     ["p1",2,8,0],
                       ["p2",1,5,1],
                        ["p3",4,7,3]
        ]

        self.show_table(priority_data)

        print("Priority running.")


    def run_srtf(self):
        data=[
                     ["p1",1,6,0],
                       ["p2",0,3,0],
                        ["p3",2,5,1]
        ]
        self.show_table(data)
        print("SRTF running")

    def compare(self):

         p_wt = sum(row[1] for row in self.priority_data) / len(self.priority_data)
         p_tat = sum(row[2] for row in self.priority_data) / len(self.priority_data)
         p_rt = sum(row[3] for row in self.priority_data) / len(self.priority_data)

         s_wt=sum(row[1] for row in self.data)/len(self.data)

         s_tat=sum(row[2] for row in self.data)/len(self.data)
         s_rt=sum(row[3] for row in self.data)/len(self.data)



         if s_wt < p_wt:
           best = "SRTF"
         else:
          best = "Priority"


 
         result_text = f"""
        Priority:
    WT = {p_wt:.2f}, TAT = {p_tat:.2f}, RT = {p_rt:.2f}

     SRTF:
     WT = {s_wt:.2f}, TAT = {s_tat:.2f}, RT = {s_rt:.2f}

     best: {best}
     """

         self.ui.label.setText(result_text)
            
         print("Comparing")








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