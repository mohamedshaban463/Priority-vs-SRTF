# Priority-vs-SRTF

## Project Description

Priority-vs-SRTF is an interactive educational tool that demonstrates and compares two fundamental CPU scheduling algorithms used in operating systems:

- **Priority Scheduling**: A preemptive scheduling algorithm where processes are executed based on their assigned priority levels
- **SRTF (Shortest Remaining Time First)**: A preemptive scheduling algorithm that executes the process with the shortest remaining burst time

This project provides a graphical user interface (GUI) that allows users to input process data, visualize scheduling timelines, and compare performance metrics such as waiting time, turnaround time, and CPU utilization between the two algorithms.

## Requirements

- Python 3.7 or higher
- PyQt5 (for GUI framework)

### Optional
- CSV support for batch testing with predefined test cases

## Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/mohamedshaban463/Priority-vs-SRTF.git
   cd Priority-vs-SRTF
   ```

## Build & Run Steps

### Running the Application

1. **Start the GUI application**
   ```bash
   python main.py
   ```

2. **Using the application**
   - Enter process information (Process ID, Arrival Time, Burst Time, Priority)
   - Select a scheduling algorithm (Priority or SRTF)
   - View the scheduling timeline and performance metrics
   - Compare results between algorithms

### Running Test Cases

Test case files are available in the `test-cases/` directory:
- `scenario_a_basic.csv` - Basic test scenario
- `scenario_b_basic.csv` - Intermediate test scenario
- `scenario_c_basic.csv` - Advanced test scenario

Load any test case file through the GUI to run simulations.

## Project Structure

```
Priority-vs-SRTF/
├── main.py                          # Application entry point
├── src/
│   ├── gui/                         # GUI components
│   │   ├── __init__.py
│   │   └── ui/
│   │       └── design.ui            # UI design file
│   ├── model/
│   │   ├── __init__.py
│   │   └── Process.py               # Process data model
│   ├── scheduler/
│   │   ├── __init__.py
│   │   ├── Priority.py              # Priority scheduling algorithm
│   │   └── SRTF.py                  # SRTF scheduling algorithm
│   ├── metrics/
│   │   ├── __init__.py
│   │   └── calculator.py            # Performance metrics calculation
│   └── util/
│       ├── __init__.py
│       └── test.ui                  # Utility files
├── test-cases/                      # Sample test scenarios
├── screenshots/                     # Application screenshots
└── README.md
```

## Features

- ✅ Interactive GUI for process scheduling
- ✅ Dual algorithm comparison (Priority vs SRTF)
- ✅ Real-time scheduling visualization
- ✅ Performance metrics calculation (waiting time, turnaround time, etc.)
- ✅ CSV-based test case support
- ✅ Educational timeline display

## Team Members

- Menna
- Mohamed
- Manar
- Maryem Hemdan
- Maryem Emad
- Yosry