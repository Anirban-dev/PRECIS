import psutil
from datetime import datetime


class SystemMonitor:

    def get_system_metrics(self):

        return {

            "timestamp":
                datetime.utcnow().isoformat(),

            "cpu_usage":
                psutil.cpu_percent(),

            "memory_usage":
                psutil.virtual_memory().percent,

            "disk_usage":
                psutil.disk_usage("/").percent
        }