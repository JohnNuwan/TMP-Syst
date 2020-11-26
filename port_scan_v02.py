import requests
import pandas as pd 
import socket
import threading
from queue import Queue


res = requests.get("https://ipinfo.io/")

data = res.json()
location = data['loc']
latitude = float(location[0])
longitude = float(location[1])

df = pd.DataFrame(list(data.items()), columns=['Key', 'info'])
print(df.head())



ip_target = df["info"][0]

print("#"*60)
print(ip_target)
print("#"*60)

target = ip_target

queue = Queue()
open_ports = []

def port_scan(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((target, port))
        return True
    except Exception as e:
        return False

def fill_queue(port_list):
    for port in port_list:
        queue.put(port)


def worker():
    while not queue.empty():
        port = queue.get()
        if port_scan(port):
            print(f"Port {port} is open")
            open_ports.append(port)

port_list = range (1, 1024)
fill_queue(port_list)
thread_list = []

for t in range(100):
    thread = threading.Thread(target=worker)
    thread_list.append(thread)

for thread in thread_list:
    thread.start()

for thread in thread_list:
    thread.join()

print(f"Open Port is: {open_ports}")