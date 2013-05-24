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

from _lcd import PCD8544
from _keypad import keypad

class navigation_menu:

    lcd = None
    pad = None
    asterisk_old = False
    start_hold_time = 0
    shutdown_time = 3

    def __init__(self):
        self.lcd = PCD8544()
        self.pad = keypad()

    def loop(self):
        while 1==1:
            self.pad.read()
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
                        self.lcd.centre_word(4,"             ")
                        self.lcd.centre_word(4,key)
            time.sleep(0.2)

    def kill_handler(self, signum, frame):
        self.lcd.cls()
        self.lcd.set_display_mode(invert=True)
        self.lcd.centre_word(1,"netPi")
        self.lcd.centre_word(3,"desligando")
        time.sleep(1)
        self.lcd.write_logo()
        sys.exit(0)


#if __name__ == '__main__':
