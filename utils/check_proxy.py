'''
This file is created to check the validity of the proxies in the proxy_List.txt file.
The valid proxies are stored in the valid_proxy.txt file.
'''

# ----------------------- Modules -------------------------------- #
import threading
import queue
import requests


# ------------------ Using Queue structure ----------------------- #
q = queue.Queue()
valid = []


# ------------------ reading data from file ---------------------- #
with open("txt_files/proxy_List.txt", 'r') as f:
    proxy = f.read().split('\n')
    for p in proxy:
        q.put(p)


# ---------------------- Checking proxy -------------------------- #
def check_proxy():
    global q
    while not q.empty():
        proxy = q.get()
        try:
            res = requests.get('http://ipinof.io/json', proxies={'http': proxy}, timeout=5)
        except:
            continue
        
        if res.status_code == 200:
            valid.append(proxy)
    
    with open("txt_files/valid_proxy.txt",'a',newline="") as fw:
        for v in valid:
            fw.write(v + '\n')


# -------------------------- Program ---------------------------- #
def Start_Checking_Proxy():
    for _ in range(10):
        t = threading.Thread(target=check_proxy)
        t.start()


# -------------------------- Main ------------------------------- #
if __name__ == "__main__":
    Start_Checking_Proxy()