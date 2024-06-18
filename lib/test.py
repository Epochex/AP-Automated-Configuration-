import time
from concurrent.futures import ThreadPoolExecutor
import os

def ping(ip):
    os.system(f"ping -w 1 -n 1 {ip}")

def ping_net_segments_all(net_segment, max_workers):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for i in range(1, 100):
            ip = f"{net_segment}.{i}"
            futures.append(executor.submit(ping, ip))
        for future in futures:
            future.result()  # 等待所有线程完成

if __name__ == "__main__":
    net_segment = "192.168.1"

    print("开始单线程测试...")
    start_time = time.time()
    ping_net_segments_all(net_segment, 1)  # 单线程
    single_thread_time = time.time() - start_time
    print(f"单线程执行时间: {single_thread_time:.6f} 秒")

    print("开始4线程测试...")
    start_time = time.time()
    ping_net_segments_all(net_segment, 4)  # 4线程
    four_thread_time = time.time() - start_time
    print(f"4线程执行时间: {four_thread_time:.6f} 秒")

    print("开始10线程测试...")
    start_time = time.time()
    ping_net_segments_all(net_segment, 10)  # 10线程
    ten_thread_time = time.time() - start_time
    print(f"10线程执行时间: {ten_thread_time:.6f} 秒")

    print("测试完成。")
