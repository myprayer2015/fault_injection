#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import _thread
import threading
import time
import sys
import logging
import requests


def exhaust_cpu(times=10000000):
    count = 1
    num = 1
    while count < times:
        num = num * 2
        count = count + 1
        if num >= sys.maxsize/2:
            num = 1

'''
if __name__ == '__main__':
    try:
        threads = []
        for i in range(0, 5):
            thread = threading.Thread(target=exhaust_cpu, args=(10000000,))
            threads.append(thread)
        for t in threads:
            t.start()
        for t in threads:
            t.join()
    except Exception as e:
        logging.exception(e)



env_dist = os.environ
cpu_num = 4
cpu_time = 100
if env_dist.get('CPU_NUM'):
    cpu_num = env_dist.get('CPU_NUM')
if env_dist.get('CPU_TIME'):
    cpu_time = env_dist.get('CPU_TIME')
os.system("stress -c %s -t %s" %(cpu_num, cpu_time))'''

#按照不同模式增长,1线性，2指数
def cal(num, dif, mode):
    num = int(num)
    if int(mode) == 1:
        num = num + dif
    elif int(mode) == 2:
        num = num * 2
    return str(num)

def fault_injection():
    env_dist = os.environ
    #fault_list = {'cpu' : 1, 'mem' : 2, 'disk' : 3, 'net' : 4}
    fault_type = env_dist.get('FAULT_TYPE') or 'cpu'
    #cpu : FAULT_TYPE、CPU_NUM、MODE
    #mem : FAULT_TYPE、THREAD_NUM、MEM_SIZE、MODE
    #disk : FAULT_TYPE、IO_TIMES、MODE
    #net : FAULT_TYPE、NET_PORT、MODE
    if fault_type == 'cpu':
        cpu_num = env_dist.get('CPU_NUM') or '1'
        cpu_num_new = env_dist.get('CPU_NUM_NEW') or '0'
        mode = env_dist.get('MODE') or '1'
        if cpu_num_new == '0':
            os.popen("stress -c %s -t 300" %(cpu_num))
            cpu_num_new = cal(cpu_num, 1, mode)
        else:
            os.popen("stress -c %s -t 300" %(str(int(cpu_num_new)-int(cpu_num))))
            cpu_num = cpu_num_new
            cpu_num_new = cal(cpu_num, 1, mode)
        os.popen("export CPU_NUM=%s" %(cpu_num))
        os.popen("export CPU_NUM_NEW=%s" %(cpu_num_new))
    elif fault_type == 'mem':
        thread_num = env_dist.get('THREAD_NUM') or '1'
        thread_num_new = env_dist.get('THREAD_NUM_NEW') or '0'
        mem_size = env_dist.get('MEM_SIZE') or '5M'
        mode = env_dist('MODE') or '1'
        if thread_num_new == '0':
            os.popen("stress --vm %s --vm-bytes %s --vm-keep -t 180" %(thread_num, mem_size))
            thread_num_new = cal(thread_num, 1, mode)
        else:
            os.popen("stress --vm %s --vm-bytes %s --vm-keep  -t 180" %(str(int(thread_num_new)-int(thread_num)), mem_size))
            thread_num = thread_num_new
            thread_num_new = cal(thread_num, 1, mode)
        os.popen("export THREAD_NUM=%s" %(thread_num))
        os.popen("export THREAD_NUM_NEW=%s" %(thread_num_new))
    #iostat -x -k -d 1
    elif fault_type == 'disk':
        io_times = env_dist.get("IO_TIMES") or '1'
        io_times_new = env_dist.get("IO_TIMES_NEW") or '0'
        mode = env_dist('MODE') or '1'
        if io_times_new == '0':
            os.popen("stress -i %s -t 300" %(io_times))
            io_times_new = cal(io_times, 1, mode)
        else:
            os.popen("stress -i %s -t 300" %(str(int(io_times_new)-int(io_times))))
            io_times = io_times_new
            io_times_new = cal(io_times, 1, mode)
        os.popen("export IO_TIMES=%s" %(io_times))
        os.popen("export IO_TIMES_NEW=%s" %(io_times_new))
    elif fault_type == 'net':
        net_port = env_dist.get('NET_PORT')
        if not env_dist.get('NET_FLAG'):
            os.popen("iperf3 -s -p %s" %(net_port))
        os.popen("export NET_FLAG=1")
    return fault_type+' error injection success!'