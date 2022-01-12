# -*- coding: utf-8 -*-
"""
TI CC2650 SensorTag
-------------------
An example connecting to a TI CC2650 SensorTag (reference platform).
Created on 2018-01-10 by hbldh <henrik.blidh@nedomkull.com>
Source: https://github.com/hbldh/bleak/blob/master/examples/sensortag.py

Modified by Team Random for COMP6733 project:
Inclusion of MPU logic and message passing
"""

import os
os.environ['FOR_DISABLE_CONSOLE_CTRL_HANDLER'] = '1' # Anaconda specific?
# https://github.com/ContinuumIO/anaconda-issues/issues/905

# import platform
# import logging
import asyncio
import aiofile    # https://github.com/mosquito/aiofile/issues/16

from bleak import BleakClient
# from bleak import _logger as logger
from bleak.uuids import uuid16_dict

import sys
import time

from Madgwick import MadgwickAHRSupdate
from Mahony import MahonyAHRSupdate
import zmq
import zmq.asyncio

from ml import classifyDataNB, classifyDataDTC, classifyDataKNN, classifyDataSVM,classifyDataDNNStatic, classifyDataDNNDynamic

import pprint
pp = pprint.PrettyPrinter(indent=4, width=160)

dataCollectionCount = 0
collectedData = []
tempList = []

# zmq messaging
# https://pyzmq.readthedocs.io/en/latest/api/zmq.asyncio.html
# https://zeromq.org/socket-api/
PUB_PORT = 5555

context = zmq.asyncio.Context()
socket = context.socket(zmq.PUB) # publisher-subscriber with topics (body parts)
socket.bind("tcp://*:{}".format(PUB_PORT))

##################################################################################
TAG1_MAC = "98:07:2D:2F:79:04" # Eric, short cable
TAG2_MAC = "98:07:2D:32:3D:06"
TAG3_MAC = "54:6C:0E:52:CD:0B" # Yemi's
TAG4_MAC = "98:07:2D:31:EA:04" # Victor's

##################################################################################
LEFT_HAND = "Left Hand"
LEFT_FOREARM = "Left Forearm"
LEFT_UPPER_ARM = "Left Upper Arm"
RIGHT_HAND = "Right Hand"
RIGHT_FOREARM = "Right Forearm"
RIGHT_UPPER_ARM = "Right Upper Arm"
##################################################################################
worn_config = {                     # edit this for the desired body config
    TAG3_MAC : RIGHT_FOREARM,
    TAG1_MAC : RIGHT_UPPER_ARM
}

#worn_config = { TAG4_MAC : LEFT_HAND }
##################################################################################
NUM_BLE_CONN_TRIES = 20
LAST_LABELS_MAX_SIZE = 2
CLASSIFY_TOPIC = 'Classify'
##################################################################################
#given by bleak
ALL_SENSORTAG_CHARACTERISTIC_UUIDS = """
00002a00-0000-1000-8000-00805f9b34fb
00002a01-0000-1000-8000-00805f9b34fb
00002a04-0000-1000-8000-00805f9b34fb
00002a23-0000-1000-8000-00805f9b34fb
00002a24-0000-1000-8000-00805f9b34fb
00002a25-0000-1000-8000-00805f9b34fb
00002a26-0000-1000-8000-00805f9b34fb
00002a27-0000-1000-8000-00805f9b34fb
00002a28-0000-1000-8000-00805f9b34fb
00002a29-0000-1000-8000-00805f9b34fb
00002a2a-0000-1000-8000-00805f9b34fb
00002a50-0000-1000-8000-00805f9b34fb
00002a19-0000-1000-8000-00805f9b34fb
f000aa01-0451-4000-b000-000000000000
f000aa02-0451-4000-b000-000000000000
f000aa03-0451-4000-b000-000000000000
f000aa21-0451-4000-b000-000000000000
f000aa22-0451-4000-b000-000000000000
f000aa23-0451-4000-b000-000000000000
f000aa41-0451-4000-b000-000000000000
f000aa42-0451-4000-b000-000000000000
f000aa44-0451-4000-b000-000000000000
f000aa81-0451-4000-b000-000000000000
f000aa82-0451-4000-b000-000000000000
f000aa83-0451-4000-b000-000000000000
f000aa71-0451-4000-b000-000000000000
f000aa72-0451-4000-b000-000000000000
f000aa73-0451-4000-b000-000000000000
0000ffe1-0000-1000-8000-00805f9b34fb
f000aa65-0451-4000-b000-000000000000
f000aa66-0451-4000-b000-000000000000
f000ac01-0451-4000-b000-000000000000
f000ac02-0451-4000-b000-000000000000
f000ac03-0451-4000-b000-000000000000
f000ccc1-0451-4000-b000-000000000000
f000ccc2-0451-4000-b000-000000000000
f000ccc3-0451-4000-b000-000000000000
f000ffc1-0451-4000-b000-000000000000
f000ffc2-0451-4000-b000-000000000000
f000ffc3-0451-4000-b000-000000000000
f000ffc4-0451-4000-b000-000000000000
"""

