# -*- coding: utf-8 -*-
"""

"""

import numpy as np

def SimADC(Uin = 0, Uref = 3.3):
    LSBs = Uin / Uref * 4096
    return np.round(LSBs).astype(int)