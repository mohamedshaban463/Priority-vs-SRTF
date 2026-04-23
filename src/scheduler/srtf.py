from .Process import Process

#  CORE ALGORITHM
def srtf_schedule(processes):
    
    if not processes:
        return [], []

    #  Step 0: Reset all processes for a clean run 
    for p in processes:
        p.reset()

    n = len(processes)
    completed = 0
    current_time = 0
    gantt_raw = []  
    #  Main simulation loop 
    while completed < n:
        # Gather processes that have arrived and are not yet complete
        available = [
            p for p in processes
            if p.arrival_time <= current_time and p.remaining_time > 0
        ]

        # Handle CPU idle: no process available yet
        if not available:
            next_arrival = min(
                p.arrival_time for p in processes if p.remaining_time > 0
            )
            gantt_raw.append((current_time, next_arrival, "IDLE"))
            current_time = next_arrival
            continue

        # SRTF Selection with tie-breaking 
        selected = min(
            available,
            key=lambda p: (p.remaining_time, p.arrival_time, p.id)
        )

        # Record first CPU access (needed for Response Time)
        if selected.start_time is None:
            selected.start_time = current_time

        # -- Determine run duration until next potential preemption --
        # Process runs until:
        #   a) A new process arrives (possible preemption), or
        #   b) It completes its burst
        future_arrivals = [
            p.arrival_time for p in processes
            if p.arrival_time > current_time and p.remaining_time > 0
        ]

        if future_arrivals:
            next_event = min(future_arrivals)
            run_duration = min(selected.remaining_time,
                               next_event - current_time)
        else:
            run_duration = selected.remaining_time

        # Execute
        start = current_time
        selected.remaining_time -= run_duration
        current_time += run_duration
        gantt_raw.append((start, current_time, selected.id))

        # Check completion
        if selected.remaining_time == 0:
            selected.completion_time = current_time
            completed += 1

    # Merge consecutive Gantt segments for same process 
    gantt_chart = _merge_gantt(gantt_raw)

    #Calculate per-process metrics
    for p in processes:
        p.turnaround_time = p.completion_time - p.arrival_time
        p.waiting_time = p.turnaround_time - p.burst_time

    return processes, gantt_chart


# -- HELPER FUNCTIONS --

def _merge_gantt(segments):
    """
    Merge consecutive Gantt segments belonging to the same process.
    Preemption points remain visible as boundaries between different PIDs.

    Example:
        [(0,1,"P1"), (1,3,"P1"), (3,5,"P2")] -> [(0,3,"P1"), (3,5,"P2")]
    """
    if not segments:
        return []

    merged = [list(segments[0])]
    for start, end, pid in segments[1:]:
        if merged[-1][2] == pid and merged[-1][1] == start:
            merged[-1][1] = end   # extend the segment
        else:
            merged.append([start, end, pid])

    return [tuple(seg) for seg in merged]


def get_response_times(processes):
    """
    Calculate Response Time for each process.
    RT = start_time - arrival_time

    Returns:
        dict: {process_id: response_time}
    """
    return {p.id: p.start_time - p.arrival_time for p in processes}


def get_average_metrics(processes):
    """
    Compute average WT, TAT, and RT 

    Returns:
        dict with keys 'avg_wt', 'avg_tat', 'avg_rt'
    """
    n = len(processes)
    if n == 0:
        return {'avg_wt': 0, 'avg_tat': 0, 'avg_rt': 0}

    avg_wt  = sum(p.waiting_time for p in processes) / n
    avg_tat = sum(p.turnaround_time for p in processes) / n
    avg_rt  = sum((p.start_time - p.arrival_time) for p in processes) / n

    return {'avg_wt': avg_wt, 'avg_tat': avg_tat, 'avg_rt': avg_rt}


