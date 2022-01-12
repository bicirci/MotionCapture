/*
 * Copyright (c) 2017, Texas Instruments Incorporated
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 *
 * *  Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 *
 * *  Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 *
 * *  Neither the name of Texas Instruments Incorporated nor the names of
 *    its contributors may be used to endorse or promote products derived
 *    from this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
 * THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
 * PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
 * CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
 * EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
 * PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
 * OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
 * WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
 * OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
 * EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

/***** Includes *****/
/* Standard C Libraries */
#include <stdlib.h>
#include <stdio.h>

#include <xdc/std.h>
#include <xdc/runtime/System.h>

#include <ti/sysbios/BIOS.h>
/* TI Drivers */
#include <ti/drivers/rf/RF.h>
#include <ti/drivers/PIN.h>
#include <ti/drivers/pin/PINCC26XX.h>

#include <ti/sysbios/knl/Clock.h>
#include <ti/sysbios/knl/Task.h>

#include <ti/mw/display/Display.h>
#include <ti/mw/display/DisplayExt.h>

//#include "fusion_9axis.h"

#include "SensorI2C.c"
#include "SensorMpu9250.c"

//#include "MadgwickAHRS.c"
#include "MadgwickAHRS.h"

#include <time.h>
#include <ti/sysbios/hal/Seconds.h>

/* Board Header files */
#include "Board.h"

#define TASKSTACKSIZE   768

Task_Struct task0Struct;
Char task0Stack[TASKSTACKSIZE];

