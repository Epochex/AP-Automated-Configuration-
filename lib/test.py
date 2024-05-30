from PyQt5.QtCore import QThread, pyqtSignal
import os
import re
import time
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED

def get_net_segment():
    with os.popen("arp -a") as res:  # os.popen执行了arp -a，返回了一个可以读取的文件对象
        count = 0
        net_segment = None
        for line in res:
            line = line.strip()
            print(f"Processing line: {line}")  # 打印当前处理的行
            if line.startswith("接口") or line.startswith("Interface"):
                count += 1
                print(f"Found interface: {line}, count: {count}")  # 打印找到的接口信息和计数器值
                net_segment = re.findall(  # re.findall 返回一个列表
                    "(\d+\.\d+\.\d+)\.\d+", line)[0]  # 括号用于创建捕获组，匹配完整的ip地址，仅捕获前三段
                print(f"Extracted net segment: {net_segment}")  # 打印提取的网络段
            if count == 2:
                print("Count reached 2, returning 0")
                return 0
    print(f"Returning net segment: {net_segment}")  # 打印最终返回的网络段
    return net_segment

def ping_net_segment_all(net_segment):  # 并发ping给定网段中所有ip，副作用函数
    print(f"Pinging all IPs in the segment: {net_segment}")
    with ThreadPoolExecutor(max_workers=4) as executor:
        for i in range(1, 255):
            ip = f"{net_segment}.{i}"
            executor.submit(os.popen, f"ping -w 1 -n 1 {ip}")

def get_arp_ip_mac():
    header = None
    with os.popen("arp -a") as res:
        for line in res:
            line = line.strip()
            if not line or line.startswith("接口") or line.startswith("Interface"):
                global LANG
                if line.startswith("接口"):
                    LANG = ['接口', '物理地址', '动态', 'Internet 地址']
                elif line.startswith("Interface"):
                    LANG = ['Interface', 'Physical Address', 'dynamic', 'Internet Address']
                print(f"Set LANG: {LANG}")  # 打印设置的LANG
                continue
            if header is None:
                header = re.split(" {2,}", line.strip())
                print(f"Extracted header: {header}")  # 打印提取的表头
                break
        df = pd.read_csv(res, sep=" {2,}", names=header, header=None, engine='python')
        print(f"ARP table:\n{df}")  # 打印完整的ARP表
        df_bool = df[LANG[1]].str.startswith("98-")
        df = df[df_bool].reset_index(drop=True)
        print(f"Filtered ARP table:\n{df}")  # 打印过滤后的ARP表
    return df

def ping_ip_list(ips, max_workers=4):
    print("Scanning online AP now")
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_tasks = []
        for ip in ips:
            print(f"Pinging {ip}")  # 打印当前ping的IP地址
            future_tasks.append(executor.submit(os.popen, f"ping -w 1 -n 1 {ip}"))
        wait(future_tasks, return_when=ALL_COMPLETED)

def get_ap():
    seg = get_net_segment()
    if seg == 0:
        print("Segment is 0, exiting")
        return 0
    ping_net_segment_all(seg)  # 会在cmd中输出所有ping过的ip地址
    df = get_arp_ip_mac()
    #组合操作，过滤出动态/dynamic的字段，过滤条件df.Type == LANG[2]，过滤出来之后再选择特定的列,IP地址[3]和MAC[1]
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
    while 1:  # 无限循环，持续监控网络上的接入点
        df = get_arp_ip_mac()  # 获取当前的ARP表数据，返回一个DataFrame
        if df.empty:  # 如果ARP表数据为空
            continue  # 跳过本次循环，继续下一次检查
        if LANG[0] == 'Interface':  # 如果LANG的第一个元素是'Interface'（即英语环境）
            df = df.loc[df.Type == LANG[2], [LANG[3], LANG[1]]]  # 过滤出Type为'dynamic'的行，并选择特定列
            online = df.loc[~df['Physical Address'].isin(last['Physical Address'])]  # 找到新的接入点
        elif LANG[0] == '接口':  # 如果LANG的第一个元素是'接口'（即中文环境）
            df = df.loc[df.类型 == "动态", ["Internet 地址", "物理地址"]]  # 过滤出类型为'动态'的行，并选择特定列
            online = df.loc[~df.物理地址.isin(last.物理地址)]  # 找到新的接入点
        if online.shape[0] > 0:  # 如果有新的接入点
            print("New AP:")  # 打印提示信息
            print(online)  # 打印新的接入点信息
            i = 1
            for k, v in online.values.tolist():  # 遍历新的接入点信息
                data = str(i) + '                    ' + k + '                    ' + v  # 格式化接入点信息
                i += 1
            global ONLINE
            ONLINE.append(data) if data not in ONLINE else ONLINE  # 将新的接入点信息添加到全局变量ONLINE中
        time.sleep(10)  # 等待10秒后再次检查
        print(ONLINE)  # 打印当前在线的接入点信息
        ping_ip_list(df["Internet 地址"].values)  # 对当前的IP地址列表进行ping操作
        online = online.values.tolist()  # 将DataFrame转换为列表


if __name__ == "__main__":
    segment = get_net_segment()
    print("Network Segment:", segment)
    ap_df = get_ap()
    print("Final AP DataFrame:\n", ap_df)
