# Health Monitor

A small Python script that checks CPU, memory, and disk usage. It reports `CRITICAL` when any resource reaches 90% and writes results to a log file.

## Run

```bash
pip install -r requirements.txt
python health_monitor.py
```

Exit codes: `0` healthy, `1` critical, `2` error.