uuid16_dict = {v: k for k, v in uuid16_dict.items()}

# https://rigado.zendesk.com/hc/en-us/articles/227621508-What-UUIDs-can-I-use-with-my-product-
# http://processors.wiki.ti.com/index.php/CC2650_SensorTag_User's_Guide#Calibration
SYSTEM_ID_UUID = "0000{0:x}-0000-1000-8000-00805f9b34fb".format(
    uuid16_dict.get("System ID")
)
MODEL_NBR_UUID = "0000{0:x}-0000-1000-8000-00805f9b34fb".format(
    uuid16_dict.get("Model Number String")
)
DEVICE_NAME_UUID = "0000{0:x}-0000-1000-8000-00805f9b34fb".format(
    uuid16_dict.get("Device Name")
)
FIRMWARE_REV_UUID = "0000{0:x}-0000-1000-8000-00805f9b34fb".format(
    uuid16_dict.get("Firmware Revision String")
)
HARDWARE_REV_UUID = "0000{0:x}-0000-1000-8000-00805f9b34fb".format(
    uuid16_dict.get("Hardware Revision String")
)
SOFTWARE_REV_UUID = "0000{0:x}-0000-1000-8000-00805f9b34fb".format(
    uuid16_dict.get("Software Revision String")
)
MANUFACTURER_NAME_UUID = "0000{0:x}-0000-1000-8000-00805f9b34fb".format(
    uuid16_dict.get("Manufacturer Name String")
)
BATTERY_LEVEL_UUID = "0000{0:x}-0000-1000-8000-00805f9b34fb".format(
    uuid16_dict.get("Battery Level")
)

#modified part
MPU_CONFIG_UUID = "f000aa82-0451-4000-b000-000000000000"
MPU_DATA_UUID = "f000aa81-0451-4000-b000-000000000000"
MPU_PERIOD_UUID = "f000aa83-0451-4000-b000-000000000000"
#end

KEY_PRESS_UUID = "0000{0:x}-0000-1000-8000-00805f9b34fb".format(0xffe1)
# I/O test points on SensorTag.
IO_DATA_CHAR_UUID = "f000aa65-0451-4000-b000-000000000000"
IO_CONFIG_CHAR_UUID = "f000aa66-0451-4000-b000-000000000000"

#assume range is 4G, converts data to m/s^2
def accConvert(data):
    v = (data  * 1.0)/(32768/8) * 9.8066
    return v

#converts gyro to deg/s
def gyroConvert(data):
    return (data * 1.0)/(65536/500) * 2 * 3.1415/360


