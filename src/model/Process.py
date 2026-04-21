class Process:
    def __init__(self, process_id, arrival_time, burst_time, priority=0):
        self.id = process_id
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        self.remaining_time = burst_time
        self.start_time = None
        self.completion_time = None
        self.waiting_time = 0
        self.turnaround_time = 0
    
    def reset(self):
        self.remaining_time = self.burst_time
        self.start_time = None
        self.completion_time = None
        self.waiting_time = 0
        self.turnaround_time = 0
    
    def __repr__(self):
        return (f"Process(id={self.id}, arrival={self.arrival_time}, "
                f"burst={self.burst_time}, priority={self.priority}, "
                f"remaining={self.remaining_time})")
