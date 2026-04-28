from calculator import calculate_all_metrics

def srtf_schedule(processes):
    if not processes:
        return [], []

    for p in processes:
        p.reset()

    n = len(processes)
    completed = 0
    current_time = 0
    gantt_raw = []  

    while completed < n:
        available = [
            p for p in processes
            if p.arrival_time <= current_time and p.remaining_time > 0
        ]

        if not available:
            next_arrival = min(p.arrival_time for p in processes if p.remaining_time > 0)
            gantt_raw.append((current_time, next_arrival, "IDLE"))
            current_time = next_arrival
            continue

        selected = min(
            available,
            key=lambda p: (p.remaining_time, p.arrival_time, p.id)
        )

        if selected.start_time is None:
            selected.start_time = current_time

        future_arrivals = [
            p.arrival_time for p in processes
            if p.arrival_time > current_time and p.remaining_time > 0
        ]

        if future_arrivals:
            next_event = min(future_arrivals)
            run_duration = min(selected.remaining_time, next_event - current_time)
        else:
            run_duration = selected.remaining_time

        start = current_time
        selected.remaining_time -= run_duration
        current_time += run_duration
        gantt_raw.append((start, current_time, selected.id))

        if selected.remaining_time == 0:
            selected.completion_time = current_time
            completed += 1

    gantt_chart = _merge_gantt(gantt_raw)
    
    calculate_all_metrics(processes)

    return processes, gantt_chart


def _merge_gantt(segments):
    if not segments:
        return []
    merged = [list(segments[0])]
    for start, end, pid in segments[1:]:
        if merged[-1][2] == pid and merged[-1][1] == start:
            merged[-1][1] = end   
        else:
            merged.append([start, end, pid])
    return [tuple(seg) for seg in merged]

from calculator import calculate_all_metrics

def srtf_schedule(processes):
    if not processes:
        return [], []

    for p in processes:
        p.reset()

    n = len(processes)
    completed = 0
    current_time = 0
    gantt_raw = []  

    while completed < n:
        available = [
            p for p in processes
            if p.arrival_time <= current_time and p.remaining_time > 0
        ]

        if not available:
            next_arrival = min(p.arrival_time for p in processes if p.remaining_time > 0)
            gantt_raw.append((current_time, next_arrival, "IDLE"))
            current_time = next_arrival
            continue

        selected = min(
            available,
            key=lambda p: (p.remaining_time, p.arrival_time, p.id)
        )

        if selected.start_time is None:
            selected.start_time = current_time

        future_arrivals = [
            p.arrival_time for p in processes
            if p.arrival_time > current_time and p.remaining_time > 0
        ]

        if future_arrivals:
            next_event = min(future_arrivals)
            run_duration = min(selected.remaining_time, next_event - current_time)
        else:
            run_duration = selected.remaining_time

        start = current_time
        selected.remaining_time -= run_duration
        current_time += run_duration
        
        gantt_raw.append((start, current_time, selected.id))

        if selected.remaining_time == 0:
            selected.completion_time = current_time
            completed += 1

    gantt_chart = _merge_gantt(gantt_raw)
    
    calculate_all_metrics(processes)

    return processes, gantt_chart


def _merge_gantt(segments):
    if not segments:
        return []
    merged = [list(segments[0])]
    for start, end, pid in segments[1:]:
        if merged[-1][2] == pid and merged[-1][1] == start:
            merged[-1][1] = end   
        else:
            merged.append([start, end, pid])
    return [tuple(seg) for seg in merged]