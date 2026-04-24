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
        self.ui.scenarioA_Button_2.clicked.connect(self.scenario_A)
        self.ui.scenarioB_Button.clicked.connect(self.scenario_B)

    
        self.data = []
        self.priority_data = []
        self.srtf_data = []

    def scenario_A(self):
        self.data = [
            ["P1", 0, 7, 2],
            ["P2", 2, 4, 1],
            ["P3", 4, 1, 3],
            ["P4", 5, 4, 2]
        ]

        self.show_input_table(self.data)
        self.ui.comparison.setText("Scenario A Loaded")

    def scenario_B(self):
        self.data = [
            ["P1", 0, 20, 1],
            ["P2", 1, 2, 5],
            ["P3", 2, 1, 4],
            ["P4", 8, 4, 2]   
                      ]

        self.show_input_table(self.data)
        self.ui.comparison.setText("Scenario B Loaded")


    def run_priority(self):

        if len(self.data) == 0:
            self.ui.comparison.setText("Choose Scenario First")
            return 
        data = self.data

        
        result = [
        ["P2", 5, 9, 5],
        ["P1", 2, 9, 0],
    ]
        self.priority_data=result

        self.show_result_table(result)
        print("Priority running")


    def run_srtf(self):

        if len(self.data) == 0:
            self.ui.comparison.setText("Choose Scenario First")
            return 
        
    
        result = [
             ["P2", 0, 2, 0],
             ["P3", 1, 2, 1],
    ]      
        self.srtf_data=result
        self.show_result_table(result)
        print("SRTF running")

    def compare(self):

        if len(self.priority_data) == 0 or len(self.srtf_data) == 0:
            self.ui.comparison.setText("Run Priority and SRTF First")
            return

        p_wt = sum(row[1] for row in self.priority_data) / len(self.priority_data)
        s_wt = sum(row[1] for row in self.srtf_data) / len(self.srtf_data)

        best = "SRTF" if s_wt < p_wt else "Priority"

        self.ui.comparison.setText(
            f"Priority Avg WT = {p_wt:.2f}\n"
            f"SRTF Avg WT = {s_wt:.2f}\n"
            f"Best = {best}"
        )

    def show_input_table(self, data):

        self.ui.tableWidget_2.setRowCount(len(data))

        for row in range(len(data)):
            for col in range(len(data[row])):
                item = QTableWidgetItem(str(data[row][col]))
                self.ui.tableWidget_2.setItem(row, col, item)

    def show_result_table(self, data):

        self.ui.tableWidget.setRowCount(len(data))

        for row in range(len(data)):
            for col in range(len(data[row])):
                item = QTableWidgetItem(str(data[row][col]))
                self.ui.tableWidget.setItem(row, col, item)


app = QApplication(sys.argv)
win = Window()
win.show()
sys.exit(app.exec_())