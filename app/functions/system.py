import psutil
import platform
import socket
import os
from datetime import datetime

def get_system_info():
    """
    Get comprehensive system information.
    
    Returns:
        dict: System information including OS, CPU, memory, etc.
    """
    info = {
        "platform": platform.system(),
        "platform_release": platform.release(),
        "platform_version": platform.version(),
        "architecture": platform.machine(),
        "hostname": socket.gethostname(),
        "ip_address": socket.gethostbyname(socket.gethostname()),
        "processor": platform.processor(),
        "ram": f"{round(psutil.virtual_memory().total / (1024.0**3))} GB",
        "date_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    return info

def get_cpu_usage():
    """
    Get current CPU usage percentage.
    
    Returns:
        float: CPU usage percentage
    """
    return psutil.cpu_percent(interval=1)

def get_memory_usage():
    """
    Get current memory usage details.
    
    Returns:
        dict: Memory usage statistics
    """
    vm = psutil.virtual_memory()
    return {
        "total": f"{vm.total / (1024.0**3):.2f} GB",
        "available": f"{vm.available / (1024.0**3):.2f} GB",
        "used": f"{vm.used / (1024.0**3):.2f} GB",
        "percentage": f"{vm.percent}%"
    }

def get_disk_usage():
    """
    Get disk usage information.
    
    Returns:
        dict: Disk usage statistics for each drive/partition
    """
    disks = {}
    for partition in psutil.disk_partitions():
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
            disks[partition.mountpoint] = {
                "total": f"{partition_usage.total / (1024.0**3):.2f} GB",
                "used": f"{partition_usage.used / (1024.0**3):.2f} GB",
                "free": f"{partition_usage.free / (1024.0**3):.2f} GB",
                "percentage": f"{partition_usage.percent}%"
            }
        except PermissionError:
            continue
    return disks