##################################################################################
async def runBleSession(address, loop, classifier_q, debug=False):
    body_part = worn_config[address]
    def dprint(msg):
        if debug:
            print("{}: {}".format(body_part, msg))
        # if debug:
        #     loop.set_debug(True)
        #     l = logging.getLogger("asyncio")
        #     l.setLevel(logging.DEBUG)
        #     h = logging.StreamHandler(sys.stdout)
        #     h.setLevel(logging.DEBUG)
        #     l.addHandler(h)

    dprint("running, may take a while to connect - {}".format(address))

    for cur_ble_try in range(NUM_BLE_CONN_TRIES):
        try:
            async with BleakClient(address, loop=loop) as client:
                # connect to BLE server and read device id + model + device
                dprint("BleakClient started, address: '{}'".format(address))
                x = await client.is_connected()
                dprint("BleakClient connected: {0}".format(x))

                # do MPU configuration to enable sensor
                # ** (first generate the 2 byte array for mpu configure characteristic)
                #mpu_con_value = b'\x07\x02'  #0000 0111 0000 0010  first 3 set bits are for accelerator x y z, last set bit is for unit of the value
                mpu_con_value = b'\xff\x80' # 1111 1111 1000 0000 first 7 bits all sensors, 1 bit WOM, 1 bit rang 8G
                await client.write_gatt_char(MPU_CONFIG_UUID, mpu_con_value)
                mpu_con_resp = await client.read_gatt_char(MPU_CONFIG_UUID)
                dprint("mpu config is: {0}".format(mpu_con_resp))

                period_seconds = 0.1 # [100ms, 2.55s]
                mpu_period_val = int(0x64 * period_seconds)  # period(s) / 1s = mpu_period_val / 0x64
                await client.write_gatt_char(MPU_PERIOD_UUID, bytes([mpu_period_val]))
                mpu_period_resp = await client.read_gatt_char(MPU_PERIOD_UUID)
                dprint("mpu period is: {0}".format(mpu_period_resp))

                # poll for MPU data
                mpu_str2int = ['gx', 'gy', 'gz', 'ax', 'ay', 'az', 'mx', 'my', 'mz']    # dprint formatting
                mpu_unit2int = ['deg/s'] * 3 + ['m/s^2'] * 3 + ['uT'] * 3
                while True:
                    #await client.start_notify(KEY_PRESS_UUID, keypress_handler)
                    #await asyncio.sleep(period_seconds, loop=loop)

                    # read mpu data from gatt server
                    mpu_raw = await client.read_gatt_char(MPU_DATA_UUID) # returns bytearray
                    mpu_recvtime = time.time()
                    mpu_value = [mpu_raw[i:i+2] for i in range(0, len(mpu_raw), 2)] # each MPU reading is 16 bits
                    #dprint("mpu raw bytes (grouped):", mpu_value, "at time:", mpu_recvtime)
                    mpu_int = [int.from_bytes(i, byteorder='little', signed=True) for i in mpu_value]
                    #dprint("mpu raw readings: {0}".format(mpu_int))
                    #await client.stop_notify(KEY_PRESS_UUID)

                    # convert mpu raw readings to correct units
                    # ** gyro
                    mpu_int[0] = gyroConvert(mpu_int[0])
                    mpu_int[1] = gyroConvert(mpu_int[1])
                    mpu_int[2] = gyroConvert(mpu_int[2])
                    # ** acc
                    mpu_int[3] = accConvert(mpu_int[3])
                    mpu_int[4] = accConvert(mpu_int[4])
                    mpu_int[5] = accConvert(mpu_int[5])

                    # sensor_data = [[mpu_int[3], mpu_int[4], mpu_int[5],mpu_int[0], mpu_int[1],  # order specific for classification?
                    #                 mpu_int[2],mpu_int[6],mpu_int[7],mpu_int[8]]]

                    sensor_data = [[mpu_int[3], mpu_int[4], mpu_int[5],mpu_int[0], mpu_int[1],  # order specific for classification?
                                    mpu_int[2]]]

                    # ** mag - (no conversion required: x1 multiplier)
                    #mpu_strvals = ['{}={:.3f}{}'.format(mpu_str2int[i], mpu_int[i], mpu_unit2int[i]) for i in range(len(mpu_str2int))]
                    #dprint(', '.join(mpu_strvals))

                    #MadgwickAHRSupdate(gx, gy, gz, ax, ay, az, mx, my, mz, sampleFreq)
                    #quats = MadgwickAHRSupdate(mpu_int[0], mpu_int[1], mpu_int[2], mpu_int[3], mpu_int[4],
                    #                          mpu_int[5], mpu_int[6], mpu_int[7], mpu_int[8], 1/period_seconds)


                    c_msg = (body_part, mpu_recvtime, sensor_data)
                    await classifier_q.put(c_msg)

                    quats = MahonyAHRSupdate(mpu_int[0], mpu_int[1], mpu_int[2], mpu_int[3], mpu_int[4],
                                                mpu_int[5], mpu_int[6], mpu_int[7], mpu_int[8], 1/period_seconds)

                    # send MPU quaternion data to other subsystems (UI)
                    # ** pub-sub mechanism: type of pkt denoted by 'topic', which is the body part
                    # ** pkt structure is: ['body_part', 'recvtime,quaternion']. 1st part of pkt is topic
                    # ** pkt represented as string in csv format
                    msg = ','.join( [str(mpu_recvtime)] + list(map(str, quats)) )
                    #dprint("[mpu_raw len]: {}, [ZeroMQ]: '{}'\r\n".format(len(mpu_raw), msg))
                    await socket.send_multipart([body_part.encode('utf-8'), msg.encode('utf-8')])

        except Exception as e:
            dprint('Ignoring error and retrying: {}'.format(e))
            await asyncio.sleep(2)
            continue
    dprint('Failed to connect to BLE device!')
    while True: # needed for KeyboardInterrupt responsiveness
        await asyncio.sleep(2)


