#!/usr/bin/env python2
# -*- encoding: utf-8 -*-
"""
Modulo: 
"""
__author__ = 'Sergio Cioban Filho'
__version__ = '1.0'
__date__ = '24/05/2013 09:01:45 AM'

import time
import signal

from _lcd import PCD8544
from _menu import navigation_menu

if __name__ == "__main__":
    while 1==1:
        try:
            lcd = None
            menu = navigation_menu()
            signal.signal(signal.SIGTERM, menu.kill_handler)

            lcd = PCD8544()

            menu.loop()

        except KeyboardInterrupt:
            menu.kill_handler(0, '')

        except Exception, e:
            if lcd is not None:
                lcd.cls()
                lcd.centre_word(0,"ERROR!!!")
                lcd.gotoxy(0,1)
                lcd.text(str(e))

        time.sleep(5)
