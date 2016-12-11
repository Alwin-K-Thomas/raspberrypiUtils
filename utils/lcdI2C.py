#!/usr/bin/python
#--------------------------------------
# LCD test script using I2C backpack.
# Author : Matt Hawkins
# Supports : 16x2 and 20x4 screens.
# Modified : Varadarajan A G
# -------------------------------------

import smbus
import time
import fcntl
import struct

class LCD_I2C(object):
    """
	Module to display LCD values
    """
    I2C_ADDR  = 0x27
    LCD_WIDTH = 16
    LCD_CHR = 1
    LCD_CMD = 0
    LCD_LINE_1 = 0x80
    LCD_LINE_2 = 0xC0
    LCD_LINE_3 = 0x94
    LCD_LINE_4 = 0xD4
    LCD_BACKLIGHT  = 0x08
    #LCD_BACKLIGHT = 0x00
    ENABLE = 0b00000100
    E_PULSE = 0.0005
    E_DELAY = 0.0005
    bus = smbus.SMBus(1) # Rev 2 Pi uses 1

    @classmethod
    def lcd_init(cls):
    # Initialise display
        cls.lcd_byte(0x33,cls.LCD_CMD)
        cls.lcd_byte(0x32,cls.LCD_CMD)
        cls.lcd_byte(0x06,cls.LCD_CMD)
        cls.lcd_byte(0x0C,cls.LCD_CMD)
        cls.lcd_byte(0x28,cls.LCD_CMD)
        cls.lcd_byte(0x01,cls.LCD_CMD)
        time.sleep(cls.E_DELAY)
    
    @classmethod
    def lcd_byte(cls, bits, mode):
        bits_high = mode | (bits & 0xF0) | cls.LCD_BACKLIGHT
        bits_low = mode | ((bits<<4) & 0xF0) | cls.LCD_BACKLIGHT
        cls.bus.write_byte(cls.I2C_ADDR, bits_high)
        cls.lcd_toggle_enable(bits_high)
        cls.bus.write_byte(cls.I2C_ADDR, bits_low)
        cls.lcd_toggle_enable(bits_low)
    
    @classmethod
    def lcd_toggle_enable(cls, bits):
        time.sleep(cls.E_DELAY)
        cls.bus.write_byte(cls.I2C_ADDR, (bits | cls.ENABLE))
        time.sleep(cls.E_PULSE)
        cls.bus.write_byte(cls.I2C_ADDR,(bits & ~cls.ENABLE))
        time.sleep(cls.E_DELAY)
    
    @classmethod
    def lcd_string(cls, message,line):
        message = message.ljust(cls.LCD_WIDTH," ")
        cls.lcd_byte(line, cls.LCD_CMD)
        for i in range(cls.LCD_WIDTH):
            cls.lcd_byte(ord(message[i]),cls.LCD_CHR)
            
    @classmethod
    def main(cls, msg_1 = None, msg_2 = None):
        cls.lcd_init()
        if msg_1:
           cls.lcd_string("{0} <".format(msg_1),cls.LCD_LINE_1)
       
        if msg_2:
           cls.lcd_string("{0} <".format(msg_2),cls.LCD_LINE_2)

        time.sleep(3)
            
if __name__ == '__main__':
  try:
    LCD_I2C.main('Hi Varad.')
  except KeyboardInterrupt:
    pass
  #finally:
  #  lcd_byte(0x01, LCD_CMD)

