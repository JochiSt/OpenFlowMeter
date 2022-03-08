// clang-format off
/*******************************************************************************

   File - CO_OD.c/CO_OD.h
   CANopen Object Dictionary.

   This file was automatically generated with libedssharp Object
   Dictionary Editor v0.8-0-gb60f4eb   DON'T EDIT THIS FILE MANUALLY !!!!
*******************************************************************************/


#ifndef CO_OD_H_
#define CO_OD_H_

/*******************************************************************************
   CANopen DATA TYPES
*******************************************************************************/
   typedef bool_t       BOOLEAN;
   typedef uint8_t      UNSIGNED8;
   typedef uint16_t     UNSIGNED16;
   typedef uint32_t     UNSIGNED32;
   typedef uint64_t     UNSIGNED64;
   typedef int8_t       INTEGER8;
   typedef int16_t      INTEGER16;
   typedef int32_t      INTEGER32;
   typedef int64_t      INTEGER64;
   typedef float32_t    REAL32;
   typedef float64_t    REAL64;
   typedef char_t       VISIBLE_STRING;
   typedef oChar_t      OCTET_STRING;

   #ifdef DOMAIN
   #undef DOMAIN
   #endif

   typedef domain_t     DOMAIN;

#ifndef timeOfDay_t
    typedef union {
        unsigned long long ullValue;
        struct {
            unsigned long ms:28;
            unsigned reserved:4;
            unsigned days:16;
            unsigned reserved2:16;
        };
    }timeOfDay_t;
#endif

    typedef timeOfDay_t TIME_OF_DAY;
    typedef timeOfDay_t TIME_DIFFERENCE;


/*******************************************************************************
   FILE INFO:
      FileName:     
      FileVersion:  1
      CreationTime: 
      CreationDate: 
      CreatedBy:    JochiSt
******************************************************************************/


/*******************************************************************************
   DEVICE INFO:
      VendorName:     
      VendorNumber    0
      ProductName:    OpenFlowMeter
      ProductNumber:  0
******************************************************************************/


/*******************************************************************************
   FEATURES
*******************************************************************************/
  #define CO_NO_SYNC                     1   //Associated objects: 1005-1007
  #define CO_NO_EMERGENCY                1   //Associated objects: 1014, 1015
  #define CO_NO_TS                       1   //Associated objects: 1012, 1013
  #define CO_NO_SDO_SERVER               1   //Associated objects: 1200-127F
  #define CO_NO_SDO_CLIENT               1   //Associated objects: 1280-12FF
  #define CO_NO_LSS_SERVER               0   //LSS Slave
  #define CO_NO_LSS_CLIENT               0   //LSS Master
  #define CO_NO_RPDO                     2   //Associated objects: 14xx, 16xx
  #define CO_NO_TPDO                     2   //Associated objects: 18xx, 1Axx
  #define CO_NO_NMT_MASTER               0


/*******************************************************************************
   OBJECT DICTIONARY
*******************************************************************************/
   #define CO_OD_NoOfElements             37


/*******************************************************************************
   TYPE DEFINITIONS FOR RECORDS
*******************************************************************************/
/*1018    */ typedef struct {
               UNSIGNED8      maxSubIndex;
               UNSIGNED32     vendorID;
               UNSIGNED32     productCode;
               UNSIGNED32     revisionNumber;
               UNSIGNED32     serialNumber;
               }              OD_identity_t;
/*1200    */ typedef struct {
               UNSIGNED8      maxSubIndex;
               UNSIGNED32     COB_IDClientToServer;
               UNSIGNED32     COB_IDServerToClient;
               }              OD_SDOServerParameter_t;
/*1280    */ typedef struct {
               UNSIGNED8      maxSubIndex;
               UNSIGNED32     COB_IDClientToServer;
               UNSIGNED32     COB_IDServerToClient;
               UNSIGNED8      nodeIDOfTheSDOServer;
               }              OD_SDOClientParameter_t;
/*1400    */ typedef struct {
               UNSIGNED8      maxSubIndex;
               UNSIGNED32     COB_IDUsedByRPDO;
               UNSIGNED8      transmissionType;
               }              OD_RPDOCommunicationParameter_t;
/*1600    */ typedef struct {
               UNSIGNED8      numberOfMappedObjects;
               UNSIGNED32     mappedObject1;
               UNSIGNED32     mappedObject2;
               UNSIGNED32     mappedObject3;
               UNSIGNED32     mappedObject4;
               UNSIGNED32     mappedObject5;
               UNSIGNED32     mappedObject6;
               UNSIGNED32     mappedObject7;
               UNSIGNED32     mappedObject8;
               }              OD_RPDOMappingParameter_t;
/*1800    */ typedef struct {
               UNSIGNED8      maxSubIndex;
               UNSIGNED32     COB_IDUsedByTPDO;
               UNSIGNED8      transmissionType;
               UNSIGNED16     inhibitTime;
               UNSIGNED8      compatibilityEntry;
               UNSIGNED16     eventTimer;
               UNSIGNED8      SYNCStartValue;
               }              OD_TPDOCommunicationParameter_t;
