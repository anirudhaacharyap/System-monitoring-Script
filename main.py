import argparse
import time
from datetime import datetime

import config
from monitor import metrics
from monitor import alerts
from monitor.logger import log_system_metrics

def main():
    parser = argparse.ArgumentParser(description="System Monitoring Tool (SRE)")
    parser.add_argument("--interval", type=int, default=config.DEFAULT_INTERVAL_SECONDS, 
                        help="Monitoring interval in seconds")
    parser.add_argument("--cpu-threshold", type=float, default=config.DEFAULT_CPU_WARNING_THRESHOLD,
                        help="CPU usage warning threshold (%)")
    parser.add_argument("--mem-threshold", type=float, default=config.DEFAULT_MEM_WARNING_THRESHOLD,
                        help="Memory usage warning threshold (%)")
    parser.add_argument("--disk-threshold", type=float, default=config.DEFAULT_DISK_WARNING_THRESHOLD,
                        help="Disk usage warning threshold (%)")
    
    args = parser.parse_args()
    
    thresholds = {
        'cpu': args.cpu_threshold,
        'memory': args.mem_threshold,
        'disk': args.disk_threshold
    }
    
    print("=" * 60)
    print("Starting System Monitoring Tool")
    print(f"Interval: {args.interval} seconds")
    print(f"Thresholds -> CPU: {thresholds['cpu']}%, Memory: {thresholds['memory']}%, Disk: {thresholds['disk']}%")
    print("=" * 60)
    print("Press Ctrl+C to stop.\n")
    
    try:
        while True:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Gather metrics
            sys_metrics = metrics.get_system_metrics()
            
            # Print real-time metrics
            print(f"[{current_time}] CPU: {sys_metrics['cpu_percent']:5.1f}% | "
                  f"Mem: {sys_metrics['mem_percent']:5.1f}% | "
                  f"Disk: {sys_metrics['disk_percent']:5.1f}%", end="")
            
            # Log metrics
            log_system_metrics(
                sys_metrics['cpu_percent'],
                sys_metrics['mem_percent'],
                sys_metrics['disk_percent']
            )
            
            # Need top process if CPU is high
            top_proc = None
            if sys_metrics['cpu_percent'] > thresholds['cpu']:
                top_proc = metrics.get_top_process_by_cpu()
            
            # Check thresholds and generate alerts
            active_alerts = alerts.check_thresholds(sys_metrics, thresholds, top_proc)
            
            if active_alerts:
                print(f"  [!] {len(active_alerts)} Alert(s)")
                for alert in active_alerts:
                    print(f"    -> {alert}")
            else:
                print("  [OK]")
            
            # Use max(0, interval - 1) because get_system_metrics() blocks for 1 second 
            # to measure CPU utilization accurately over that second.
            sleep_time = max(0, args.interval - 1)
            if sleep_time > 0:
                time.sleep(sleep_time)
            
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")
        
if __name__ == "__main__":
    main()
