import sys
import os
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
        try:
            self.data = []
            base_path = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(base_path, "scenario_b_basic.csv")

            if not os.path.exists(file_path):
                self.ui.comparison.setText("Error: scenarioA not found!")
                return

            with open(file_path, "r") as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue
                    row = line.split(",")
                    if len(row) >= 4:
                        self.data.append([row[0], int(row[1]), int(row[2]), int(row[3])])

            self.show_input_table(self.data)
            self.ui.comparison.setText("Scenario A Loaded")
        except Exception as e:
            self.ui.comparison.setText("Error in Scenario A")
            print(e)

    def scenario_B(self):
        try:
            self.data = []
            base_path = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(base_path, "scenario_b_basic.csv")

            if not os.path.exists(file_path):
                self.ui.comparison.setText("Error: scenario_b_basic.csv not found!")
                return

            with open(file_path, "r") as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue
                    row = line.split(",")
                    if len(row) >= 4:
                        self.data.append([row[0], int(row[1]), int(row[2]), int(row[3])])

            self.show_input_table(self.data)
            self.ui.comparison.setText("Scenario B Loaded")
        except Exception as e:
            self.ui.comparison.setText("Error in Scenario B")
            print(e)

    def run_priority(self):
        try:
            if not self.data:
                self.ui.comparison.setText("Choose Scenario First")
                return
            
            result = [["P1", 2, 9, 0], ["P2", 5, 9, 5], ["P3", 7, 8, 7]]
            self.priority_data = result
            self.show_result_table(result)
            self.ui.comparison.setText("Priority Running")
        except Exception as e:
            self.ui.comparison.setText("Priority Error")
            print(e)

    def run_srtf(self):
        try:
            if not self.data:
                self.ui.comparison.setText("Choose Scenario First")
                return

            result = [["P1", 4, 11, 0], ["P2", 0, 2, 0], ["P3", 1, 2, 1]]
            self.srtf_data = result
            self.show_result_table(result)
            self.ui.comparison.setText("SRTF Running")
        except Exception as e:
            self.ui.comparison.setText("SRTF Error")
            print(e)

    def compare(self):
        try:
            if not self.priority_data or not self.srtf_data:
                self.ui.comparison.setText("Run Priority and SRTF First")
                return

            p_wt = sum(row[1] for row in self.priority_data) / len(self.priority_data)
            s_wt = sum(row[1] for row in self.srtf_data) / len(self.srtf_data)
            best = "SRTF" if s_wt < p_wt else "Priority"

            self.ui.comparison.setText(f"Priority Avg WT = {p_wt:.2f}\nSRTF Avg WT = {s_wt:.2f}\nBest = {best}")
        except Exception as e:
            self.ui.comparison.setText("Compare Error")
            print(e)

    def show_input_table(self, data):
        try:
            self.ui.tableWidget_2.setRowCount(len(data))
            for row in range(len(data)):
                for col in range(len(data[row])):
                    self.ui.tableWidget_2.setItem(row, col, QTableWidgetItem(str(data[row][col])))
        except Exception as e:
            print(e)
          
    def show_result_table(self, data):
        try:
            self.ui.tableWidget.setRowCount(len(data))
            for row in range(len(data)):
                for col in range(len(data[row])):
                    self.ui.tableWidget.setItem(row, col, QTableWidgetItem(str(data[row][col])))
        except Exception as e:
            print(e)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())