/*1a00    */ typedef struct {
               UNSIGNED8      numberOfMappedObjects;
               UNSIGNED32     mappedObject1;
               UNSIGNED32     mappedObject2;
               UNSIGNED32     mappedObject3;
               UNSIGNED32     mappedObject4;
               UNSIGNED32     mappedObject5;
               UNSIGNED32     mappedObject6;
               UNSIGNED32     mappedObject7;
               UNSIGNED32     mappedObject8;
               }              OD_TPDOMappingParameter_t;

/*******************************************************************************
   TYPE DEFINITIONS FOR OBJECT DICTIONARY INDEXES

   some of those are redundant with CO_SDO.h CO_ObjDicId_t <Common CiA301 object 
   dictionary entries>
*******************************************************************************/
/*1000 */
        #define OD_1000_deviceType                                  0x1000

/*1001 */
        #define OD_1001_errorRegister                               0x1001

/*1002 */
        #define OD_1002_manufacturerStatusRegister                  0x1002

/*1003 */
        #define OD_1003_preDefinedErrorField                        0x1003

        #define OD_1003_0_preDefinedErrorField_maxSubIndex          0
        #define OD_1003_1_preDefinedErrorField_standardErrorField   1
        #define OD_1003_2_preDefinedErrorField_standardErrorField   2
        #define OD_1003_3_preDefinedErrorField_standardErrorField   3
        #define OD_1003_4_preDefinedErrorField_standardErrorField   4
        #define OD_1003_5_preDefinedErrorField_standardErrorField   5
        #define OD_1003_6_preDefinedErrorField_standardErrorField   6
        #define OD_1003_7_preDefinedErrorField_standardErrorField   7
        #define OD_1003_8_preDefinedErrorField_standardErrorField   8

/*1005 */
        #define OD_1005_COB_ID_SYNCMessage                          0x1005

/*1006 */
        #define OD_1006_communicationCyclePeriod                    0x1006

/*1007 */
        #define OD_1007_synchronousWindowLength                     0x1007

/*1008 */
        #define OD_1008_manufacturerDeviceName                      0x1008

/*1009 */
        #define OD_1009_manufacturerHardwareVersion                 0x1009

/*100a */
        #define OD_100a_manufacturerSoftwareVersion                 0x100a

/*100c */
        #define OD_100c_guardTime                                   0x100c

/*100d */
        #define OD_100d_lifeTimeFactor                              0x100d

/*1010 */
        #define OD_1010_storeParameters                             0x1010

        #define OD_1010_0_storeParameters_maxSubIndex               0
        #define OD_1010_1_storeParameters_saveAllParameters         1

/*1011 */
        #define OD_1011_restoreDefaultParameters                    0x1011

        #define OD_1011_0_restoreDefaultParameters_maxSubIndex      0
        #define OD_1011_1_restoreDefaultParameters_restoreAllDefaultParameters 1

/*1012 */
        #define OD_1012_COB_ID_TIME                                 0x1012

/*1013 */
        #define OD_1013_highResolutionTimeStamp                     0x1013

/*1014 */
        #define OD_1014_COB_ID_EMCY                                 0x1014

/*1015 */
        #define OD_1015_inhibitTimeEMCY                             0x1015

/*1016 */
        #define OD_1016_consumerHeartbeatTime                       0x1016

        #define OD_1016_0_consumerHeartbeatTime_maxSubIndex         0
        #define OD_1016_1_consumerHeartbeatTime_consumerHeartbeatTime 1
        #define OD_1016_2_consumerHeartbeatTime_consumerHeartbeatTime 2
        #define OD_1016_3_consumerHeartbeatTime_consumerHeartbeatTime 3
        #define OD_1016_4_consumerHeartbeatTime_consumerHeartbeatTime 4

/*1017 */
        #define OD_1017_producerHeartbeatTime                       0x1017

/*1018 */
        #define OD_1018_identity                                    0x1018

        #define OD_1018_0_identity_maxSubIndex                      0
        #define OD_1018_1_identity_vendorID                         1
        #define OD_1018_2_identity_productCode                      2
        #define OD_1018_3_identity_revisionNumber                   3
        #define OD_1018_4_identity_serialNumber                     4

/*1019 */
        #define OD_1019_synchronousCounterOverflowValue             0x1019

/*1029 */
        #define OD_1029_errorBehavior                               0x1029

        #define OD_1029_0_errorBehavior_maxSubIndex                 0
        #define OD_1029_1_errorBehavior_communication               1
        #define OD_1029_2_errorBehavior_communicationOther          2
        #define OD_1029_3_errorBehavior_communicationPassive        3
        #define OD_1029_4_errorBehavior_generic                     4
        #define OD_1029_5_errorBehavior_deviceProfile               5
        #define OD_1029_6_errorBehavior_manufacturerSpecific        6

/*1200 */
        #define OD_1200_SDOServerParameter                          0x1200

        #define OD_1200_0_SDOServerParameter_maxSubIndex            0
        #define OD_1200_1_SDOServerParameter_COB_IDClientToServer   1
        #define OD_1200_2_SDOServerParameter_COB_IDServerToClient   2

