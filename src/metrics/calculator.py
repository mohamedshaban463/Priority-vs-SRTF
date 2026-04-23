def calculate_all_metrics(processes):
    """
    Calculates TAT, WT, and RT for all processes and returns the averages.
    """
    n = len(processes)
    if n == 0:
        return {'avg_wt': 0, 'avg_tat': 0, 'avg_rt': 0}

    for p in processes:
        # Fallback just in case a process never got CPU time
        if p.completion_time is None:
            p.completion_time = p.arrival_time
        if p.start_time is None:
            p.start_time = p.arrival_time

        # TAT = Completion Time - Arrival Time
        p.turnaround_time = p.completion_time - p.arrival_time
        
        # WT = Turnaround Time - Burst Time
        p.waiting_time = p.turnaround_time - p.burst_time
        
        # RT = First Start Time - Arrival Time 
        # (We dynamically add response_time here since it was missing from the Process class)
        p.response_time = p.start_time - p.arrival_time

    # Calculate overall averages
    avg_wt  = sum(p.waiting_time for p in processes) / n
    avg_tat = sum(p.turnaround_time for p in processes) / n
    avg_rt  = sum(p.response_time for p in processes) / n

    return {'avg_wt': avg_wt, 'avg_tat': avg_tat, 'avg_rt': avg_rt}
