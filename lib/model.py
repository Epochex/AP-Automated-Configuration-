from PyQt5.QtCore import QThread,pyqtSignal
import time,os,re,time,pandas as pd
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED

def get_net_segment():
    with os.popen("arp -a") as res:  # os.popen执行了arp -a，返回了一个可以读取的文件对象。pipe.read()读取该命令的输出，并将其存储在变量output中
        count = 0
        for line in res:
            line = line.strip()
            if line.startswith("接口") or line.startswith("Interface"):
                count = count + 1
                net_segment = re.findall(
                    "(\d+\.\d+\.\d+)\.\d+", line)[0]
            if count == 2:
                return 0
    return net_segment

def ping_net_segment_all(net_segment):
    with ThreadPoolExecutor(max_workers=4) as executor:
        for i in range(1, 255):
            executor.submit(os.popen, f"ping -w 1 -n 1 {net_segment}.{i}")


def get_arp_ip_mac():
    header = None
    with os.popen("arp -a") as res:
        # get header
        for line in res:
            line = line.strip()
            if not line or line.startswith("接口") or line.startswith("Interface"):
                global LANG
                if line.startswith("接口"):
                    LANG = ['接口','物理地址','动态', 'Internet 地址']
                elif line.startswith("Interface"):
                    LANG = ['Interface','Physical Address','dynamic', 'Internet Address']
                continue
            if header is None:
                header = re.split(" {2,}", line.strip())
                break
        # choose AP who start with 98-
        df = pd.read_csv(res, sep=" {2,}",
                         names=header, header=None, engine='python')
        print(df)
        df_bool = df[LANG[1]].str.startswith("98-")
        df = df[df_bool].reset_index(drop=True)
    return df


def ping_ip_list(ips, max_workers=4):
    print("Scanning online AP now")
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_tasks = []
        for ip in ips:
            future_tasks.append(executor.submit(os.popen, f"ping -w 1 -n 1 {ip}"))
        wait(future_tasks, return_when=ALL_COMPLETED)


def get_ap():
    seg = get_net_segment()
    if seg == 0:
        return 0
    ping_net_segment_all(seg)
    df = get_arp_ip_mac()
    if LANG[0] == 'Interface':
        df = df.loc[df.Type == LANG[2], [LANG[3], LANG[1]]]
    elif LANG[0] == '接口':
        df = df.loc[df.类型 == LANG[2], [LANG[3], LANG[1]]]
    print("AP currently online:")
    if df.empty:
        print("No AP online, you can connect APs")
    else:
        print(df)
    ping_ip_list(df[LANG[3]].values)
    return df

def get_ap_pass(last):
    while 1:
        df = get_arp_ip_mac()
        if df.empty:
            continue
        if LANG[0] == 'Interface':
            df = df.loc[df.Type == LANG[2], [LANG[3], LANG[1]]]
            online = df.loc[~df['Physical Address'].isin(last['Physical Address'])]
        elif LANG[0] == '接口':
            df = df.loc[df.类型 == "动态", ["Internet 地址", "物理地址"]]
            online = df.loc[~df.物理地址.isin(last.物理地址)]
        if online.shape[0] > 0:
            print("New AP:")
            print(online)
            i = 1
            for k,v in online.values.tolist():
                data = str(i) + '                    '+ k + '                    ' + v
                i = i + 1
            global ONLINE
            ONLINE.append(data) if data not in ONLINE else ONLINE
        time.sleep(10)
        print(ONLINE)
        ping_ip_list(df["Internet 地址"].values)
        online = online.values.tolist()
