# -*- coding: utf-8 -*-

import csv
import numpy as np
import matplotlib.pyplot as plt

with open("DCA_ZF3.3.txt") as tsv:
    reader = csv.reader(tsv, dialect="excel-tab")
    for i in range(6):
        next(reader)
    columns = list( zip(*[line for line in reader]) )

    U1 = np.array( columns[1][:48], dtype=float)
    I1 = np.array( columns[2][:48], dtype=float )

    U2 = np.array( columns[3], dtype=float )
    I2 = np.array( columns[4], dtype=float )

    plt.title("3V3 Zener Diode Forward Voltage")
    plt.plot(U1, I1, label="1")
    plt.plot(U2, I2, label="2")
    plt.xlabel('forward voltage / V')
    plt.ylabel('current / mA')
    plt.legend()
    plt.show()
