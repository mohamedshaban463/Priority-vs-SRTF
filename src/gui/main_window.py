from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor
import sys
from scheduler import priority_schedule, srtf_schedule


class Process:
    def __init__(self, id, arrival_time, burst_time, priority=0):
        self.id = id
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        self.remaining_time = burst_time
        self.start_time = None
        self.completion_time = None

    def reset(self):
        self.remaining_time = self.burst_time
        self.start_time = None
        self.completion_time = None


class GanttWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.gantt = []

    def paintEvent(self, event):
        if not self.gantt:
            return
        painter = QPainter(self)
        scale = 50
        y = 40
        for process, start, end in self.gantt:
            x = start * scale + 20
            width = (end - start) * scale
            painter.setBrush(QColor("skyblue"))
            painter.drawRect(x, y, width, 50)
            painter.drawText(x + 10, y + 30, process)
            painter.drawText(x, y + 70, str(start))
        last_end = self.gantt[-1][2]
        painter.drawText(last_end * scale + 20, y + 70, str(last_end))


app = QtWidgets.QApplication(sys.argv)
window = uic.loadUi(r"src/gui/ui/design.ui")

custom = GanttWidget(window)
custom.setGeometry(window.widget.geometry())
window.widget.hide()


def draw():
    processes = []
    rows = window.tableWidget.rowCount()
    for row in range(rows):
        pid_item = window.tableWidget.item(row, 0)
        arrival_item = window.tableWidget.item(row, 1)
        burst_item = window.tableWidget.item(row, 2)
        priority_item = window.tableWidget.item(row, 3)
        if pid_item and arrival_item and burst_item:
            pid = pid_item.text()
            arrival = int(arrival_item.text())
            burst = int(burst_item.text())
            priority = int(priority_item.text()) if priority_item else 0
            processes.append(Process(pid, arrival, burst, priority))
    if not processes:
        return
    _, gantt_chart = priority_schedule(processes)
    custom.gantt = [(pid, start, end) for start, end, pid in gantt_chart]
    custom.update()


window.pushButton.clicked.connect(draw)
window.show()
sys.exit(app.exec_())
