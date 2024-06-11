from hashlib import md5
import re, os


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
    data = []  # 初始化一个空列表用于存储处理后的数据
    with open(file, 'r', encoding='utf-8') as f:  # 打开文件，以读取模式和utf-8编码
        lines_unhandled = f.readlines()  # 读取文件的所有行，并返回一个列表，每行作为列表中的一个元素
        lines_unhandled = [x.strip() for x in lines_unhandled]  # 去除每行的前后空白字符
        lines = list(set(lines_unhandled))  # 去除重复行
        lines.sort()  # 对行进行排序
        lines.remove('')  # 移除空行
        print(lines)  # 输出处理后的行，供调试使用
        if lines:  # 如果处理后的行列表不为空
            for line in lines:  # 遍历每一行
                line = line.strip()  # 去除每行的前后空白字符
                # 忽略以 "#" 开头的行，或者包含 "=;"、"= ;"、"=  ;" 的行
                if line[0] == "#" or "=;" in line or "= ;" in line or "=  ;" in line:
                    continue
                line = line.split(';')[0]  # 按照分号分割行，并取第一部分
                if "descript" not in line:  # 如果行中不包含 "descript" 字符串
                    line = ''.join(line.split())  # 移除行中的所有空白字符
                # 对单引号进行转义处理，将单引号替换为反斜杠加单引号
                line = line.replace("'", "\\'")
                data.append(line)  # 将处理后的行添加到数据列表中
    return data  # 返回处理后的数据列表