/*1280 */
        #define OD_1280_SDOClientParameter                          0x1280

        #define OD_1280_0_SDOClientParameter_maxSubIndex            0
        #define OD_1280_1_SDOClientParameter_COB_IDClientToServer   1
        #define OD_1280_2_SDOClientParameter_COB_IDServerToClient   2
        #define OD_1280_3_SDOClientParameter_nodeIDOfTheSDOServer   3

/*1400 */
        #define OD_1400_RPDOCommunicationParameter                  0x1400

        #define OD_1400_0_RPDOCommunicationParameter_maxSubIndex    0
        #define OD_1400_1_RPDOCommunicationParameter_COB_IDUsedByRPDO 1
        #define OD_1400_2_RPDOCommunicationParameter_transmissionType 2

/*1401 */
        #define OD_1401_RPDOCommunicationParameter                  0x1401

        #define OD_1401_0_RPDOCommunicationParameter_maxSubIndex    0
        #define OD_1401_1_RPDOCommunicationParameter_COB_IDUsedByRPDO 1
        #define OD_1401_2_RPDOCommunicationParameter_transmissionType 2

/*1600 */
        #define OD_1600_RPDOMappingParameter                        0x1600

        #define OD_1600_0_RPDOMappingParameter_maxSubIndex          0
        #define OD_1600_1_RPDOMappingParameter_mappedObject1        1
        #define OD_1600_2_RPDOMappingParameter_mappedObject2        2
        #define OD_1600_3_RPDOMappingParameter_mappedObject3        3
        #define OD_1600_4_RPDOMappingParameter_mappedObject4        4
        #define OD_1600_5_RPDOMappingParameter_mappedObject5        5
        #define OD_1600_6_RPDOMappingParameter_mappedObject6        6
        #define OD_1600_7_RPDOMappingParameter_mappedObject7        7
        #define OD_1600_8_RPDOMappingParameter_mappedObject8        8

/*1601 */
        #define OD_1601_RPDOMappingParameter                        0x1601

        #define OD_1601_0_RPDOMappingParameter_maxSubIndex          0
        #define OD_1601_1_RPDOMappingParameter_mappedObject1        1
        #define OD_1601_2_RPDOMappingParameter_mappedObject2        2
        #define OD_1601_3_RPDOMappingParameter_mappedObject3        3
        #define OD_1601_4_RPDOMappingParameter_mappedObject4        4
        #define OD_1601_5_RPDOMappingParameter_mappedObject5        5
        #define OD_1601_6_RPDOMappingParameter_mappedObject6        6
        #define OD_1601_7_RPDOMappingParameter_mappedObject7        7
        #define OD_1601_8_RPDOMappingParameter_mappedObject8        8

/*1800 */
        #define OD_1800_TPDOCommunicationParameter                  0x1800

        #define OD_1800_0_TPDOCommunicationParameter_maxSubIndex    0
        #define OD_1800_1_TPDOCommunicationParameter_COB_IDUsedByTPDO 1
        #define OD_1800_2_TPDOCommunicationParameter_transmissionType 2
        #define OD_1800_3_TPDOCommunicationParameter_inhibitTime    3
        #define OD_1800_4_TPDOCommunicationParameter_compatibilityEntry 4
        #define OD_1800_5_TPDOCommunicationParameter_eventTimer     5
        #define OD_1800_6_TPDOCommunicationParameter_SYNCStartValue 6

/*1801 */
        #define OD_1801_TPDOCommunicationParameter                  0x1801

        #define OD_1801_0_TPDOCommunicationParameter_maxSubIndex    0
        #define OD_1801_1_TPDOCommunicationParameter_COB_IDUsedByTPDO 1
        #define OD_1801_2_TPDOCommunicationParameter_transmissionType 2
        #define OD_1801_3_TPDOCommunicationParameter_inhibitTime    3
        #define OD_1801_4_TPDOCommunicationParameter_compatibilityEntry 4
        #define OD_1801_5_TPDOCommunicationParameter_eventTimer     5
        #define OD_1801_6_TPDOCommunicationParameter_SYNCStartValue 6

/*1a00 */
        #define OD_1a00_TPDOMappingParameter                        0x1a00

        #define OD_1a00_0_TPDOMappingParameter_maxSubIndex          0
        #define OD_1a00_1_TPDOMappingParameter_mappedObject1        1
        #define OD_1a00_2_TPDOMappingParameter_mappedObject2        2
        #define OD_1a00_3_TPDOMappingParameter_mappedObject3        3
        #define OD_1a00_4_TPDOMappingParameter_mappedObject4        4
        #define OD_1a00_5_TPDOMappingParameter_mappedObject5        5
        #define OD_1a00_6_TPDOMappingParameter_mappedObject6        6
        #define OD_1a00_7_TPDOMappingParameter_mappedObject7        7
        #define OD_1a00_8_TPDOMappingParameter_mappedObject8        8

