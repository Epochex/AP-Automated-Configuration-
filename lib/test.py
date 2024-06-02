import os
import re

def get_net_segments(interface):
    net_segments = []
    command = f'powershell "Get-NetIPAddress -InterfaceAlias \'{interface}\' | Where-Object {{ $_.AddressFamily -eq \'IPv4\' }} | Select-Object -ExpandProperty IPAddress"'
    with os.popen(command) as res:
        for line in res:
            line = line.strip()
            net_segment = re.findall(r"(\d+\.\d+\.\d+)\.\d+", line)
            if net_segment:
                net_segments.append(net_segment[0])
    return net_segments

def get_network_interfaces():
    interfaces = []
    command = 'powershell "Get-NetIPAddress | Select-Object -ExpandProperty InterfaceAlias"'
    with os.popen(command) as res:
        for line in res:
            line = line.strip()
            if line and line not in interfaces:  # Ensure no duplicates
                interfaces.append(line)
    return interfaces

# Test the functions
def main():
    interfaces = get_network_interfaces()
    print("Available network interfaces:", interfaces)
    for interface in interfaces:
        net_segments = get_net_segments(interface)
        print(f"Net segments for {interface}:", net_segments)

if __name__ == "__main__":
    main()
