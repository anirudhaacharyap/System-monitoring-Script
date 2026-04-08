from monitor.logger import log_alert

def check_thresholds(metrics, thresholds, top_process=None):
    """
    Checks if system metrics exceed defined thresholds.
    Generates alerts if breached.
    """
    alerts_generated = []
    
    cpu_usage = metrics.get('cpu_percent', 0)
    mem_usage = metrics.get('mem_percent', 0)
    disk_usage = metrics.get('disk_percent', 0)
    
    if cpu_usage > thresholds['cpu']:
        alert_msg = f"High CPU Usage detected: {cpu_usage}% (Threshold: {thresholds['cpu']}%)"
        if top_process:
            alert_msg += f". Top process: {top_process['name']} (PID: {top_process['pid']}, CPU: {top_process['cpu_percent']}%)"
        log_alert(alert_msg)
        alerts_generated.append(alert_msg)
        
    if mem_usage > thresholds['memory']:
        alert_msg = f"High Memory Usage detected: {mem_usage}% (Threshold: {thresholds['memory']}%)"
        log_alert(alert_msg)
        alerts_generated.append(alert_msg)
        
    if disk_usage > thresholds['disk']:
        alert_msg = f"High Disk Usage detected: {disk_usage}% (Threshold: {thresholds['disk']}%)"
        log_alert(alert_msg)
        alerts_generated.append(alert_msg)
        
    return alerts_generated