/*1a01 */
        #define OD_1a01_TPDOMappingParameter                        0x1a01

        #define OD_1a01_0_TPDOMappingParameter_maxSubIndex          0
        #define OD_1a01_1_TPDOMappingParameter_mappedObject1        1
        #define OD_1a01_2_TPDOMappingParameter_mappedObject2        2
        #define OD_1a01_3_TPDOMappingParameter_mappedObject3        3
        #define OD_1a01_4_TPDOMappingParameter_mappedObject4        4
        #define OD_1a01_5_TPDOMappingParameter_mappedObject5        5
        #define OD_1a01_6_TPDOMappingParameter_mappedObject6        6
        #define OD_1a01_7_TPDOMappingParameter_mappedObject7        7
        #define OD_1a01_8_TPDOMappingParameter_mappedObject8        8

/*1f80 */
        #define OD_1f80_NMTStartup                                  0x1f80

/*1f81 */
        #define OD_1f81_slaveAssignment                             0x1f81

        #define OD_1f81_0_slaveAssignment_maxSubIndex               0
        #define OD_1f81_1_slaveAssignment_                          1
        #define OD_1f81_2_slaveAssignment_                          2
        #define OD_1f81_3_slaveAssignment_                          3
        #define OD_1f81_4_slaveAssignment_                          4
        #define OD_1f81_5_slaveAssignment_                          5
        #define OD_1f81_6_slaveAssignment_                          6
        #define OD_1f81_7_slaveAssignment_                          7
        #define OD_1f81_8_slaveAssignment_                          8
        #define OD_1f81_9_slaveAssignment_                          9
        #define OD_1f81_10_slaveAssignment_                         10
        #define OD_1f81_11_slaveAssignment_                         11
        #define OD_1f81_12_slaveAssignment_                         12
        #define OD_1f81_13_slaveAssignment_                         13
        #define OD_1f81_14_slaveAssignment_                         14
        #define OD_1f81_15_slaveAssignment_                         15
        #define OD_1f81_16_slaveAssignment_                         16
        #define OD_1f81_17_slaveAssignment_                         17
        #define OD_1f81_18_slaveAssignment_                         18
        #define OD_1f81_19_slaveAssignment_                         19
        #define OD_1f81_20_slaveAssignment_                         20
        #define OD_1f81_21_slaveAssignment_                         21
        #define OD_1f81_22_slaveAssignment_                         22
        #define OD_1f81_23_slaveAssignment_                         23
        #define OD_1f81_24_slaveAssignment_                         24
        #define OD_1f81_25_slaveAssignment_                         25
        #define OD_1f81_26_slaveAssignment_                         26
        #define OD_1f81_27_slaveAssignment_                         27
        #define OD_1f81_28_slaveAssignment_                         28
        #define OD_1f81_29_slaveAssignment_                         29
        #define OD_1f81_30_slaveAssignment_                         30
        #define OD_1f81_31_slaveAssignment_                         31
        #define OD_1f81_32_slaveAssignment_                         32
        #define OD_1f81_33_slaveAssignment_                         33
        #define OD_1f81_34_slaveAssignment_                         34
        #define OD_1f81_35_slaveAssignment_                         35
        #define OD_1f81_36_slaveAssignment_                         36
        #define OD_1f81_37_slaveAssignment_                         37
        #define OD_1f81_38_slaveAssignment_                         38
        #define OD_1f81_39_slaveAssignment_                         39
        #define OD_1f81_40_slaveAssignment_                         40
        #define OD_1f81_41_slaveAssignment_                         41
        #define OD_1f81_42_slaveAssignment_                         42
        #define OD_1f81_43_slaveAssignment_                         43
        #define OD_1f81_44_slaveAssignment_                         44
        #define OD_1f81_45_slaveAssignment_                         45
        #define OD_1f81_46_slaveAssignment_                         46
        #define OD_1f81_47_slaveAssignment_                         47
        #define OD_1f81_48_slaveAssignment_                         48
        #define OD_1f81_49_slaveAssignment_                         49
        #define OD_1f81_50_slaveAssignment_                         50
        #define OD_1f81_51_slaveAssignment_                         51
        #define OD_1f81_52_slaveAssignment_                         52
        #define OD_1f81_53_slaveAssignment_                         53
        #define OD_1f81_54_slaveAssignment_                         54
        #define OD_1f81_55_slaveAssignment_                         55
        #define OD_1f81_56_slaveAssignment_                         56
        #define OD_1f81_57_slaveAssignment_                         57
        #define OD_1f81_58_slaveAssignment_                         58
        #define OD_1f81_59_slaveAssignment_                         59
        #define OD_1f81_60_slaveAssignment_                         60
        #define OD_1f81_61_slaveAssignment_                         61
        #define OD_1f81_62_slaveAssignment_                         62
        #define OD_1f81_63_slaveAssignment_                         63
        #define OD_1f81_64_slaveAssignment_                         64
        #define OD_1f81_65_slaveAssignment_                         65
        #define OD_1f81_66_slaveAssignment_                         66
        #define OD_1f81_67_slaveAssignment_                         67
        #define OD_1f81_68_slaveAssignment_                         68
        #define OD_1f81_69_slaveAssignment_                         69
        #define OD_1f81_70_slaveAssignment_                         70
        #define OD_1f81_71_slaveAssignment_                         71
        #define OD_1f81_72_slaveAssignment_                         72
        #define OD_1f81_73_slaveAssignment_                         73
        #define OD_1f81_74_slaveAssignment_                         74
        #define OD_1f81_75_slaveAssignment_                         75
        #define OD_1f81_76_slaveAssignment_                         76
        #define OD_1f81_77_slaveAssignment_                         77
        #define OD_1f81_78_slaveAssignment_                         78
        #define OD_1f81_79_slaveAssignment_                         79
        #define OD_1f81_80_slaveAssignment_                         80
        #define OD_1f81_81_slaveAssignment_                         81
        #define OD_1f81_82_slaveAssignment_                         82
        #define OD_1f81_83_slaveAssignment_                         83
        #define OD_1f81_84_slaveAssignment_                         84
        #define OD_1f81_85_slaveAssignment_                         85
        #define OD_1f81_86_slaveAssignment_                         86
        #define OD_1f81_87_slaveAssignment_                         87
        #define OD_1f81_88_slaveAssignment_                         88
        #define OD_1f81_89_slaveAssignment_                         89
        #define OD_1f81_90_slaveAssignment_                         90
        #define OD_1f81_91_slaveAssignment_                         91
        #define OD_1f81_92_slaveAssignment_                         92
        #define OD_1f81_93_slaveAssignment_                         93
        #define OD_1f81_94_slaveAssignment_                         94
        #define OD_1f81_95_slaveAssignment_                         95
        #define OD_1f81_96_slaveAssignment_                         96
        #define OD_1f81_97_slaveAssignment_                         97
        #define OD_1f81_98_slaveAssignment_                         98
        #define OD_1f81_99_slaveAssignment_                         99
        #define OD_1f81_100_slaveAssignment_                        100
        #define OD_1f81_101_slaveAssignment_                        101
        #define OD_1f81_102_slaveAssignment_                        102
        #define OD_1f81_103_slaveAssignment_                        103
        #define OD_1f81_104_slaveAssignment_                        104
        #define OD_1f81_105_slaveAssignment_                        105
        #define OD_1f81_106_slaveAssignment_                        106
        #define OD_1f81_107_slaveAssignment_                        107
        #define OD_1f81_108_slaveAssignment_                        108
        #define OD_1f81_109_slaveAssignment_                        109
        #define OD_1f81_110_slaveAssignment_                        110
        #define OD_1f81_111_slaveAssignment_                        111
        #define OD_1f81_112_slaveAssignment_                        112
        #define OD_1f81_113_slaveAssignment_                        113
        #define OD_1f81_114_slaveAssignment_                        114
        #define OD_1f81_115_slaveAssignment_                        115
        #define OD_1f81_116_slaveAssignment_                        116
        #define OD_1f81_117_slaveAssignment_                        117
        #define OD_1f81_118_slaveAssignment_                        118
        #define OD_1f81_119_slaveAssignment_                        119
        #define OD_1f81_120_slaveAssignment_                        120
        #define OD_1f81_121_slaveAssignment_                        121
        #define OD_1f81_122_slaveAssignment_                        122
        #define OD_1f81_123_slaveAssignment_                        123
        #define OD_1f81_124_slaveAssignment_                        124
        #define OD_1f81_125_slaveAssignment_                        125
        #define OD_1f81_126_slaveAssignment_                        126
        #define OD_1f81_127_slaveAssignment_                        127

