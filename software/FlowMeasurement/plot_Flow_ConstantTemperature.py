# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import os

def plot_Flow_ConstantTemperature(filename):
    npzfile = np.load(filename)

    log_dac=npzfile['log_dac'][2:]
    log_time=npzfile['log_time'][2:]
    log_T=npzfile['log_T'][2:]
    log_current=npzfile['log_current'][2:]
    log_voltage=npzfile['log_voltage'][2:]
    pid_params = npzfile['pid_params']

    fig, ax1 = plt.subplots()
    ax1.set_title("PID test P%3.1f I%3.1f D%3.1f"%(pid_params[0], pid_params[1], pid_params[2]) )
    color = 'tab:red'
    ax1.set_xlabel("measurement time / s")
    ax1.set_ylabel("OFM current / LSB", color=color)
    ax1.plot( log_time, log_current, color=color, label="current")
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    color = 'tab:blue'
    ax2.set_ylabel('OFM voltage / LSB', color=color)  # we already handled the x-label with ax1
    ax2.plot( log_time, log_voltage, color=color, label="voltage")
    ax2.tick_params(axis='y', labelcolor=color)

    ax3 = ax1.twinx()
    color = 'tab:green'
    ax3.spines['right'].set_position(('outward', 60))
    ax3.set_ylabel('OFM temperature / °C', color=color)
    ax3.plot( log_time, log_T, color=color, label="temperature")
    ax3.tick_params(axis='y', labelcolor=color)
    ax3.hlines(40, 0, np.max(log_time), color=color, linestyle="--")

    ax4 = ax1.twinx()
    color = 'tab:orange'
    ax4.spines['right'].set_position(('outward', 120))
    ax4.set_ylabel('OFM dac / LSB', color=color)  # we already handled the x-label with ax1
    ax4.plot( log_time, log_dac, color=color, label="DAC")
    ax4.tick_params(axis='y', labelcolor=color)
    ax4.set_ylim([100,600])

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.savefig(os.path.splitext(filename)[0]+".png")
    plt.show()

if __name__ == "__main__":
    with os.scandir(".") as it:
        for entry in it:
            if entry.name.endswith(".npz") and entry.is_file():
                plot_Flow_ConstantTemperature(entry.name)