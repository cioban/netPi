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
import psutil

def cpu_usage():
    return str(psutil.cpu_percent())


def get_memused():
    mem = psutil.virtual_memory()
    return str((mem.used / 1024) / 1024)

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

def get_temp():
    temp = int(open('/sys/class/thermal/thermal_zone0/temp').read()) / 1e3

    return str(round(temp, 2))

if __name__ == '__main__':
    print get_uptime()
    print 'eth0:', get_ip('eth0')
    print get_memused()
    print cpu_usage()
    print get_temp()

