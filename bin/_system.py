#!/usr/bin/env python2
# -*- encoding: utf-8 -*-
"""
Modulo: 
"""
__author__ = 'Sergio Cioban Filho'
__version__ = '1.0'
__date__ = '24/05/2013 04:13:02 PM'

import socket
import fcntl
import struct
from datetime import timedelta
import re
import time

class cpu_usage:
   def __init__(self, interval=0.3, percentage=True):
       self.interval=interval
       self.percentage=percentage
       self.result=self.compute()

   def get_time(self):
       stat_file=file("/proc/stat", "r")
       time_list=stat_file.readline().split(" ")[2:6]
       stat_file.close()
       for i in range(len(time_list))  :
           time_list[i]=int(time_list[i])
       return time_list

   def delta_time(self):
       x=self.get_time()
       time.sleep(self.interval)
       y=self.get_time()
       for i in range(len(x)):
           y[i]-=x[i]
       return y

   def compute(self):
       t=self.delta_time()
       if self.percentage:
           result=100-(t[len(t)-1]*100.00/sum(t))
       else:
           result=sum(t)
       return result

   def __repr__(self):
       return str(round(self.result, 1))


def get_meminfo():
    re_parser = re.compile(r'^(?P<key>\S*):\s*(?P<value>\d*)\s*kB')
    result = dict()
    for line in open('/proc/meminfo'):
        match = re_parser.match(line)
        if not match:
            continue # skip lines that don't parse
        key, value = match.groups(['key', 'value'])
        result[key] = int(value)
    return result

def get_memused():
    meminfo = get_meminfo()
    memused = (meminfo['MemTotal'] -  meminfo['MemFree']) / 1024
    return str(memused)

def get_uptime():
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])
        uptime_string = str(timedelta(seconds = uptime_seconds)).split('.')[0]

    return uptime_string

def get_ip(ifname):
    try:
	    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	    return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915,
                struct.pack('256s', ifname[:15]))[20:24])
    except Exception:
        return ''

if __name__ == '__main__':
    print get_uptime()
    print 'eth0:', get_ip('eth0')
    print get_meminfo()
    print get_memused()
    print cpu_usage()
