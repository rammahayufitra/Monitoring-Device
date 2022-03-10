import psutil
import GPUtil
import numpy as np
import os



gpus = GPUtil.getGPUs()


def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


def info_cpu():
    """
    temp_cpu dalam celcius
    cpu_usage_core dalam persen 
    total_cpu_usage dalam persen
    
    """
    temp_cpu = 0.0
    if os.path.isfile('/sys/class/thermal/thermal_zone0/temp'):
        with open('/sys/class/thermal/thermal_zone0/temp') as f:
            line = f.readline().strip()
        if line.isdigit():
            temp_cpu = float(line) / 1000
    cpu_usage_per_core = psutil.cpu_percent(percpu=True, interval=1)
    total_cpu_usage = psutil.cpu_percent()
    return ([temp_cpu,cpu_usage_per_core, total_cpu_usage])

def info_memory():
    svmem = psutil.virtual_memory()
    total_ram = get_size(svmem.total)
    available_ram = get_size(svmem.available)
    used_ram = get_size(svmem.used)
    percentage = get_size(svmem.percent)
    return([total_ram, available_ram, used_ram, percentage])

def info_disk():
    partitions = psutil.disk_partitions()
    for partition in partitions:
        try:
            partition_usage =  psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            continue
        total_size_disk = get_size(partition_usage.total)
        used_disk = get_size(partition_usage.used)
        available_disk = get_size(partition_usage.free)
        percentage = get_size(partition_usage.percent)
    return ([total_size_disk, used_disk, available_disk, percentage])

def info_gpu():
    """
    temp gpu dalam celcius
    """
    for gpu in gpus:
        gpu_name = gpu.name
        gpu_temp = gpu.temperature
        gpu_free_memory = gpu.memoryFree
        gpu_used_memory = gpu.memoryUsed
        gpu_total_memory = gpu.memoryTotal
    return ([gpu_name, gpu_temp, gpu_free_memory, gpu_used_memory, gpu_total_memory])
    
while True:
    print(info_disk(), end= ' ')