/*1f82 */
        #define OD_1f82_requestNMT                                  0x1f82

        #define OD_1f82_0_requestNMT_maxSubIndex                    0
        #define OD_1f82_1_requestNMT_                               1
        #define OD_1f82_2_requestNMT_                               2
        #define OD_1f82_3_requestNMT_                               3
        #define OD_1f82_4_requestNMT_                               4
        #define OD_1f82_5_requestNMT_                               5
        #define OD_1f82_6_requestNMT_                               6
        #define OD_1f82_7_requestNMT_                               7
        #define OD_1f82_8_requestNMT_                               8
        #define OD_1f82_9_requestNMT_                               9
        #define OD_1f82_10_requestNMT_                              10
        #define OD_1f82_11_requestNMT_                              11
        #define OD_1f82_12_requestNMT_                              12
        #define OD_1f82_13_requestNMT_                              13
        #define OD_1f82_14_requestNMT_                              14
        #define OD_1f82_15_requestNMT_                              15
        #define OD_1f82_16_requestNMT_                              16
        #define OD_1f82_17_requestNMT_                              17
        #define OD_1f82_18_requestNMT_                              18
        #define OD_1f82_19_requestNMT_                              19
        #define OD_1f82_20_requestNMT_                              20
        #define OD_1f82_21_requestNMT_                              21
        #define OD_1f82_22_requestNMT_                              22
        #define OD_1f82_23_requestNMT_                              23
        #define OD_1f82_24_requestNMT_                              24
        #define OD_1f82_25_requestNMT_                              25
        #define OD_1f82_26_requestNMT_                              26
        #define OD_1f82_27_requestNMT_                              27
        #define OD_1f82_28_requestNMT_                              28
        #define OD_1f82_29_requestNMT_                              29
        #define OD_1f82_30_requestNMT_                              30
        #define OD_1f82_31_requestNMT_                              31
        #define OD_1f82_32_requestNMT_                              32
        #define OD_1f82_33_requestNMT_                              33
        #define OD_1f82_34_requestNMT_                              34
        #define OD_1f82_35_requestNMT_                              35
        #define OD_1f82_36_requestNMT_                              36
        #define OD_1f82_37_requestNMT_                              37
        #define OD_1f82_38_requestNMT_                              38
        #define OD_1f82_39_requestNMT_                              39
        #define OD_1f82_40_requestNMT_                              40
        #define OD_1f82_41_requestNMT_                              41
        #define OD_1f82_42_requestNMT_                              42
        #define OD_1f82_43_requestNMT_                              43
        #define OD_1f82_44_requestNMT_                              44
        #define OD_1f82_45_requestNMT_                              45
        #define OD_1f82_46_requestNMT_                              46
        #define OD_1f82_47_requestNMT_                              47
        #define OD_1f82_48_requestNMT_                              48
        #define OD_1f82_49_requestNMT_                              49
        #define OD_1f82_50_requestNMT_                              50
        #define OD_1f82_51_requestNMT_                              51
        #define OD_1f82_52_requestNMT_                              52
        #define OD_1f82_53_requestNMT_                              53
        #define OD_1f82_54_requestNMT_                              54
        #define OD_1f82_55_requestNMT_                              55
        #define OD_1f82_56_requestNMT_                              56
        #define OD_1f82_57_requestNMT_                              57
        #define OD_1f82_58_requestNMT_                              58
        #define OD_1f82_59_requestNMT_                              59
        #define OD_1f82_60_requestNMT_                              60
        #define OD_1f82_61_requestNMT_                              61
        #define OD_1f82_62_requestNMT_                              62
        #define OD_1f82_63_requestNMT_                              63
        #define OD_1f82_64_requestNMT_                              64
        #define OD_1f82_65_requestNMT_                              65
        #define OD_1f82_66_requestNMT_                              66
        #define OD_1f82_67_requestNMT_                              67
        #define OD_1f82_68_requestNMT_                              68
        #define OD_1f82_69_requestNMT_                              69
        #define OD_1f82_70_requestNMT_                              70
        #define OD_1f82_71_requestNMT_                              71
        #define OD_1f82_72_requestNMT_                              72
        #define OD_1f82_73_requestNMT_                              73
        #define OD_1f82_74_requestNMT_                              74
        #define OD_1f82_75_requestNMT_                              75
        #define OD_1f82_76_requestNMT_                              76
        #define OD_1f82_77_requestNMT_                              77
        #define OD_1f82_78_requestNMT_                              78
        #define OD_1f82_79_requestNMT_                              79
        #define OD_1f82_80_requestNMT_                              80
        #define OD_1f82_81_requestNMT_                              81
        #define OD_1f82_82_requestNMT_                              82
        #define OD_1f82_83_requestNMT_                              83
        #define OD_1f82_84_requestNMT_                              84
        #define OD_1f82_85_requestNMT_                              85
        #define OD_1f82_86_requestNMT_                              86
        #define OD_1f82_87_requestNMT_                              87
        #define OD_1f82_88_requestNMT_                              88
        #define OD_1f82_89_requestNMT_                              89
        #define OD_1f82_90_requestNMT_                              90
        #define OD_1f82_91_requestNMT_                              91
        #define OD_1f82_92_requestNMT_                              92
        #define OD_1f82_93_requestNMT_                              93
        #define OD_1f82_94_requestNMT_                              94
        #define OD_1f82_95_requestNMT_                              95
        #define OD_1f82_96_requestNMT_                              96
        #define OD_1f82_97_requestNMT_                              97
        #define OD_1f82_98_requestNMT_                              98
        #define OD_1f82_99_requestNMT_                              99
        #define OD_1f82_100_requestNMT_                             100
        #define OD_1f82_101_requestNMT_                             101
        #define OD_1f82_102_requestNMT_                             102
        #define OD_1f82_103_requestNMT_                             103
        #define OD_1f82_104_requestNMT_                             104
        #define OD_1f82_105_requestNMT_                             105
        #define OD_1f82_106_requestNMT_                             106
        #define OD_1f82_107_requestNMT_                             107
        #define OD_1f82_108_requestNMT_                             108
        #define OD_1f82_109_requestNMT_                             109
        #define OD_1f82_110_requestNMT_                             110
        #define OD_1f82_111_requestNMT_                             111
        #define OD_1f82_112_requestNMT_                             112
        #define OD_1f82_113_requestNMT_                             113
        #define OD_1f82_114_requestNMT_                             114
        #define OD_1f82_115_requestNMT_                             115
        #define OD_1f82_116_requestNMT_                             116
        #define OD_1f82_117_requestNMT_                             117
        #define OD_1f82_118_requestNMT_                             118
        #define OD_1f82_119_requestNMT_                             119
        #define OD_1f82_120_requestNMT_                             120
        #define OD_1f82_121_requestNMT_                             121
        #define OD_1f82_122_requestNMT_                             122
        #define OD_1f82_123_requestNMT_                             123
        #define OD_1f82_124_requestNMT_                             124
        #define OD_1f82_125_requestNMT_                             125
        #define OD_1f82_126_requestNMT_                             126
        #define OD_1f82_127_requestNMT_                             127

