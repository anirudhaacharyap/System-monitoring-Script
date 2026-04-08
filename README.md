# System Monitoring Tool

A lightweight, Python-based System Monitoring Tool designed with Site Reliability Engineering (SRE) best practices in mind. It provides real-time tracking of critical system metrics, logs historical data, and generates alerts when predefined thresholds are breached.

## Features

- **Real-time Monitoring**: Tracks CPU, Memory, and Disk usage at configurable intervals.
- **Alerting System**: Generates warnings when metrics exceed configurable thresholds.
- **Top Process Identification**: When CPU usage is high, it identifies and logs the exact process consuming the most CPU.
- **Structured Logging**: 
  - `logs/system.log`: Maintains a continuous history of all system metrics along with timestamps.
  - `logs/alerts.log`: Isolated log specifically for threshold breaches and critical events.
- **CLI Configuration**: Fully customizable via command-line arguments.

## Project Structure

```text
├── main.py              # Application entry point
├── config.py            # Global default configurations
├── requirements.txt     # Python dependencies
├── README.md            # Documentation
├── monitor/             # Core monitoring modules
│   ├── metrics.py       # Metrics collection logic (CPU, Mem, Disk usages & top process)
│   ├── alerts.py        # Threshold evaluation and alerting logic
│   └── logger.py        # File-based logging setup that separates system and alert logs
└── logs/                # Automatically generated log files
    ├── system.log       
    └── alerts.log       
```

## Setup Instructions

1. Navigate to the project directory
2. It's recommended to create and activate a Python virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

**Run with default configurations:**
```bash
python main.py
```

**Run with custom configurations:**
You can specify the checking interval (in seconds) and custom thresholds (in percentages) for CPU, Memory, and Disk.
```bash
python main.py --interval 2 --cpu-threshold 75.0 --mem-threshold 80.0 --disk-threshold 90.0
```

**View all available options:**
```bash
python main.py --help
```

## Example Output

**Terminal execution:**
```text
============================================================
Starting System Monitoring Tool
Interval: 5 seconds
Thresholds -> CPU: 80.0%, Memory: 80.0%, Disk: 85.0%
============================================================
Press Ctrl+C to stop.

[2026-04-08 10:30:00] CPU:  12.5% | Mem:  45.2% | Disk:  60.1%  [OK]
[2026-04-08 10:30:05] CPU:  85.2% | Mem:  45.3% | Disk:  60.1%  [!] 1 Alert(s)
    -> High CPU Usage detected: 85.2% (Threshold: 80.0%). Top process: python.exe (PID: 1234, CPU: 82.1%)
```

**`logs/system.log` Output:**
```text
2026-04-08 10:30:00,123 - INFO - CPU: 12.5% | Memory: 45.2% | Disk: 60.1%
2026-04-08 10:30:05,234 - INFO - CPU: 85.2% | Memory: 45.3% | Disk: 60.1%
```

**`logs/alerts.log` Output:**
```text
2026-04-08 10:30:05,235 - WARNING - ALERT: High CPU Usage detected: 85.2% (Threshold: 80.0%). Top process: python.exe (PID: 1234, CPU: 82.1%)
```
