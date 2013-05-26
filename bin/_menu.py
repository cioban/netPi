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
from threading import Thread

from _lcd import PCD8544
from _keypad import keypad
from _system import get_ip, get_uptime, get_memused, cpu_usage
from _tcpdump import TCPDUMP, IPV4


class navigation_menu_thread(Thread):
    def __init__(self, function):
        Thread.__init__(self)
        self.function = function

    def run(self):
        self.function()

class navigation_menu:
    lcd = None
    pad = None
    asterisk_old = False
    start_hold_time = 0
    shutdown_time = 3

    menu_screens = [ 'init', 'system', 'analyzer_controller',
                'analyzer_l2_count', 'analyzer_ipv4_count' ]
    menu_pos = 0
    last_menu_pos = -1

    analyzer_running = False

    def __init__(self):
        self.lcd = PCD8544()
        self.pad = keypad()
        self.tcpdump = TCPDUMP(iface='eth0')


    def menu_pos_common(self):
        if self.menu_pos < 0:
            self.menu_pos = len(self.menu_screens) - 1
        if self.menu_pos >= len(self.menu_screens):
            self.menu_pos = 0
        self.lcd.cls()
        self.lcd.set_display_mode()

    def menu_pos_up(self):
        self.menu_pos = self.menu_pos + 1
        self.menu_pos_common()

    def menu_pos_down(self):
        self.menu_pos = self.menu_pos - 1
        self.menu_pos_common()

    def menu_init(self):
        if self.menu_pos != self.last_menu_pos:
            self.last_menu_pos = self.menu_pos
            self.lcd.centre_word(0,":netPi: ready")
            self.lcd.centre_word(2,"Use as teclas")
            ip = get_ip('eth0')
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
            self.lcd.centre_word(0, ":system info")

            self.lcd.gotoxy(0,2)
            self.lcd.text("CPU: %s%%" % cpu_usage())
            self.lcd.gotoxy(0,3)
            self.lcd.text("MEM: %s MB" % get_memused())
            self.lcd.gotoxy(0,4)
            self.lcd.text("UP: %s" % get_uptime())

        for key, value in self.pad.key_value.iteritems():
            if key == 'six' and value is True:
                self.menu_pos_up()
            elif key == 'four' and value is True:
                self.menu_pos_down()
            elif key == 'five' and value is True:
                self.last_menu_pos = -1

    def analyzer_thread_toggle(self):
        if self.analyzer_running is True:
            self.tcpdump.keep_running = False
            self.analyzer_running = False
        else:
            thread_tcpdump = navigation_menu_thread(self.tcpdump.main)
            thread_tcpdump.start()
            self.analyzer_running = True

    def menu_analyzer_controller(self):
        if self.menu_pos != self.last_menu_pos:
            self.last_menu_pos = self.menu_pos
            self.lcd.centre_word(0,":analyzer ctrl")
            self.lcd.gotoxy(0,2)
            if self.analyzer_running is True:
                self.lcd.text("Analyzer: RUN ")
            else:
                self.lcd.text("Analyzer: STOP")
            self.lcd.gotoxy(0,4)
            self.lcd.text("Use a tecla #")
            self.lcd.gotoxy(0,5)
            self.lcd.text("para controlar")


        for key, value in self.pad.key_value.iteritems():
            if key == 'six' and value is True:
                self.menu_pos_up()
            elif key == 'four' and value is True:
                self.menu_pos_down()
            elif key == 'five' and value is True:
                self.last_menu_pos = -1
            elif key == 'hash' and value is True:
                self.analyzer_thread_toggle()
                self.last_menu_pos = -1

    def menu_analyzer_l2_count(self):
        if self.menu_pos != self.last_menu_pos:
            self.last_menu_pos = self.menu_pos
            self.lcd.centre_word(0,": L2 counters")

            if self.tcpdump.ethernet_data['byte_counter'] > 1024:
                byte_str = str(int(self.tcpdump.ethernet_data['byte_counter'] / 1024))
            else:
                byte_str = str(0)

            self.lcd.gotoxy(0,1)
            self.lcd.text("PKT:%d" % self.tcpdump.ethernet_data['pkt_couter'])

            self.lcd.gotoxy(0,2)
            self.lcd.text("KB:%s" % byte_str)

            lcd_row = 3
            for ether, DATA in self.tcpdump.ethertypes.iteritems():
                if DATA[1] > 0 and DATA[0] != 'Unknown':
                    self.lcd.gotoxy(0,lcd_row)
                    self.lcd.text('%s: %d' % (DATA[0], DATA[1]))
                    lcd_row += 1
                    if lcd_row > 5:
                        break

        for key, value in self.pad.key_value.iteritems():
            if key == 'six' and value is True:
                self.menu_pos_up()
            elif key == 'four' and value is True:
                self.menu_pos_down()
            elif key == 'five' and value is True:
                self.last_menu_pos = -1

    def menu_analyzer_ipv4_count(self):
        if self.menu_pos != self.last_menu_pos:
            self.last_menu_pos = self.menu_pos
            self.lcd.centre_word(0,":ipv4 counters")

            if IPV4.ip_data['byte_counter'] > 1024:
                byte_str = str(int(IPV4.ip_data['byte_counter'] / 1024))
            else:
                byte_str = str(0)

            if IPV4.ip_data['payload_byte_counter'] > 1024:
                pl_byte_str = str(int(IPV4.ip_data['payload_byte_counter'] / 1024))
            else:
                pl_byte_str = str(0)

            self.lcd.gotoxy(0,1)
            self.lcd.text("KB:%s" % byte_str)

            self.lcd.gotoxy(0,2)
            self.lcd.text("P KB:%s" % pl_byte_str)

            lcd_row = 3
            for ether, DATA in IPV4.protocols.iteritems():
                if DATA[1] > 0 and DATA[0] != 'Unknown':
                    self.lcd.gotoxy(0,lcd_row)
                    self.lcd.text('%s: %d' % (DATA[0], DATA[1]))
                    lcd_row += 1
                    if lcd_row > 5:
                        break

        for key, value in self.pad.key_value.iteritems():
            if key == 'six' and value is True:
                self.menu_pos_up()
            elif key == 'four' and value is True:
                self.menu_pos_down()
            elif key == 'five' and value is True:
                self.last_menu_pos = -1

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
        self.tcpdump.keep_running = False
        self.lcd.cls()
        self.lcd.set_display_mode(invert=True)
        self.lcd.centre_word(1,"netPi")
        self.lcd.centre_word(3,"desligando")
        time.sleep(1)
        self.lcd.write_logo()
        sys.exit(0)

