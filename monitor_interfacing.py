from flask import Flask 
from info_device import info_cpu, info_gpu, info_memory, info_disk


app = Flask(__name__)

@app.route('/monitoring', methods=['GET'])
    
def get_monitoring():
    
    temparature_cpu,cpu_use_per_core, total_cpu_usage = info_cpu() 
    gpu_name, gpu_temp, gpu_free_memory, gpu_used_memory, gpu_total_memory = info_gpu()
    total_ram, available_ram, used_ram, percentage = info_memory()
    total_size_disk, used_disk, available_disk, percentage = info_disk()
   
    monitoring_device = {
        "info_cpu": {
            "temparature_cpu": f'{temparature_cpu} \u2103',
            "cpu_core1": f'{cpu_use_per_core[0]} %',
            "cpu_core2": f'{cpu_use_per_core[1]} %',
            "cpu_core3": f'{cpu_use_per_core[2]} %',
            "cpu_core4": f'{cpu_use_per_core[3]} %', 
            "total_cpu_usage": f'{total_cpu_usage} %'
        },
        "info_gpu":{
            "gpu_name": gpu_name,
            "gpu_temp": f'{gpu_temp} \u2103',
            "gpu_free_memory": gpu_free_memory,
            "gpu_usage_memory": gpu_used_memory,
            "gpu_total_memory": gpu_total_memory
        },
        "info_memory":{
            "total_ram": total_ram,
            "available_ram": available_ram,
            "used_ram": used_ram,
            "percentage": percentage
        },
        "info_disk":{
            "total_size_disk": total_size_disk,
            "used_disk": used_disk,
            "available_disk": available_disk,
            "percentage": percentage
        }
    }
    return monitoring_device
    