Void motionSensor(UArg arg0, UArg arg1){

    System_printf("Entered Task\n");
    System_flush();

    Display_Params params;
    Display_Params_init(&params);
    params.lineClearMode = DISPLAY_CLEAR_BOTH;

    Display_Handle hDisplaySerial = Display_open(Display_Type_UART, &params);


    int debug = 2;

    if (SensorI2C_open()){
        Task_sleep((UInt)arg0);
        SensorMpu9250_init();
        SensorMpu9250_powerOn();
        SensorMpu9250_enable(0x003F);
    }

    static float acc_x;
    static float acc_y;
    static float acc_z;
    static float gyro_x;
    static float gyro_y;
    static float gyro_z;
    int16_t magData[3];
    uint16_t accData[3];
    uint16_t gyroData[3];

    uint8_t status;

    SensorMpu9250_accSetRange(ACC_RANGE_8G);
    int rang = SensorMpu9250_accReadRange();
    //Display_print1(hDisplaySerial, 0, 0, "Range is %d", rang);

    bool success;
    char temp[100] = {0};

    float radConvert = 2*3.1415/360;
    float accelConvert = 9.8066;




    while(1){
        success = SensorMpu9250_accRead(accData);
        if (success){
            acc_x = SensorMpu9250_accConvert(accData[0]);
            acc_y = SensorMpu9250_accConvert(accData[1]);
            acc_z = SensorMpu9250_accConvert(accData[2]);
        } else {
            Display_print0(hDisplaySerial, 0, 0, "Accel Failed");
        }

        success = SensorMpu9250_gyroRead(gyroData);
        if (success){
            gyro_x = SensorMpu9250_gyroConvert(gyroData[0]);
            gyro_y = SensorMpu9250_gyroConvert(gyroData[1]);
            gyro_z = SensorMpu9250_gyroConvert(gyroData[2]);;

        } else {
            Display_print0(hDisplaySerial, 0, 0, "Gyro failed");
        }

        status = SensorMpu9250_magRead(magData);
        success = status == MAG_STATUS_OK;

        if (status == MAG_BYPASS_FAIL)
        {
            SensorMpu9250_magReset();
        }


        MadgwickAHRSupdate(gyro_x, gyro_y, gyro_z,
                           acc_x,acc_y,acc_z,
                                (float)magData[0], (float)magData[1], (float)magData[2]);
        //MadgwickAHRSupdateIMU(gyro_x, gyro_y, gyro_z, acc_x, acc_y, acc_z);

        //Printing values
        if (debug == 1){
            sprintf(temp, "Accel: x=%1.5f, y=%1.5f, z=%1.5f", acc_x,acc_y,acc_z);
            Display_print1(hDisplaySerial, 0, 0, "%s", temp);
            sprintf(temp, "Accel: x=%1.5f, y=%1.5f, z=%1.5f", acc_x*accelConvert,acc_y*accelConvert,acc_z*accelConvert);
            Display_print1(hDisplaySerial, 0, 0, "%s", temp);
            sprintf(temp, "Gyro: x=%1.5f, y=%1.5f,z=%1.5f", gyro_x, gyro_y, gyro_z);
            Display_print1(hDisplaySerial, 0, 0, "%s", temp);
            sprintf(temp, "Gyro: x=%1.5f, y=%1.5f,z=%1.5f", gyro_x * radConvert, gyro_y*radConvert, gyro_z*radConvert);
            Display_print1(hDisplaySerial, 0, 0, "%s", temp);
            sprintf(temp, "Mag: x=%.2f, y=%.2f, z=%.2f", (float)magData[0], (float)magData[1], (float)magData[2]);
            Display_print1(hDisplaySerial, 0, 0, "%s", temp);
            sprintf(temp, "%.2f %.2f %.2f %.2f", q0, q1, q2, q3);
            Display_print1(hDisplaySerial, 0, 0, "%s", temp);
        } else if (debug == 2) {
            sprintf(temp, "%1.2f %1.2f %1.2f %1.2f %1.2f %1.2f %.1f %.1f %.1f %.2f %.2f %.2f %.2f",
                    acc_x,acc_y,acc_z,
                    gyro_x, gyro_y, gyro_z,
                            (float)magData[0], (float)magData[1], (float)magData[2],
                            q0, q1, q2, q3);
            Display_print1(hDisplaySerial, 0, 0, "%s", temp);
        } else if (debug == 3){
            sprintf(temp, "Accel: x=%d, y=%d, z=%d", (uint16_t)accData[0], (uint16_t)accData[1],(uint16_t)accData[2]);
            Display_print1(hDisplaySerial, 0, 0, "%s", temp);
            sprintf(temp, "Gyro: x=%d, y=%d,z=%d", (uint16_t)gyroData[0], (uint16_t)gyroData[1], (uint16_t)gyroData[2]);
            Display_print1(hDisplaySerial, 0, 0, "%s", temp);
            sprintf(temp, "Mag: x=%d, y=%d, z=%d", (uint16_t)magData[0], (uint16_t)magData[1], (uint16_t)magData[2]);
            Display_print1(hDisplaySerial, 0, 0, "%s", temp);
            sprintf(temp, "%.2f %.2f %.2f %.2f", q0, q1, q2, q3);
            Display_print1(hDisplaySerial, 0, 0, "%s", temp);

        } else {
            sprintf(temp, "%.2f %.2f %.2f %.2f", q0, q1, q2, q3);
            Display_print1(hDisplaySerial, 0, 0, "%s", temp);
        }
        //Task_sleep((UInt)arg0);

        //sprintf(temp, "Time(GMT): %d\n", t);
        //Display_print1(hDisplaySerial, 0, 0, "%s", temp);


        Task_sleep(10000);  //10 ms

    }
}


int main(void)
{
    Task_Params taskParams;
    Board_initGeneral();

    System_printf("Starting ...\n");
    System_flush();

    Task_Params_init(&taskParams);
    taskParams.arg0 = 100000/Clock_tickPeriod;
    System_printf("Clock tick: %d\n",Clock_tickPeriod);
    System_flush();
    taskParams.stackSize = TASKSTACKSIZE;
    taskParams.stack = &task0Stack;
    Task_construct(&task0Struct, (Task_FuncPtr)motionSensor, &taskParams, NULL);

    /* Start BIOS */
    BIOS_start();

    return (0);
}

