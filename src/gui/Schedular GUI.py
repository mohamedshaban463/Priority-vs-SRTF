import tkinter as tk
from tkinter import ttk, messagebox
import copy

# Import everything we built in your backend engine!
from scheduler import Process, run_priority_scheduling, run_srtf_scheduling, calculate_metrics

class SchedulerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CPU Scheduling Simulator")
        self.root.geometry("800x600")
        
        self.processes = [] 

        # --- 1. INPUT PANEL (Top Section) ---
        input_frame = tk.LabelFrame(root, text="Add New Process", padx=10, pady=10)
        input_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(input_frame, text="Process ID:").grid(row=0, column=0)
        self.pid_entry = tk.Entry(input_frame, width=10)
        self.pid_entry.grid(row=0, column=1, padx=5)

        tk.Label(input_frame, text="Arrival Time:").grid(row=0, column=2)
        self.arr_entry = tk.Entry(input_frame, width=10)
        self.arr_entry.grid(row=0, column=3, padx=5)

        tk.Label(input_frame, text="Burst Time:").grid(row=0, column=4)
        self.burst_entry = tk.Entry(input_frame, width=10)
        self.burst_entry.grid(row=0, column=5, padx=5)

        tk.Label(input_frame, text="Priority:").grid(row=0, column=6)
        self.prio_entry = tk.Entry(input_frame, width=10)
        self.prio_entry.grid(row=0, column=7, padx=5)

        add_btn = tk.Button(input_frame, text="Add Process", command=self.add_process, bg="lightblue")
        add_btn.grid(row=0, column=8, padx=10)

        # --- 2. WORKLOAD TABLE (Middle Section) ---
        table_frame = tk.LabelFrame(root, text="Current Workload", padx=10, pady=10)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("PID", "Arrival", "Burst", "Priority")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=8)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")
        self.tree.pack(fill="both", expand=True)

        # --- 3. ACTION BUTTONS (Bottom Section) ---
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        run_btn = tk.Button(btn_frame, text="Run Simulations", command=self.run_simulations, font=("Arial", 12, "bold"), bg="lightgreen", width=20)
        run_btn.pack(side="left", padx=10)
        
        clear_btn = tk.Button(btn_frame, text="Clear Data", command=self.clear_data, font=("Arial", 12), bg="lightcoral", width=15)
        clear_btn.pack(side="left", padx=10)

    # --- LOGIC FUNCTIONS ---
    def add_process(self):
        pid = self.pid_entry.get().strip()
        try:
            arr = int(self.arr_entry.get())
            burst = int(self.burst_entry.get())
            prio = int(self.prio_entry.get())

            if not pid: raise ValueError("PID cannot be empty.")
            if arr < 0 or burst <= 0 or prio <= 0: raise ValueError("Invalid numbers.")
            for p in self.processes:
                if p.pid == pid: raise ValueError("PID already exists!")

            self.processes.append(Process(pid, arr, burst, prio))
            self.tree.insert("", "end", values=(pid, arr, burst, prio))

            self.pid_entry.delete(0, tk.END)
            self.arr_entry.delete(0, tk.END)
            self.burst_entry.delete(0, tk.END)
            self.prio_entry.delete(0, tk.END)

        except ValueError:
            messagebox.showerror("Input Error", "Please ensure all fields are filled with valid positive integers.\nUnique PIDs only.")

    def clear_data(self):
        self.processes.clear()
        for row in self.tree.get_children():
            self.tree.delete(row)

    def run_simulations(self):
        if not self.processes:
            messagebox.showwarning("Warning", "Please add at least one process first!")
            return

        # 1. Create fresh copies of the data for both algorithms
        prio_list = copy.deepcopy(self.processes)
        srtf_list = copy.deepcopy(self.processes)

        # 2. Run the timelines
        prio_gantt = run_priority_scheduling(prio_list)
        srtf_gantt = run_srtf_scheduling(srtf_list)

        # 3. Calculate the math (this modifies the process objects in the lists with their final TAT, WT, RT)
        calculate_metrics(prio_list)
        calculate_metrics(srtf_list)

        # 4. Show the Results Window
        self.show_results_window(prio_list, prio_gantt, srtf_list, srtf_gantt)

    # --- RESULTS DISPLAY WINDOW ---
    def show_results_window(self, prio_processes, prio_gantt, srtf_processes, srtf_gantt):
        # Create a new popup window
        res_win = tk.Toplevel(self.root)
        res_win.title("Simulation Results & Comparisons")
        res_win.geometry("900x600")

        # Create Tabs
        notebook = ttk.Notebook(res_win)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Tab 1: Priority
        prio_tab = tk.Frame(notebook)
        notebook.add(prio_tab, text="Preemptive Priority")
        self.build_result_tab(prio_tab, prio_processes, prio_gantt)

        # Tab 2: SRTF
        srtf_tab = tk.Frame(notebook)
        notebook.add(srtf_tab, text="SRTF")
        self.build_result_tab(srtf_tab, srtf_processes, srtf_gantt)

    def build_result_tab(self, parent_frame, processes, timeline):
        # --- Format the Gantt Chart ---
        tk.Label(parent_frame, text="Gantt Chart Timeline", font=("Arial", 12, "bold")).pack(pady=10)
        
        gantt_str = ""
        if timeline:
            current = timeline[0]
            start = 0
            for t in range(1, len(timeline)):
                if timeline[t] != current:
                    gantt_str += f"[{start:02d} - {t:02d}] : {current}\n"
                    current = timeline[t]
                    start = t
            gantt_str += f"[{start:02d} - {len(timeline):02d}] : {current}\n"

        # Read-only text box for the Gantt chart
        gantt_box = tk.Text(parent_frame, height=6, width=40, font=("Courier", 11), bg="#f4f4f4")
        gantt_box.insert(tk.END, gantt_str)
        gantt_box.config(state="disabled") 
        gantt_box.pack()

        # --- Format the Metrics Table ---
        tk.Label(parent_frame, text="Per-Process Metrics", font=("Arial", 12, "bold")).pack(pady=10)
        
        cols = ("PID", "Arrival", "Burst", "Priority", "Completion", "TAT", "WT", "RT")
        tree = ttk.Treeview(parent_frame, columns=cols, show="headings", height=8)
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, width=90, anchor="center")
        tree.pack(fill="x", padx=20)

        # Populate table and calculate averages
        tot_tat = tot_wt = tot_rt = 0
        n = len(processes)
        for p in processes:
            tree.insert("", "end", values=(p.pid, p.arrival_time, p.burst_time, p.priority, 
                                           p.completion_time, p.turnaround_time, p.waiting_time, p.response_time))
            tot_tat += p.turnaround_time
            tot_wt += p.waiting_time
            tot_rt += p.response_time

        # --- Display Averages ---
        avg_text = f"Average Turnaround Time: {tot_tat/n:.2f}   |   Average Waiting Time: {tot_wt/n:.2f}   |   Average Response Time: {tot_rt/n:.2f}"
        tk.Label(parent_frame, text=avg_text, font=("Arial", 11, "bold"), fg="blue").pack(pady=20)


if __name__ == "__main__":
    root = tk.Tk()
    app = SchedulerGUI(root)
    root.mainloop()