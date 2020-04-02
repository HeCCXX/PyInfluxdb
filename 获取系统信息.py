import threading
import time
import psutil
import socket
from influxdb import InfluxDBClient

client=InfluxDBClient('localhost','8086','admin','','test')

def get_ip():
    s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255',0))
        IP=s.getsockname()[0]
        print(IP)
    except Exception as e:
        print(e)
        IP='127.0.0.1'
    finally:
        s.close()
    return IP
ip=get_ip()
def get_cpu(sec):
    while True:
        time.sleep(sec)
        info=psutil.cpu_percent(0)
        print(info)
        text=[
            {
                'measurement':'cpu_info',
                'tags':{
                    'host':ip
                },
                'fields':{
                    'percent':info
                }
            }
        ]
        client.write_points(text)

def get_memory(sec):
    while True:
        time.sleep(sec)
        info=psutil.virtual_memory()
        print(info)
        text=[
            {
                "measurement":"memory_info",
                    "tags":{
                           "host":ip
                },
                "fields":{
                            "mem_percent":info.percent,
                            "mem_used":info.used,
                            "mem_free":info.free,
                }
            }
        ]
        client.write_points(text)
def get_disk(sec):
    while True:
        time.sleep(sec)
        info=psutil.disk_usage('/')
        print(info)
        text=[
            {
                "measurement":"disk_info",
                "tags":{
                           "host":ip
                },
                "fields":{
                            "disk_used":info.used,
                            "disk_free":info.free,
                            "disk_percent":info.percent,
                }
            }
        ]
        client.write_points(text)
def get_network(sec):
    while True:
        time.sleep(sec)
        info = psutil.net_io_counters(pernic=True)['WLAN']
        print(info)
        text=[
            {
                "measurement":"network_info",
                "tags":{
                           "host":ip
                },
                "fields":{
                            "bytes_sent":info.bytes_sent,
                            "bytes_recv":info.bytes_recv,
                }
             }
        ]
        client.write_points(text)
th=[]
th.append(threading.Thread(target=get_cpu,args=(1,)))
th.append(threading.Thread(target=get_memory, args=(1,)))
th.append(threading.Thread(target=get_disk, args=(1,)))
th.append(threading.Thread(target=get_network, args=(1,)))
for a in th:
    a.start()
while True:
    pass