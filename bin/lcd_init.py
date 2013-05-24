#!/usr/bin/env python2
# -*- encoding: utf-8 -*-
"""
Modulo: 
"""
__author__ = 'Sergio Cioban Filho'
__version__ = '1.0'
__date__ = '24/05/2013 09:46:44 AM'

from _lcd import PCD8544


lcd = PCD8544()
lcd.blink_logo(10)
