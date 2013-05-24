#!/usr/bin/env python2
# -*- encoding: utf-8 -*-
"""
Modulo: 
"""
__author__ = 'Sergio Cioban Filho'
__version__ = '1.0'
__date__ = '24/05/2013 11:25:20 AM'

import os
import sys
import time
import socket
import fcntl
import struct

from _lcd import PCD8544
from _keypad import keypad

def getIpAddress(ifname):
    try:
	    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	    return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915,
                struct.pack('256s', ifname[:15]))[20:24])
    except Exception:
        return ''


class navigation_menu:

    lcd = None
    pad = None
    asterisk_old = False
    start_hold_time = 0
    shutdown_time = 3

    menu_screens = ['init', 'system', ]
    menu_pos = 0
    last_menu_pos = -1

    def __init__(self):
        self.lcd = PCD8544()
        self.pad = keypad()

    def menu_pos_common(self):
        if self.menu_pos < 0:
            self.menu_pos = len(self.menu_screens) - 1
        if self.menu_pos >= len(self.menu_screens):
            self.menu_pos = 0
        self.lcd.cls()
        menu_function = eval('self.menu_'+self.menu_screens[self.menu_pos])
        menu_function()

    def menu_pos_up(self):
        self.menu_pos = self.menu_pos + 1
        self.menu_pos_common()

    def menu_pos_down(self):
        self.menu_pos = self.menu_pos - 1
        self.menu_pos_common()



    def menu_init(self):
        if self.menu_pos != self.last_menu_pos:
            self.last_menu_pos = self.menu_pos
            self.lcd.centre_word(0,"netPi")
            self.lcd.centre_word(1,": ready :")
            self.lcd.centre_word(3,"Use as teclas")
            ip = getIpAddress('eth0')
            self.lcd.centre_word(5,ip)

        for key, value in self.pad.key_value.iteritems():
            if key == 'asterisk':
                if self.asterisk_old != value:
                    self.asterisk_old = value
                    if value is True:
                        self.start_hold_time = time.time()

                if value is True and ((time.time() - self.start_hold_time) >= self.shutdown_time):
                    os.system('(sleep 1; shutdown -h now) &')
                    self.kill_handler(0, '')
            else:
                if value is True:
                    if key == 'six':
                        self.menu_pos_up()
                    elif key == 'four':
                        self.menu_pos_down()
                    else:
                        self.lcd.centre_word(4,'Tecla invalida')

    def menu_system(self):
        if self.menu_pos != self.last_menu_pos:
            self.last_menu_pos = self.menu_pos
            self.lcd.gotoxy(0,1)
            self.lcd.text(":netPi: system")
            self.lcd.gotoxy(0,2)
            self.lcd.text("CPU:")
            self.lcd.gotoxy(0,3)
            self.lcd.text("MEM:")
            self.lcd.gotoxy(0,4)
            self.lcd.text("UPTIME:")

        for key, value in self.pad.key_value.iteritems():
            if key == 'six' and value is True:
                self.menu_pos_up()
            elif key == 'four' and value is True:
                self.menu_pos_down()

    def loop(self):
        try:
            while 1==1:
                self.pad.read()
                menu_function = eval('self.menu_'+self.menu_screens[self.menu_pos])
                menu_function()
                time.sleep(0.2)

        except KeyboardInterrupt:
            self.kill_handler(0, '')


    def kill_handler(self, signum, frame):
        self.lcd.cls()
        self.lcd.set_display_mode(invert=True)
        self.lcd.centre_word(1,"netPi")
        self.lcd.centre_word(3,"desligando")
        time.sleep(1)
        self.lcd.write_logo()
        sys.exit(0)

