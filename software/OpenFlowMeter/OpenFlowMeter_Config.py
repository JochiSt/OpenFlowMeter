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

        self.interval_CAN_ADC = 0
        self.interval_PRINT_UART = 0
        self.interval_I2C_TMP100 = 0
        self.interval_I2C_BME680 = 255

        self.PID_flags  = 0

        self.PID_T = [40   , 40  ]
        self.PID_P = [0.9  , 0.9 ]
        self.PID_I = [0.06 , 0.06]
        self.PID_D = [0.0  , 0.0 ]

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
        print("PID 0")
        print("\tT: %f"%(self.PID_T[0]))
        print("\tP: %f"%(self.PID_P[0]))
        print("\tI: %f"%(self.PID_I[0]))
        print("\tD: %f"%(self.PID_D[0]))

        print()
        print("PID 1")
        print("\tT: %f"%(self.PID_T[1]))
        print("\tP: %f"%(self.PID_P[1]))
        print("\tI: %f"%(self.PID_I[1]))
        print("\tD: %f"%(self.PID_D[1]))

        print()
        print("Smooting:")
        print("\tSMOO     %d"%(self.SMOO))
        print("\tSMOO_MAX %d"%(self.SMOO_MAX))


    def toBytes(self):
        """
        convert the configuration into bytes, which can be used to transfer the
        configuration to the OpenFlowMeter

        Returns
        -------
        all bytes beloging to the configuration.

        """

        PIDs = np.array([
            self.PID_T[0], self.PID_P[0], self.PID_I[0], self.PID_D[0],
            self.PID_T[1], self.PID_P[1], self.PID_I[1], self.PID_D[1]
            ], dtype=np.float16)


        ret = bytearray([
            self.boardID,               # 0
            self.interval_CAN_ADC,      # 1
            self.interval_PRINT_UART,   # 2
            self.interval_I2C_TMP100,   # 3
            self.interval_I2C_BME680,   # 4
            self.PID_flags              # 5
            ])

        ret += bytearray(PIDs.tobytes())

        ret += bytearray([
            self.SMOO,
            self.SMOO_MAX
            ])

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
        self.PID_flags           = bytesin[5]

        self.PID_T[0] = np.frombuffer(bytesin[ 6: 8], dtype=np.float16)[0]
        self.PID_P[0] = np.frombuffer(bytesin[ 8:10], dtype=np.float16)[0]
        self.PID_I[0] = np.frombuffer(bytesin[10:12], dtype=np.float16)[0]
        self.PID_D[0] = np.frombuffer(bytesin[12:14], dtype=np.float16)[0]
        self.PID_T[1] = np.frombuffer(bytesin[14:16], dtype=np.float16)[0]
        self.PID_P[1] = np.frombuffer(bytesin[16:18], dtype=np.float16)[0]
        self.PID_I[1] = np.frombuffer(bytesin[18:20], dtype=np.float16)[0]
        self.PID_D[1] = np.frombuffer(bytesin[20:22], dtype=np.float16)[0]

        self.SMOO                = bytesin[22]
        self.SMOO_MAX            = bytesin[23]


if __name__ == "__main__":
    OFMcfg = OpenFlowMeter_Config()
    cfgbytes = OFMcfg.toBytes()

    for byte in cfgbytes:
        print("%X"%(byte), end=" ", flush=True)
    print()

    print("length of configuration %d"%(len(cfgbytes)) )
    print()

    OFMcfg.printout()