__package__ = 'metrics'


def calculate_all_metrics(processes):

    n = len(processes)
    if n == 0:
        return {'avg_wt': 0, 'avg_tat': 0, 'avg_rt': 0}

    for p in processes:
        if p.completion_time is None:
            p.completion_time = p.arrival_time
        if p.start_time is None:
            p.start_time = p.arrival_time

        p.turnaround_time = p.completion_time - p.arrival_time
        
        p.waiting_time = p.turnaround_time - p.burst_time
        
        p.response_time = p.start_time - p.arrival_time

    avg_wt  = sum(p.waiting_time for p in processes) / n
    avg_tat = sum(p.turnaround_time for p in processes) / n
    avg_rt  = sum(p.response_time for p in processes) / n

    return {'avg_wt': avg_wt, 'avg_tat': avg_tat, 'avg_rt': avg_rt}