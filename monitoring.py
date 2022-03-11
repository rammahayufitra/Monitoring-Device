import psutil 
import GPUtil 
import os 


class Monitoring():
    def __init__(self):
        self.gpus =GPUtil.getGPUs() 
        self.temp = '/sys/class/thermal/thermal_zone0/temp'

    def get_size(self, bytes, suffix="B"):
        factor = 1024
        for unit in ["", "K", "M", "G", "T", "P"]:
            if bytes < factor:
                return f"{bytes:.2f}{unit}{suffix}"
            bytes /= factor

    def info_gpu(self):
        for gpu in self.gpus:
            gpu_name = gpu.name
            gpu_temp = gpu.temperature
            gpu_free_memory = self.get_size(gpu.memoryFree)
            gpu_used_memory = self.get_size(gpu.memoryUsed)
            gpu_total_memory = self.get_size(gpu.memoryTotal)
            json_gpu ={
                "gpu_name": gpu_name, 
                "gpu_temp":gpu_temp, 
                "gpu_free_memory":gpu_free_memory,
                "gpu_used_memory": gpu_used_memory, 
                "gpu_total_memory":gpu_total_memory
            }
        return json_gpu
    
    def info_memory(self):
        svmem = psutil.virtual_memory()
        total_ram = self.get_size(svmem.total)
        available_ram = self.get_size(svmem.available)
        used_ram = self.get_size(svmem.used)
        percentage = self.get_size(svmem.percent)
        json_info_memory = {
            "total_ram" : total_ram,
            "available_ram": available_ram,
            "used_ram": used_ram, 
            "percentage": percentage
        }
        return json_info_memory

    def info_disk(self):
        partitions = psutil.disk_partitions()
        for partition in partitions:
            try:
                partition_usage =  psutil.disk_usage(partition.mountpoint)
            except PermissionError:
                continue
            total_size_disk = self.get_size(partition_usage.total)
            used_disk = self.get_size(partition_usage.used)
            available_disk = self.get_size(partition_usage.free)
            percentage = self.get_size(partition_usage.percent)
        json_info_disk = {
            "total_size_disk" : total_size_disk,
            "used_disk" : used_disk,
            "available_disk" : available_disk,
            "percentage" : percentage
        }
        return json_info_disk

    def info_cpu(self):
        temp_cpu = 0.0
        if os.path.isfile(self.temp):
            with open(self.temp) as f:
                line = f.readline().strip()
            if line.isdigit():
                temp_cpu = float(line) / 1000
        cpu_usage_per_core = psutil.cpu_percent(percpu=True, interval=1)
        total_cpu_usage = psutil.cpu_percent()
        json_info_cpu = {
            "temp_cpu" : f'{temp_cpu} \u2103',
            "cpu_core1" : f'{cpu_usage_per_core[0]} %',
            "cpu_core2" : f'{cpu_usage_per_core[1]} %',
            "cpu_core3" : f'{cpu_usage_per_core[2]} %',
            "cpu_core4" : f'{cpu_usage_per_core[3]} %',
            "total_cpu_usage" : f'{total_cpu_usage} %'
        }
        return json_info_cpu
    

monitoring = Monitoring()
