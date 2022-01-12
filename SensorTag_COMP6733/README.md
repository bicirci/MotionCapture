# Code Composer Studio and BLE Stack Instructions

## Pre-requisites
 * Code Composer Studio
 * BLE-STACK v2 (this repository provides a modified version of the cc2650 example files)
 * UniFlash
 * Python 2/3 library: IntelHex

## About this repository

`ble_sdk_2_02_03_08 (slash) examples`: place the contents inside this folder under `C:\ti\simplelink\ble_sdk_2_02_03_08\examples`

`ble_sdk_2_02_03_08 (slash) src (slash) examples`: replace the contents inside this folder under `C:\ti\simplelink\ble_sdk_2_02_03_08\src\examples`

## Default Firmware and Bluetooth LE advertisement modification

Follow the instructions at the links below to customise the BLE advertisements to be always enabled:

 * https://github.com/PeakUp/TIDC-CC2650STK-SENSORTAG-Custom-Firmware-Continuous-Advertising-Broadcasting-/blob/master/CC2650stk%20-%20Sensortag%20Custom%20Firmware%20Download%20(Continuous%20Broadcast_Advertise).rtf

 * https://stackoverflow.com/questions/38042880/sensortag-2-cc2650-advertising-indefinately-firmware/44965797

Further clarification to these instructions is available at:

http://e2e.ti.com/support/wireless-connectivity/bluetooth/f/538/t/594826?CCS-CC2650STK-Unable-to-flash-SensorTag-super-hex-file

NOTE 1: make sure to use the same compiler (it's quite old, around version 5 or so from recollection?) as the one required by the SensorTag firmware. (Addressed in the 2nd link)

NOTE 2: for each of the three required builds (for the full .hex file to be generated after merging), make sure in the Build Settings (in Code Composer Studio) to enable the use of armhex utility, and add in the additional arguments as specified in the tutorial.

NOTE 3: run merge.bat by going to: `C:\ti\simplelink\ble_sdk_2_02_03_08\examples\cc2650stk\sensortag\ccs\app`. It should be set up (excluding any hardcoded file path issues) if you use this repository's copy - mainly with regards
to the Python verison and the file location of the required Python file called in merge.bat.

An example hex file can be flashed directly from (and is compatible with the downloadable TI SensorTag phone app):
`C:\ti\simplelink\ble_sdk_2_02_03_08\examples\hex`.

The source code for this hex file is located across several folders:
 * `C:\ti\simplelink\ble_sdk_2_02_03_08\examples\cc2650stk\sensortag\ccs` - see `app` (FlashOnly_OAD build required) and `stack` (FlashROM build required) folders (they are each Eclipse projects).
 * `C:\ti\simplelink\ble_sdk_2_02_03_08\src\examples\sensortag\cc26xx` - a lot of additional .c and .h files that get linked are located here. Includes main.c and sensortag.c which get used under the `app` Eclipse project?
 * `C:\ti\simplelink\ble_sdk_2_02_03_08\examples\util\bim_extflash\cc2640` - another Eclipse project that is required. Needed to be built for merge.bat to work and generate the full executable .hex file.

After merge.bat is run, the fully executable .hex file is located at:
`C:\ti\simplelink\ble_sdk_2_02_03_08\examples\cc2650stk\sensortag\ccs\app\FlashOnly_OAD`. In this folder, the file `sensortag_cc2650stk_all.hex` can be flashed using Uniflash.

Also see the documentation under the folder for extra info: `setup instructions`.

## Next steps

http://bluetooth-mdw.blogspot.com/2014/12/customising-texas-instruments-sensortag.html