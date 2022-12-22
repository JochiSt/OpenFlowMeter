# -*- coding: utf-8 -*-
import numpy as np

f = np.frombuffer(b'\x00\x3c', dtype=np.float16)[0]
print(f)

array = np.array([1.0], dtype=np.float16)
print("%X %X"%(array.tobytes()[0], array.tobytes()[1]))


