import os,re,pandas as pd
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED


def get_network_ips():
    ips = []
    # 获取所有网络接口的名称（别名）
    command = 'ipconfig'
    
    # 使用 os.popen 执行 PowerShell 命令，并获取命令输出的结果
    with os.popen(command) as res:
        for line in res:
            line = line.strip()  # 去除每行的首尾空白字符
            if line and line not in ips and line.startswith('IPv4 Address'):  # 确保没有重复的接口名称
                ips.append(line.split(": ")[1])  # 将接口名称添加到列表中
            elif line and line not in ips and line.startswith('IPv4 地址'):  # 确保没有重复的接口名称
                ips.append(line.split(": ")[1])  # 将接口名称添加到列表中
    return ips  # 返回包含所有网络接口名称的列表


def ping_net_segment_all(net_segment):
    with ThreadPoolExecutor(max_workers=4) as executor:
        for i in range(1, 255):
            executor.submit(os.popen, f"ping -w 1 -n 1 {net_segment}.{i}")


def get_arp_ip_mac(ip):
    header = None
    interface_found = False
    with os.popen("arp -a") as res:
        
        # get header
        # res = res.readlines()
        # print(res)
        data = []

        for line in res:
            line = line.strip()
            # print(line)
            if not line or line.startswith("接口") or line.startswith("Interface"):
                global LANG
                if line.startswith("接口"):
                    LANG = ['接口','物理地址','动态', 'Internet 地址']
                elif line.startswith("Interface"):
                    LANG = ['Interface','Physical Address','dynamic', 'Internet Address']
                if ip in line:
                    interface_found = True
                else:
                    interface_found = False
                continue
            if header is None:
                print(line)
                header = re.split(" {2,}", line.strip())
                
                continue
            if interface_found:
                if not line or line.startswith("Internet Address") or line.startswith("Internet 地址"):
                    if header is None:
                        header = re.split(" {2,}", line.strip())
                    continue
                # 收集ARP表中的数据
                if line:
                    data.append(re.split(" {2,}", line.strip()))
        # choose AP who start with 98-
        # df = pd.read_csv(res, sep=" {2,}",
        #                  names=header, header=0, engine='python')
        
        if not data:
            print(f"No data found for Interface: {ip}")
            return pd.DataFrame()  # Return empty DataFrame if no data found
        print(header)
        df = pd.DataFrame(data, columns=header)
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


def get_ap(ip) -> pd.DataFrame:
    # seg = get_net_segment()
    seg_ip = re.findall(
                    "(\d+\.\d+\.\d+)\.\d+", ip)[0]
    ping_net_segment_all(seg_ip)
    df = get_arp_ip_mac(ip)
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
    print(ip)
    return df
