# MotionCapture

使用Sensortag进行动作捕捉

Forked From : https://github.com/Yemi1234/COMP6733

## Demo

![README-2022-01-12-sensortag1](https://cdn.jsdelivr.net/gh/bicirci/PicBed@master/MarkDown/README-2022-01-12-sensortag1.png)
![README-2022-01-12-sensortag2](https://cdn.jsdelivr.net/gh/bicirci/PicBed@master/MarkDown/README-2022-01-12-sensortag2.png)

## Folders and Files

Our implementation of the SensorTag firmware code is located in: `SensorTag_COMP6733`. It is a modified copy of the SensorTag example code found in TI's BLE-STACK v2. To run our implementation, our respective files will need to copied into their equivalent file locations, to replace the example implementation's equivalent files.

All current Python code for BLE connection (from the master device), csv file sensor data storage and machine learning classification is located in: `python_BLE_connection`. This provides a 

All current Unity 3D code is located in: `Unity-animation`. Within this folder (if they have been included in the final submission) is a `character` folder for some of the modified 3D avatars, and `test\classification` and `test\joint-test` for pre-rendered classification animations and quaternion (and any kinematics) -based movement respectively.

## Installation Instructions

All development and testing was done on Windows 10.

### Texas Instruments

You are required to install the following:

 * Code Composer Studio (CCS): http://www.ti.com/tool/CCSTUDIO
 * BLE-STACK-2-2-3: http://www.ti.com/tool/BLE-STACK
 * TI v16.9.4 LTS (old compiler version): http://www.ti.com/tool/download/ARM-CGT-16/16.9.4.LTS
 * UniFlash: http://www.ti.com/tool/UNIFLASH

### Python

You are required to install the following libraries (at minimum):

 * Python 3.7+ (e.g. Anaconda distribution may resolve some dependencies)
 * aiofile: https://pypi.org/project/aiofile/
 * bleak: https://pypi.org/project/bleak/
 * ZeroMQ: https://pypi.org/project/pyzmq/
 * IntelHex: https://pypi.org/project/IntelHex/
 * scikit-learn
 * tensorflow
 * numpy
 * matplotlib

### Unity

You are required to install the following:

 * Unity: https://unity.com/
 * Blender: https://www.blender.org/


## Execution Instructions

### SensorTag

Please follow the follow-up instructions located in the README under `SensorTag_COMP6733` for more details. Code Composer Studio is not required if you are not intending to compile the .hex file yourself.

### Python

Assuming the DNN models under `python_BLE_connection` have been generated already for Model2TwoSensorsLargeClap.h5 and Model2TwoSensorsLargeClap.json, it should be sufficient to just run `python sensor-tag.py` to start the program. This program establishes Bluetooth LE connections to a hard-coded set of SensorTags (under the defined `worn_config` Python dictionary), performs classification, and outputs ZeroMQ messages for the Unity app.

### Unity

Assuming no dependencies have broken in submitting the final code implementation, it should be sufficient to open Unity and then open the project located at `.\Unity-animation\test\classification\classification`. Hit the Play button and this will run the 3D application in debug mode. The ZeroMQ messages received by Unity can be seen in the debugging console terminal within Unity.


## Files not included in final submission

### Additional Test Code

Some initial custom SensorTag firmware code that was written from scratch for USB probing of 9-axis IMU readings can be found in: `empty_CC2650STK_TI`.

MATLAB visualisation of the results for classification analysis can be found in: `Matlab`.

### Archive Code

`android_archive` contains archived Android code. Within this folder, `COMP6733_Android_git` contains work done on the initial Bluetooth LE device scanning screens. `SensorTag-CC2650` are TI-provided Android app reference materials. We had to drop this work due to both time constraints (faster to implement in Python than in Java) and knowledge constraints (not everyone in the team knew Java fluently).

`unity_archive` contains old Unity code we worked on for the ZeroMQ prior to systems integration, and any reference code we drew inspiration from. It has mostly been integrated into our current Unity codebase already.