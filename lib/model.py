from PyQt5.QtCore import QThread, pyqtSignal
import time
import os
import re
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED

LANG = []
ONLINE = []

# def get_net_segment():
#     with os.popen("arp -a") as res:  # 执行 arp -a ，返回一个可读取的文件对象 res
#         count = 0
#         for line in res:
#             line = line.strip()  # 移除行首和行尾的空白字符。
#             if line.startswith("接口") or line.startswith("Interface"): # 检查行是否以“接口”或“Interface”开头。
#                 count = count + 1  # 计数器加1，用于检测第几次出现网络接口行
#                 net_segment = re.findall(
#                     "(\d+\.\d+\.\d+)\.\d+", line)[0]  # 使用正则表达式提取网络段（三段IP地址）
#             if count == 2:   # 在找到第二个网络接口行时结束
#                 return 0     
#     return net_segment   # 返回网段

#原先的get_net_segment改为get_network_interfaces和get_net_segments


# def clear_arp_cache():
#     result = os.system('arp -d')
#     if result == 0:
#         print("ARP cache has been cleared.")
#     else:
#         print("Failed to clear ARP cache.")
# 用 netsh 命令来清除 ARP 缓存,有出现过好几次arp参数错误

def clear_arp_cache():
    result = os.system('netsh interface ip delete arpcache')
    if result == 0:
        print("ARP cache has been cleared.")
    else:
        print("Failed to clear ARP cache. \n Check that you are using a PowerShell(administrator) to start the script")



def get_network_interfaces():
    interfaces = []
    # 获取所有网络接口的名称（别名）
    command = 'powershell "Get-NetIPAddress | Select-Object -ExpandProperty InterfaceAlias"'
    
    # 使用 os.popen 执行 PowerShell 命令，并获取命令输出的结果
    with os.popen(command) as res:
        for line in res:
            line = line.strip()  # 去除每行的首尾空白字符
            if line and line not in interfaces:  # 确保没有重复的接口名称
                interfaces.append(line)  # 将接口名称添加到列表中
    return interfaces  # 返回包含所有网络接口名称的列表

def get_net_segments(interface):
    net_segments = []
    # 获取指定网络接口的所有 IPv4 地址，$_获取上一个管道符运过来的所有对象，AddressFamily= ipv4/ipv6 , ExpandProperty 展开说说叭 
    # -InterfaceAlias 参数指定接口别名
    # Where-Object 过滤条件，只获取 IPv4 地址
    # Select-Object 提取 IPAddress 属性的值
    command = f'powershell "Get-NetIPAddress -InterfaceAlias \'{interface}\' | Where-Object {{ $_.AddressFamily -eq \'IPv4\' }} | Select-Object -ExpandProperty IPAddress"'
    
    # 使用 os.popen 执行 PowerShell 命令，并获取命令输出的结果
    with os.popen(command) as res:
        for line in res:
            line = line.strip()  # 去除每行的首尾空白字符
            # 使用正则表达式匹配 IP 地址前三段
            net_segment = re.findall(r"(\d+\.\d+\.\d+)\.\d+", line)
            if net_segment:
                net_segments.append(net_segment[0])  # 将匹配到的前三段 IP 地址添加到列表中
    return net_segments  # 返回包含所有匹配到的网络段的列表


def ping_net_segments_all(net_segments): 
    with ThreadPoolExecutor(max_workers=4) as executor:  # 最多可以有4个并发的线程同时运行
        for net_segment in net_segments:
            for i in range(1, 255):
                executor.submit(os.popen, f"ping -w 1 -n 1 {net_segment}.{i}")  # -w 1，等待一秒，-n 1发起一个请求

# def get_arp_ip_mac():
#     header = None
#     with os.popen("arp -a") as res:
#         for line in res:
#             line = line.strip()
#             if not line or line.startswith("接口") or line.startswith("Interface"):
#                 global LANG
#                 if line.startswith("接口"):
#                     LANG = ['接口', '物理地址', '类型', 'Internet 地址']
#                 elif line.startswith("Interface"):
#                     LANG = ['Interface', 'Physical Address', 'Type', 'Internet Address']
#                 continue
#             if header is None:
#                 header = re.split(" {2,}", line.strip())
#                 break
#         # 读取 ARP 表数据
#         df = pd.read_csv(res, sep=" {2,}", names=header, header=None, engine='python')
    
#     # 过滤以 98- 开头的 MAC 地址
#     df_bool = df[LANG[1]].str.startswith("b0-")
#     df = df[df_bool].reset_index(drop=True)
    
#     return df

def get_arp_ip_mac():
    global LANG
    LANG = []
    header = None
    with os.popen("arp -a") as res:
        for line in res:
            line = line.strip()
            if not line or line.startswith("接口") or line.startswith("Interface"):
                if line.startswith("接口"):
                    LANG = ['接口', '物理地址', '类型', 'Internet 地址']
                elif line.startswith("Interface"):
                    LANG = ['Interface', 'Physical Address', 'Type', 'Internet Address']
                continue
            if header is None:
                header = re.split(" {2,}", line.strip())
                break
        # Read ARP table data
        df_pretraite = pd.read_csv(res, sep=" {2,}", names=header, header=None, engine='python')
    
    # Filter MAC addresses starting with b0-
    df = df_pretraite[df_pretraite[LANG[1]].str.startswith("98-")].reset_index(drop=True)
    print(f"first filtred: {df}")
    return df


def ping_ip_list(ips, max_workers=4):
    print("Scanning online AP now")
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_tasks = []
        for ip in ips:
            future_tasks.append(executor.submit(os.popen, f"ping -w 1 -n 1 {ip}"))
        wait(future_tasks, return_when=ALL_COMPLETED)

def get_ap(interface):
    clear_arp_cache()

    net_segments = get_net_segments(interface)
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