##################################################################################
# not any faster than putting the classifier in the runBleSession() loop
# since everything in a Python process is single threaded
async def runClassifier(loop, classifier_q, debug=False):
    def dprint(msg):
        if debug:
            print("{}: {}".format('Classifier', msg))
    registered_parts = set(worn_config.values())
    dprint('registered: {}'.format(registered_parts))

    global dataCollectionCount
    global collectedData
    global tempList

    # data capture
    start_sec = int(time.time())
    dir_name = 'recordings'
    data_fn = os.path.join(dir_name, 'allData_{}.csv'.format(start_sec))
    label_fn = os.path.join(dir_name, 'allLabels_{}.csv'.format(start_sec))

    # ZeroMQ "low pass" filtering...
    last_labels = []

    ###async with aiofiles.open(data_fn, mode='w', loop=loop) as data_file, aiofiles.open(label_fn, mode='w', loop=loop) as label_file:
    async with aiofile.AIOFile(data_fn, mode='w', loop=loop) as data_file, aiofile.AIOFile(label_fn, mode='w', loop=loop) as label_file:
        data_writer = aiofile.Writer(data_file)
        label_writer = aiofile.Writer(label_file)

        i = 0
        while True:
            received_parts = {}
            # get values from all registered body parts
            while len(received_parts) < len(registered_parts):
                recv_body_part, recv_time, recv_sensor_data = await classifier_q.get()
                #dprint('{}: {} received'.format(recv_time, recv_body_part))
                received_parts[recv_body_part] = recv_sensor_data

            # initial data capture
            for body_part in registered_parts:
                sensor_data = received_parts[recv_body_part]
                #dprint('storing {}: {}'.format(recv_body_part, sensor_data))
                data_csv_row = "{},{},{}\n".format( i, body_part, ','.join(map(str,sensor_data[0])) )
                ###await data_file.write(data_csv_row)
                await data_writer(data_csv_row)

            # apply model
            body_part_list = list(registered_parts)
            num_bodyparts = len(body_part_list)
            sensor_data = received_parts[body_part_list[0]]
            if num_bodyparts > 1:
                for i in range(1,num_bodyparts):
                    sensor_data[0] = sensor_data[0] + received_parts[body_part_list[i]][0]
                #print(sensor_data[0])
                #print("====================================================================")
                #combined_data.append(received_parts[parts])
            #print('sensor_data: ##################')
            #pp.pprint(sensor_data)

            #nb_result = classifyDataNB(sensor_data) # "Naive Bayes: "
            #dtc_result = classifyDataDTC(sensor_data) # "Decision Tree: "
            #svm_result = classifyDataSVM(sensor_data) # "SVM: "
            #knn_result = classifyDataKNN(sensor_data) # "KNN: "

            #print("Naive Bayes: " + nb_result)
            #print("Decision Tree: " + dtc_result)
            #print("SVM: " + svm_result)
            #print("KNN: " + knn_result)


            #dnn_static_result = classifyDataDNNStatic(sensor_data) # "DNN static: "

            #print("Vector input: " + dnn_static_result)
            dnn_dynamic_result = None
            dataCollectionCount = dataCollectionCount + 1
            collectedData.append(sensor_data[0])
            #if (len(collectedData) > 10):
            #    collectedData.pop(0)

            #if(len(collectedData) == 10):
            #    tempList.append(collectedData)
                #del tempList[:]
                #dnn_dynamic_result = classifyDataDNNDynamic(tempList)
                #del tempList[:]
            if (dataCollectionCount%10 == 0):
                tempList.append(collectedData)
                #print('tempList: #######################')
                #pp.pprint(tempList)
                dnn_dynamic_result = classifyDataDNNDynamic(tempList)
                #nb_result = classifyDataNB(tempList) # "Naive Bayes: "
                #dtc_result = classifyDataDTC(tempList) # "Decision Tree: "
                #svm_result = classifyDataSVM(tempList) # "SVM: "
                #knn_result = classifyDataKNN(tempList) # "KNN: "

                #print("Naive Bayes: " + nb_result)
                #print("Decision Tree: " + dtc_result)
                #print("SVM: " + svm_result)
                #print("KNN: " + knn_result)

                del tempList[:]
                del collectedData[:]
                dataCollectionCount = 0
                #print("Neural Network:" + dnn_dynamic_result)

            # remaining data capture
            #label_contents = [nb_result, dtc_result, svm_result, knn_result, dnn_static_result, dnn_dynamic_result]
            #dprint('storing {}: {}'.format( i, label_contents ))
            #await label_file.write('{},'.format(i) + ','.join(label_contents) + "\n")
            #await label_writer('{},'.format(i) + ','.join(label_contents) + "\n")

            # send classification result to other subsystems (UI)
            # ** pkt structure (all vals str): [topic, ml_result]
            msg = dnn_dynamic_result
            if msg != None:
                if len(last_labels) >= LAST_LABELS_MAX_SIZE:
                    last_labels.pop(0)
                if len(last_labels) < LAST_LABELS_MAX_SIZE:
                    last_labels.append(msg)
                # filter out transient conditions
                if len(set(last_labels)) == 1:
                    dprint("[ZeroMQ '{}']: '{}'\r\n".format(CLASSIFY_TOPIC, msg))
                    await socket.send_multipart([CLASSIFY_TOPIC.encode('utf-8'), msg.encode('utf-8')])

            # next loop setup
            i += 1

##################################################################################
if __name__ == "__main__":
    print("BLE client program (laptop) started...")
    os.environ["PYTHONASYNCIODEBUG"] = str(1)
    loop = asyncio.get_event_loop()
    classifier_q = asyncio.Queue(loop=loop) # make classifier dict if multiple queues needed

    print("Creating tasks...") # see global variable: worn_config
    tasks = []
    for mac in worn_config:
        tasks.append( loop.create_task(runBleSession(mac, loop, classifier_q, True)) )
    tasks.append( loop.create_task(runClassifier(loop, classifier_q, True)) )

    # https://stackoverflow.com/questions/30361824/asynchronous-exception-handling-in-python
    print("Running all tasks...")
    start_time = time.time()
    try:
        loop.run_until_complete( asyncio.gather(*tasks) )
    except KeyboardInterrupt:
        time_spent = time.time() - start_time
        sleep_time = max(2, time_spent/20e3)
        print("User generated Ctrl+C! Waiting {:.2f}s for file contents to be written...".format(sleep_time))
        time.sleep(sleep_time)
        print("Ran for: {} seconds. Exiting...".format(time_spent))