/*1f89 */
        #define OD_1f89_bootTime                                    0x1f89

/*******************************************************************************
   STRUCTURES FOR VARIABLES IN DIFFERENT MEMORY LOCATIONS
*******************************************************************************/
#define  CO_OD_FIRST_LAST_WORD     0x55 //Any value from 0x01 to 0xFE. If changed, EEPROM will be reinitialized.

/***** Structure for ROM variables ********************************************/
struct sCO_OD_ROM{
               UNSIGNED32     FirstWord;

/*1000      */ UNSIGNED32      deviceType;
/*1005      */ UNSIGNED32      COB_ID_SYNCMessage;
/*1006      */ UNSIGNED32      communicationCyclePeriod;
/*1007      */ UNSIGNED32      synchronousWindowLength;
/*1008      */ VISIBLE_STRING  manufacturerDeviceName[13];
/*1009      */ VISIBLE_STRING  manufacturerHardwareVersion[3];
/*100a      */ VISIBLE_STRING  manufacturerSoftwareVersion[3];
/*100c      */ UNSIGNED16      guardTime;
/*1012      */ UNSIGNED32      COB_ID_TIME;
/*1014      */ UNSIGNED32      COB_ID_EMCY;
/*1015      */ UNSIGNED16      inhibitTimeEMCY;
/*1016      */ UNSIGNED32      consumerHeartbeatTime[4];
/*1017      */ UNSIGNED16      producerHeartbeatTime;
/*1018      */ OD_identity_t   identity;
/*1019      */ UNSIGNED8       synchronousCounterOverflowValue;
/*1029      */ UNSIGNED8       errorBehavior[6];
/*1200      */ OD_SDOServerParameter_t SDOServerParameter[1];
/*1400      */ OD_RPDOCommunicationParameter_t RPDOCommunicationParameter[2];
/*1600      */ OD_RPDOMappingParameter_t RPDOMappingParameter[2];
/*1800      */ OD_TPDOCommunicationParameter_t TPDOCommunicationParameter[2];
/*1a00      */ OD_TPDOMappingParameter_t TPDOMappingParameter[2];

