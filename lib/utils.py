from hashlib import md5
import re, os
from utils import *

import os

def clear_arp_cache():
    os.system('arp -d')
    print("ARP cache cleared")


TRANSLATION = {
    "rul_enable":"Mode Test: ",
    "manager_passwd":"Password for admin: ",
    "ew_ipaddr":"ESL-working Addr: ",
    "ew_port":"ESL-working Port: ",
    "ew_ssl":"ESL-Working SSL: ",
    "net_dhcp":"DHCP enable: ",
    "net_ipaddr":"IP address: ",
    "net_netmask":"Netmask: ",
    "net_router":"Gateway: ",
    "net_dns1":"DNS 1: ",
    "net_dns2":"DNS 2: ",
    "descript":"Description: ",
    "ew_udp":"ESL-Working Auto Search: "
}

WARNING = '''请根据需要更改每一行开头的符号
# 代表为ap默认的配置，无需特意更改，也不在软件中显示
! 代表为需要更改的配置，需要在软件中配置并显示
无特殊符号开头的配置代表仅在软件中显示


Please change the symbol at the beginning of each line as needed
# is the default ap configuration, no need to change it, and it is not displayed in the software
! represents the configuration that needs to be changed, and needs to be configured and displayed in the software
Configurations that do not start with a special symbol are only displayed in the software


Veuillez modifier le symbole au début de chaque ligne selon les besoins.
# signifie que l'ap est configuré par défaut et n'a pas besoin d'être modifié ou affiché dans le logiciel
! est la configuration qui doit être modifiée, et qui doit être configurée et affichée dans le logiciel
Les configurations qui ne commencent pas par un symbole spécial sont uniquement affichées dans le logiciel.'''


def encrypt_md5(s):
    # 创建md5对象
    new_md5 = md5()
    # 这里必须用encode()函数对字符串进行编码，不然会报 TypeError: Unicode-objects must be encoded before hashing
    new_md5.update(s.encode(encoding='utf-8'))
    # 加密
    return new_md5.hexdigest()

def isIP(s):
    p = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if p.match(s):
        return True
    else:
        return False

def change_ip_bin(ip):
    ip_list = ip.split('.')
    bin_ip_list = []
    for i in ip_list:
        bin_ip_list.append(bin(int(i)).replace('0b','').rjust(8,'0'))
    return bin_ip_list

def change_bin_ip(bin_info):
    start = 0
    bin_list = []
    while len(bin_info) >= start+8:
        end = start + 8
        a = bin_info[start:end]
        start += 8
        b = int(a, 2)
        bin_list.append(str(b))
    return bin_list

def range_of_ip(ip, submask):
    ip_bin_list = change_ip_bin(ip)
    submask_bin_list = change_ip_bin(submask)
    one_index = ''.join(submask_bin_list).find('0')
    # 网络地址,为1的部分
    submask_bin = ''.join(submask_bin_list)[0:one_index]
    # 取IP地址中的相同位数
    ip_bin = ''.join(ip_bin_list)[0:one_index]
    # 进行 与 逻辑运算
    net_int_addr = int(submask_bin, 2) & int(ip_bin, 2)
    # 合并后的网络地址的二进制
    with_bin_net = bin(net_int_addr).replace('0b', '').rjust(one_index, '0')
    # 起始网络地址二进制
    # 广播地址二进制
    net_bin_addr = change_bin_ip(with_bin_net.ljust(32, '0'))
    net_bin_addr[3] = "236"
    broad_bin_addr = change_bin_ip(with_bin_net.ljust(32, '1'))
    broad_bin_addr[3] = "254"
    return [".".join(broad_bin_addr), ".".join(net_bin_addr)]


def get_config():
    path = "config" #文件夹目录
    files= os.listdir(path) #得到文件夹下的所有文件名称
    # for file in files: #遍历文件夹
    #      if not os.path.isdir(file): #判断是否是文件夹，不是文件夹才打开
    #           f = open(path+"/"+file); #打开文件
    #           iter_f = iter(f); #创建迭代器
    #           str = ""
    #           for line in iter_f: #遍历文件，一行行遍历，读取文本
    #               str = str + line
    #           s.append(str) #每个文件的文本存到list中
    return files


def get_file_config(file):
    data = []
    with open(file,'r',encoding='utf-8') as f:
        lines_unhandled = f.readlines()  

        lines_unhandled = [x.strip() for x in lines_unhandled] # 去掉每行两端的空白字符，并生成新的列表
        lines = list(set(lines_unhandled))  # 去重
        lines.sort()  #排序
        lines.remove('')  # #删除空行
        print(lines)
        if lines:
            for line in lines:
                line = line.strip()
                # #开头是避免不用动的配置，=;应该是避免空值，如果真的是，执行continue循环到下一行
                if line[0] == "#" or "=;" in line or "= ;" in line or "=  ;" in line:   # 跳过以 # 开头的注释行和 结尾是 = ;
                    continue
                line = line.split(';')[0]
                if "descript" in line:
                    line = line.replace("'", "\"")  #包含'就替换为"
                if "descript" not in line:
                    line = ''.join(line.split()) #  line.split()切成列表，''.join重新练成一个没空白字符的字符串
                data.append(line)
    return data   


                    # 切好的数据，大概类似于
                    # data = [
                    #     "rul_enable=true",
                    #     "ew_ipaddr=cora-prd.hanshowcloud.net",
                    #     "ew_port=37022",
                    #     "ew_ssl=true",
                    #     "! descript=\"Vichy AP A\"",
                    #     "ew_udp=false"
                    # ]





# def get_file_config(file):
#     data = []
#     with open(file,'r',encoding='utf-8') as f:
#         lines_unhandled = f.readlines()
#         lines_unhandled = [x.strip() for x in lines_unhandled]
#         lines = list(set(lines_unhandled))
#         lines.sort()
#         lines.remove('')
#         print(lines)
#         if lines:
#             for line in lines:
#                 line = line.strip()
#                 if line[0] == "#" or "=;" in line or "= ;" in line or "=  ;" in line:
#                     continue
#                 line = line.split(';')[0]
#                 if "descript" not in line:
#                     line = ''.join(line.split())
#                 data.append(line)
#     return data