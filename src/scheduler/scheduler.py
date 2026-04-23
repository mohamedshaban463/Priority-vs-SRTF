import copy

class Process:
    def __init__(self, pid, arrival_time, burst_time, priority):
        # Initial user input
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        
        # Simulation tracking variables
        self.remaining_time = burst_time  
        self.start_time = -1              
        self.completion_time = 0
        
        # Final calculated metrics
        self.turnaround_time = 0
        self.waiting_time = 0
        self.response_time = 0

def get_user_input():
    processes = []
    seen_pids = set()
    
    print("\n" + "*"*55)
    print("   CPU SCHEDULING SIMULATOR: PRIORITY vs SRTF")
    print("   (Type 'done' for the Process ID when finished)")
    print("*"*55)

    while True:
        pid = input("\nEnter Process ID (e.g., P1): ").strip()
        
        if pid.lower() == 'done':
            if len(processes) == 0:
                print("❌ Error: You must enter at least one process.")
                continue
            break
            
        if not pid:
            print("❌ Error: Process ID cannot be empty.")
            continue
            
        if pid in seen_pids:
            print(f"❌ Error: Process ID '{pid}' already exists.")
            continue

        try:
            arrival = int(input(f"Enter Arrival Time for {pid}: "))
            if arrival < 0:
                print("❌ Error: Arrival time cannot be negative.")
                continue

            burst = int(input(f"Enter Burst Time for {pid}: "))
            if burst <= 0:
                print("❌ Error: Burst time must be greater than zero.")
                continue

            priority = int(input(f"Enter Priority for {pid} (smaller integer = higher priority): "))
            
            processes.append(Process(pid, arrival, burst, priority))
            seen_pids.add(pid)
            print(f"✅ {pid} added successfully!")

        except ValueError:
            print("❌ Error: Arrival Time, Burst Time, and Priority must be integers.")

    return processes

def run_priority_scheduling(processes):
    current_time = 0
    completed = 0
    n = len(processes)
    gantt_chart = [] 

    while completed < n:
        ready_queue = []
        for p in processes:
            if p.arrival_time <= current_time and p.remaining_time > 0:
                ready_queue.append(p)
        
        if len(ready_queue) == 0:
            gantt_chart.append("Idle")
            current_time += 1
            continue
            
        # Sort by lowest priority integer, then by arrival time (FCFS tie-breaker)
        ready_queue.sort(key=lambda x: (x.priority, x.arrival_time))
        current_process = ready_queue[0]
        
        if current_process.start_time == -1:
            current_process.start_time = current_time
            
        current_process.remaining_time -= 1
        gantt_chart.append(current_process.pid)
        current_time += 1
        
        if current_process.remaining_time == 0:
            current_process.completion_time = current_time
            completed += 1
            
    return gantt_chart

def run_srtf_scheduling(processes):
    current_time = 0
    completed = 0
    n = len(processes)
    gantt_chart = [] 

    while completed < n:
        ready_queue = []
        for p in processes:
            if p.arrival_time <= current_time and p.remaining_time > 0:
                ready_queue.append(p)
        
        if len(ready_queue) == 0:
            gantt_chart.append("Idle")
            current_time += 1
            continue
            
        # Sort by shortest remaining time, then by arrival time (FCFS tie-breaker)
        ready_queue.sort(key=lambda x: (x.remaining_time, x.arrival_time))
        current_process = ready_queue[0]
        
        if current_process.start_time == -1:
            current_process.start_time = current_time
            
        current_process.remaining_time -= 1
        gantt_chart.append(current_process.pid)
        current_time += 1
        
        if current_process.remaining_time == 0:
            current_process.completion_time = current_time
            completed += 1
            
    return gantt_chart

def print_gantt_chart(timeline):
    print("\n--- Gantt Chart ---")
    if not timeline:
        return

    current_process = timeline[0]
    start_time = 0

    for time in range(1, len(timeline)):
        if timeline[time] != current_process:
            print(f"[{start_time:02d} - {time:02d}] : {current_process}")
            current_process = timeline[time]
            start_time = time
            
    print(f"[{start_time:02d} - {len(timeline):02d}] : {current_process}")
    print("-" * 19)

def calculate_metrics(processes):
    total_wt = 0
    total_tat = 0
    total_rt = 0
    n = len(processes)

    print("\n--- Final Results Table ---")
    print(f"{'PID':<5} | {'Arrival':<8} | {'Burst':<6} | {'Priority':<8} | {'Completion':<10} | {'TAT':<5} | {'WT':<5} | {'RT':<5}")
    print("-" * 75)

    for p in processes:
        p.turnaround_time = p.completion_time - p.arrival_time
        p.waiting_time = p.turnaround_time - p.burst_time
        p.response_time = p.start_time - p.arrival_time

        total_tat += p.turnaround_time
        total_wt += p.waiting_time
        total_rt += p.response_time

        print(f"{p.pid:<5} | {p.arrival_time:<8} | {p.burst_time:<6} | {p.priority:<8} | {p.completion_time:<10} | {p.turnaround_time:<5} | {p.waiting_time:<5} | {p.response_time:<5}")

    print("-" * 75)
    print(f"Average Turnaround Time (TAT): {total_tat / n:.2f}")
    print(f"Average Waiting Time (WT):     {total_wt / n:.2f}")
    print(f"Average Response Time (RT):    {total_rt / n:.2f}\n")
    
    # Return averages just in case another file (like the GUI) needs them!
    return (total_tat / n, total_wt / n, total_rt / n)



# MAIN EXECUTION SCRIPT (For Terminal Use)

if __name__ == "__main__":
    # 1. Get the workload from the user
    user_processes = get_user_input()

    # 2. Create deep copies so the algorithms don't overwrite each other's remaining times
    priority_list = copy.deepcopy(user_processes)
    srtf_list = copy.deepcopy(user_processes)

    # 3. Execute and Output Preemptive Priority
    print("\n" + "="*60)
    print(" ALGORITHM 1: PREEMPTIVE PRIORITY SCHEDULING")
    print("="*60)
    priority_timeline = run_priority_scheduling(priority_list)
    print_gantt_chart(priority_timeline)
    calculate_metrics(priority_list)

    # 4. Execute and Output SRTF
    print("\n" + "="*60)
    print(" ALGORITHM 2: SHORTEST REMAINING TIME FIRST (SRTF)")
    print("="*60)
    srtf_timeline = run_srtf_scheduling(srtf_list)
    print_gantt_chart(srtf_timeline)
    calculate_metrics(srtf_list)