               UNSIGNED32     LastWord;
};

/***** Structure for RAM variables ********************************************/
struct sCO_OD_RAM{
               UNSIGNED32     FirstWord;

/*1001      */ UNSIGNED8       errorRegister;
/*1002      */ UNSIGNED32      manufacturerStatusRegister;
/*1003      */ UNSIGNED32      preDefinedErrorField[8];
/*100d      */ UNSIGNED8       lifeTimeFactor;
/*1010      */ UNSIGNED32      storeParameters[1];
/*1011      */ UNSIGNED32      restoreDefaultParameters[1];
/*1013      */ UNSIGNED32      highResolutionTimeStamp;
/*1280      */ OD_SDOClientParameter_t SDOClientParameter[1];
/*1f80      */ UNSIGNED32      NMTStartup;
/*1f81      */ UNSIGNED32      slaveAssignment[127];
/*1f82      */ UNSIGNED8       requestNMT[127];
/*1f89      */ UNSIGNED32      bootTime;

               UNSIGNED32     LastWord;
};

/***** Structure for EEPROM variables ********************************************/
struct sCO_OD_EEPROM{
               UNSIGNED32     FirstWord;


               UNSIGNED32     LastWord;
};

/***** Declaration of Object Dictionary variables *****************************/
extern struct sCO_OD_ROM CO_OD_ROM;

extern struct sCO_OD_RAM CO_OD_RAM;

extern struct sCO_OD_EEPROM CO_OD_EEPROM;

/*******************************************************************************
   ALIASES FOR OBJECT DICTIONARY VARIABLES
*******************************************************************************/
/*1000, Data Type: UNSIGNED32 */
        #define OD_deviceType                                       CO_OD_ROM.deviceType

/*1001, Data Type: UNSIGNED8 */
        #define OD_errorRegister                                    CO_OD_RAM.errorRegister

/*1002, Data Type: UNSIGNED32 */
        #define OD_manufacturerStatusRegister                       CO_OD_RAM.manufacturerStatusRegister

/*1003, Data Type: UNSIGNED32, Array[8] */
        #define OD_preDefinedErrorField                             CO_OD_RAM.preDefinedErrorField
        #define ODL_preDefinedErrorField_arrayLength                8
        #define ODA_preDefinedErrorField_standardErrorField         0

/*1005, Data Type: UNSIGNED32 */
        #define OD_COB_ID_SYNCMessage                               CO_OD_ROM.COB_ID_SYNCMessage

/*1006, Data Type: UNSIGNED32 */
        #define OD_communicationCyclePeriod                         CO_OD_ROM.communicationCyclePeriod

/*1007, Data Type: UNSIGNED32 */
        #define OD_synchronousWindowLength                          CO_OD_ROM.synchronousWindowLength

