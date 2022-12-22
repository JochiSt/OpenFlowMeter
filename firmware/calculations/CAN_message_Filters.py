# -*- coding: utf-8 -*-
"""
    Test the message filters for the STM32 CAN
    based on https://community.st.com/s/question/0D50X00009XkfSlSAJ/can-filters
    translated to Python and adapted
"""

BOARD_ID = 3

COMP = 0x000 | (BOARD_ID << 4)
MASK = 0xFF0

for id in range(0x800):
    if ( (id & MASK) == COMP):
        print("%03X"%(id))
