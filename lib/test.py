# import os
# import re

# def get_net_segments(interface):
#     net_segments = []
#     command = f'powershell "Get-NetIPAddress -InterfaceAlias \'{interface}\' | Where-Object {{ $_.AddressFamily -eq \'IPv4\' }} | Select-Object -ExpandProperty IPAddress"'
#     with os.popen(command) as res:
#         for line in res:
#             line = line.strip()
#             net_segment = re.findall(r"(\d+\.\d+\.\d+)\.\d+", line)
#             if net_segment:
#                 net_segments.append(net_segment[0])
#     return net_segments

# def get_network_interfaces():
#     interfaces = []
#     command = 'powershell "Get-NetIPAddress | Select-Object -ExpandProperty InterfaceAlias"'
#     with os.popen(command) as res:
#         for line in res:
#             line = line.strip()
#             if line and line not in interfaces:  # Ensure no duplicates
#                 interfaces.append(line)
#     return interfaces

# # Test the functions
# def main():
#     interfaces = get_network_interfaces()
#     print("Available network interfaces:", interfaces)
#     for interface in interfaces:
#         net_segments = get_net_segments(interface)
#         print(f"Net segments for {interface}:", net_segments)

# if __name__ == "__main__":
#     main()

import time

# 方法一
start_time = time.perf_counter()
result = ""
for char in range(26000):
    result += chr(ord('A') + (char % 26)) * 26
method_one_time = time.perf_counter() - start_time

# 方法二
start_time = time.perf_counter()
result_list = []
for char in range(26000):
    result_list.append(chr(ord('A') + (char % 26)) * 26)
result = ''.join(result_list)
method_two_time = time.perf_counter() - start_time

print(f"方法一运行时间: {method_one_time:.10f} 秒")
print(f"方法二运行时间: {method_two_time:.10f} 秒")