/*1008, Data Type: VISIBLE_STRING */
        #define OD_manufacturerDeviceName                           CO_OD_ROM.manufacturerDeviceName
        #define ODL_manufacturerDeviceName_stringLength             13

/*1009, Data Type: VISIBLE_STRING */
        #define OD_manufacturerHardwareVersion                      CO_OD_ROM.manufacturerHardwareVersion
        #define ODL_manufacturerHardwareVersion_stringLength        3

/*100a, Data Type: VISIBLE_STRING */
        #define OD_manufacturerSoftwareVersion                      CO_OD_ROM.manufacturerSoftwareVersion
        #define ODL_manufacturerSoftwareVersion_stringLength        3

/*100c, Data Type: UNSIGNED16 */
        #define OD_guardTime                                        CO_OD_ROM.guardTime

/*100d, Data Type: UNSIGNED8 */
        #define OD_lifeTimeFactor                                   CO_OD_RAM.lifeTimeFactor

/*1010, Data Type: UNSIGNED32, Array[1] */
        #define OD_storeParameters                                  CO_OD_RAM.storeParameters
        #define ODL_storeParameters_arrayLength                     1
        #define ODA_storeParameters_saveAllParameters               0

/*1011, Data Type: UNSIGNED32, Array[1] */
        #define OD_restoreDefaultParameters                         CO_OD_RAM.restoreDefaultParameters
        #define ODL_restoreDefaultParameters_arrayLength            1
        #define ODA_restoreDefaultParameters_restoreAllDefaultParameters 0

/*1012, Data Type: UNSIGNED32 */
        #define OD_COB_ID_TIME                                      CO_OD_ROM.COB_ID_TIME

/*1013, Data Type: UNSIGNED32 */
        #define OD_highResolutionTimeStamp                          CO_OD_RAM.highResolutionTimeStamp

/*1014, Data Type: UNSIGNED32 */
        #define OD_COB_ID_EMCY                                      CO_OD_ROM.COB_ID_EMCY

/*1015, Data Type: UNSIGNED16 */
        #define OD_inhibitTimeEMCY                                  CO_OD_ROM.inhibitTimeEMCY

/*1016, Data Type: UNSIGNED32, Array[4] */
        #define OD_consumerHeartbeatTime                            CO_OD_ROM.consumerHeartbeatTime
        #define ODL_consumerHeartbeatTime_arrayLength               4
        #define ODA_consumerHeartbeatTime_consumerHeartbeatTime     0

/*1017, Data Type: UNSIGNED16 */
        #define OD_producerHeartbeatTime                            CO_OD_ROM.producerHeartbeatTime

/*1018, Data Type: identity_t */
        #define OD_identity                                         CO_OD_ROM.identity

/*1019, Data Type: UNSIGNED8 */
        #define OD_synchronousCounterOverflowValue                  CO_OD_ROM.synchronousCounterOverflowValue

/*1029, Data Type: UNSIGNED8, Array[6] */
        #define OD_errorBehavior                                    CO_OD_ROM.errorBehavior
        #define ODL_errorBehavior_arrayLength                       6
        #define ODA_errorBehavior_communication                     0
        #define ODA_errorBehavior_communicationOther                1
        #define ODA_errorBehavior_communicationPassive              2
        #define ODA_errorBehavior_generic                           3
        #define ODA_errorBehavior_deviceProfile                     4
        #define ODA_errorBehavior_manufacturerSpecific              5

/*1200, Data Type: SDOServerParameter_t */
        #define OD_SDOServerParameter                               CO_OD_ROM.SDOServerParameter

/*1280, Data Type: SDOClientParameter_t */
        #define OD_SDOClientParameter                               CO_OD_RAM.SDOClientParameter

/*1400, Data Type: RPDOCommunicationParameter_t */
        #define OD_RPDOCommunicationParameter                       CO_OD_ROM.RPDOCommunicationParameter

/*1600, Data Type: RPDOMappingParameter_t */
        #define OD_RPDOMappingParameter                             CO_OD_ROM.RPDOMappingParameter

/*1800, Data Type: TPDOCommunicationParameter_t */
        #define OD_TPDOCommunicationParameter                       CO_OD_ROM.TPDOCommunicationParameter

/*1a00, Data Type: TPDOMappingParameter_t */
        #define OD_TPDOMappingParameter                             CO_OD_ROM.TPDOMappingParameter

/*1f80, Data Type: UNSIGNED32 */
        #define OD_NMTStartup                                       CO_OD_RAM.NMTStartup

/*1f81, Data Type: UNSIGNED32, Array[127] */
        #define OD_slaveAssignment                                  CO_OD_RAM.slaveAssignment
        #define ODL_slaveAssignment_arrayLength                     127
        #define ODA_slaveAssignment_                                0

/*1f82, Data Type: UNSIGNED8, Array[127] */
        #define OD_requestNMT                                       CO_OD_RAM.requestNMT
        #define ODL_requestNMT_arrayLength                          127
        #define ODA_requestNMT_                                     0

/*1f89, Data Type: UNSIGNED32 */
        #define OD_bootTime                                         CO_OD_RAM.bootTime

#endif
// clang-format on
