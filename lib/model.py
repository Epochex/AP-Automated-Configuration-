from PyQt5.QtCore import QThread,pyqtSignal
import time,os,re,time,pandas as pd
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED

def get_net_segments():
    net_segments = []
    with os.popen("arp -a") as res:
        for line in res:
            line = line.strip()
            if line.startswith("接口") or line.startswith("Interface"):
                net_segment = re.findall("(\d+\.\d+\.\d+)\.\d+", line)
                if net_segment:
                    net_segments.append(net_segment[0])
    return net_segments

def ping_net_segments_all(net_segments):
    with ThreadPoolExecutor(max_workers=4) as executor:
        for net_segment in net_segments:
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
    with ThreadPoolExecutor(max_workers=max_workers) as executor: #executor 线程池执行器对象
        future_tasks = []
        for ip in ips:
            # 使用 executor.submit 方法提交一个ping任务给线程池执行，每个任务执行 os.popen(f"ping -w 1 -n 1 {ip}") 命令
            # future_tasks.append 将每个提交的任务（Future 对象）添加到 future_tasks 列表中。
            future_tasks.append(executor.submit(os.popen, f"ping -w 1 -n 1 {ip}"))
        wait(future_tasks, return_when=ALL_COMPLETED)

# 清arp缓存
def clear_arp_cache():
    if os.name == 'nt':  # windows
        os.system('arp -d *')
    else:  # Unix
        os.system('sudo ip -s -s neigh flush all')



def get_ap():
    # 清除ARP缓存
    clear_arp_cache()

    net_segments = get_net_segments()
    if not net_segments:
        return 0
    
    ping_net_segments_all(net_segments)
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



# 监控函数，持续检查AP变化
def get_ap_pass(last):
    while 1:
        df = get_arp_ip_mac()
        if df.empty:
            continue
        if LANG[0] == 'Interface':
            df = df.loc[df.Type == LANG[2], [LANG[3], LANG[1]]]
            
            online = df.loc[~df['Physical Address'].isin(last['Physical Address'])]
            # df['Physical Address']表示之前已知的mac地址，然后和新检测出来的mac进行isin比较，isin返回bool对象，true为一样，false为不一样，~取反
        elif LANG[0] == '接口':
            df = df.loc[df.类型 == "动态", ["Internet 地址", "物理地址"]]
            online = df.loc[~df.物理地址.isin(last.物理地址)]
        if online.shape[0] > 0: # 若大于0则有新的AP
            print("New AP:")
            print(online)
            i = 1
            for k,v in online.values.tolist():
                data = str(i) + '                    '+ k + '                    ' + v  # 转化为字符串(序号+IP+MAC)
                i = i + 1
            global ONLINE
            ONLINE.append(data) if data not in ONLINE else ONLINE #如果 data 不在 ONLINE 列表中，则将其添加到 ONLINE，否则保持不变
        time.sleep(10) # 10秒循环一次
        print(ONLINE)
        ping_ip_list(df["Internet 地址"].values)
        online = online.values.tolist()
