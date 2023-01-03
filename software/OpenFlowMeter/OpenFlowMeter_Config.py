# -*- coding: utf-8 -*-

import numpy as np

class OpenFlowMeter_Config(object):
    """
    based on config.h (2022-12-20)
    uint8_t board_ID;             ///< Board ID
    uint8_t interval_CAN_ADC;       ///< interval, the data is reported to CAN
    uint8_t interval_PRINT_UART;    ///< interval, the data is printed on UART

    uint8_t interval_I2C_TMP100;    ///< interval, the TMP100 should be read
    uint8_t interval_I2C_BME680;    ///< internal, the BME680 should be read

    union{
        struct {
            uint8_t PID0_active : 1;  ///< is PID channel 0 active
            uint8_t PID1_active : 1;  ///< is PID channel 1 active
            uint8_t spare : 6;
        };
        uint8_t raw;
    } PID_flags;

    PID_config_t PID0; ///< configuration of PID channel 0
    PID_config_t PID1; ///< configuration of PID channel 1

    uint8_t SMOO;     ///< smoothing value
    uint8_t SMOO_MAX; ///< maximal smoothing

    typedef struct {
    float PID_T;  ///< temperature setpoint
    float PID_P;  ///< proportional part
    float PID_I;  ///< integral part
    float PID_D;  ///< differential part
    } PID_config_t;

    """

    def __init__(self):
        """
        """
        self.boardID = 1

        self.interval_CAN_ADC = 255
        self.interval_PRINT_UART = 255
        self.interval_I2C_TMP100 = 255
        self.interval_I2C_BME680 = 255

        self.PID_flags  = 0
        self.PID_active = [ False, False ]

        self.PID_T = [0.0 , 0.0]
        self.PID_P = [0.0 , 0.0]
        self.PID_I = [0.0 , 0.0]
        self.PID_D = [0.0 , 0.0]

        self.Ugain = [0.0 , 0.0]
        self.Igain = [0.0 , 0.0]

        self.SMOO = 15
        self.SMOO_MAX = 16

    def printout(self):
        print("Board ID: %d"%(self.boardID))
        print("Intervals:")
        print("\tCAN ADC    %d"%(self.interval_CAN_ADC))
        print("\tPrint UART %d"%(self.interval_PRINT_UART))
        print("\t\tI2C TMP100 %d"%(self.interval_I2C_TMP100))
        print("\t\tI2C BME680 %d"%(self.interval_I2C_BME680))
        print()
        print("PIDflags 0x%X"%(self.PID_flags))
        print("PID 0\t", end="")
        if self.PID_active[1]:
            print("active")
        else:
            print("deactivated")
        print("\tT: %f"%(self.PID_T[0]))
        print("\tP: %f"%(self.PID_P[0]))
        print("\tI: %f"%(self.PID_I[0]))
        print("\tD: %f"%(self.PID_D[0]))

        print()
        print("PID 1\t", end="")
        if self.PID_active[1]:
            print("active")
        else:
            print("deactivated")
        print("\tT: %f"%(self.PID_T[1]))
        print("\tP: %f"%(self.PID_P[1]))
        print("\tI: %f"%(self.PID_I[1]))
        print("\tD: %f"%(self.PID_D[1]))

        print()
        print("Smoothing:")
        print("\tSMOO     %d"%(self.SMOO))
        print("\tSMOO_MAX %d"%(self.SMOO_MAX))

        print()
        print("Amplification:")
        print("\tU0: %f"%(self.Ugain[0]))
        print("\tI0: %f"%(self.Igain[0]))
        print("\tU1: %f"%(self.Ugain[1]))
        print("\tI1: %f"%(self.Igain[1]))

    def toBytes(self):
        """
        convert the configuration into bytes, which can be used to transfer the
        configuration to the OpenFlowMeter

        Returns
        -------
        all bytes beloging to the configuration.

        """

        self.PID_flags = self.PID_active[1] << 1 | self.PID_active[0]

        PIDs = np.array([
            self.PID_T[0], self.PID_P[0], self.PID_I[0], self.PID_D[0],
            self.PID_T[1], self.PID_P[1], self.PID_I[1], self.PID_D[1]
            ], dtype=np.float32)

        GAINs = np.array([
            self.Ugain[0], self.Igain[0], self.Ugain[1], self.Igain[1]
            ], dtype=np.float32)

        ret = bytearray([
            self.boardID,               # 0
            self.interval_CAN_ADC,      # 1
            self.interval_PRINT_UART,   # 2
            self.interval_I2C_TMP100,   # 3

            self.interval_I2C_BME680,   # 4
            ])
        ret += bytearray([
            self.SMOO,                  # 5
            self.SMOO_MAX               # 6
            ])

        ret += bytearray([
            self.PID_flags              # 7
            ])

        ret += bytearray(PIDs.tobytes())

        ret += bytearray(GAINs.tobytes())

        return ret

    def fromBytes(self, bytesin=[]):
        """
        construct the configuration from the bytes
        Parameters
        ----------
        bytesin : TYPE, optional
            DESCRIPTION. The default is [].

        Returns
        -------
        None.

        """
        self.boardID             = bytesin[0]
        self.interval_CAN_ADC    = bytesin[1]
        self.interval_PRINT_UART = bytesin[2]
        self.interval_I2C_TMP100 = bytesin[3]

        self.interval_I2C_BME680 = bytesin[4]
        self.SMOO                = bytesin[5]
        self.SMOO_MAX            = bytesin[6]
        self.PID_flags           = bytesin[7]

        nfloat = 12
        floatstart = 8
        floats = np.frombuffer(bytesin[ floatstart :  floatstart + nfloat*4], dtype=np.float32)

        self.PID_active = [ bool((self.PID_flags & 0x1)),
                            bool((self.PID_flags & 0x2) >> 1) ]

        self.PID_T[0] = floats[ 0]
        self.PID_P[0] = floats[ 1]
        self.PID_I[0] = floats[ 2]
        self.PID_D[0] = floats[ 3]
        self.PID_T[1] = floats[ 4]
        self.PID_P[1] = floats[ 5]
        self.PID_I[1] = floats[ 6]
        self.PID_D[1] = floats[ 7]

        self.Ugain[0] = floats[ 8]
        self.Igain[0] = floats[ 9]
        self.Ugain[1] = floats[10]
        self.Igain[0] = floats[11]

if __name__ == "__main__":
    OFMcfg = OpenFlowMeter_Config()
    cfgbytes = OFMcfg.toBytes()

    for byte in cfgbytes:
        print("%X"%(byte), end=" ", flush=True)
    print()

    print("length of configuration %d"%(len(cfgbytes)) )
    print()

    OFMcfg.printout()

    OFMcfg.fromBytes(cfgbytes)

    OFMcfg.printout()

    print()
    print()
    for i, byte in enumerate(OFMcfg.toBytes()):
        print(i, byte)
