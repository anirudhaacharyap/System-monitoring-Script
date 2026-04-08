import psutil
import time

def get_system_metrics():
    """
    Collects CPU, memory, and disk usage metrics.
    Returns a dictionary containing the metrics.
    """
    # Get CPU usage percentage over a 1 second interval
    cpu_percent = psutil.cpu_percent(interval=1)
    
    # Get memory usage percentage
    memory = psutil.virtual_memory()
    mem_percent = memory.percent
    
    # Get disk usage percentage of the root directory
    disk = psutil.disk_usage('/')
    disk_percent = disk.percent
    
    return {
        'cpu_percent': cpu_percent,
        'mem_percent': mem_percent,
        'disk_percent': disk_percent
    }

def get_top_process_by_cpu():
    """
    Finds and returns the process consuming the most CPU.
    Takes ~0.1s to evaluate.
    """
    top_proc = None
    max_cpu = -1.0
    
    processes = []
    # Initialize cpu_percent for all processes
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            # First call initializes the measurement for this process
            proc.cpu_percent(interval=None)
            processes.append(proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
            
    # Short sleep to measure CPU usage duration
    time.sleep(0.1)
    
    for proc in processes:
        try:
            # Second call gives the cpu usage since the previous call
            cpu_usage = proc.cpu_percent(interval=None)
            if cpu_usage > max_cpu:
                max_cpu = cpu_usage
                top_proc = {
                    'pid': proc.info['pid'], 
                    'name': proc.info['name'], 
                    'cpu_percent': round(cpu_usage, 2)
                }
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
            
    return top_proc
