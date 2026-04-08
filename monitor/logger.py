import logging
import os

# Ensure logs directory exists relative to the project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGS_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOGS_DIR, exist_ok=True)

# System logger setup
system_logger = logging.getLogger("system_logger")
system_logger.setLevel(logging.INFO)
system_handler = logging.FileHandler(os.path.join(LOGS_DIR, "system.log"))
system_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
system_handler.setFormatter(system_formatter)
if not system_logger.handlers:
    system_logger.addHandler(system_handler)

# Alerts logger setup
alerts_logger = logging.getLogger("alerts_logger")
alerts_logger.setLevel(logging.WARNING)
alerts_handler = logging.FileHandler(os.path.join(LOGS_DIR, "alerts.log"))
alerts_formatter = logging.Formatter('%(asctime)s - %(levelname)s - ALERT: %(message)s')
alerts_handler.setFormatter(alerts_formatter)
if not alerts_logger.handlers:
    alerts_logger.addHandler(alerts_handler)

def log_system_metrics(cpu_percent, mem_percent, disk_percent):
    """Log current system metrics to system.log"""
    system_logger.info(f"CPU: {cpu_percent}% | Memory: {mem_percent}% | Disk: {disk_percent}%")

def log_alert(message):
    """Log an alert message to alerts.log"""
    alerts_logger.warning(message)
