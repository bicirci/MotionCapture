################################################################################
# Automatically-generated file. Do not edit!
################################################################################

SHELL = cmd.exe

# Each subdirectory must supply rules for building sources it contributes
TOOLS/onboard.obj: C:/ti/simplelink/ble_sdk_2_02_03_08/src/common/cc26xx/onboard.c $(GEN_OPTS) | $(GEN_FILES) $(GEN_MISC_FILES)
	@echo 'Building file: "$<"'
	@echo 'Invoking: ARM Compiler'
	"C:/ti/ti-cgt-arm_16.9.4.LTS/bin/armcl" --cmd_file="C:/ti/simplelink/ble_sdk_2_02_03_08/examples/cc2650stk/sensortag/ccs/stack/../../../../../src/config/build_components.opt" --cmd_file="C:/ti/simplelink/ble_sdk_2_02_03_08/examples/cc2650stk/sensortag/ccs/stack/build_config.opt"  -mv7M3 --code_state=16 --abi=eabi -me -O4 --opt_for_speed=0 --include_path="C:/ti/ti-cgt-arm_16.9.4.LTS/include" --include_path="C:/ti/simplelink/ble_sdk_2_02_03_08/src/examples/sensortag/cc26xx/stack" --include_path="C:/ti/simplelink/ble_sdk_2_02_03_08/src/inc" --include_path="C:/ti/simplelink/ble_sdk_2_02_03_08/src/common/cc26xx" --include_path="C:/ti/simplelink/ble_sdk_2_02_03_08/src/components/hal/src/target/_common" --include_path="C:/ti/simplelink/ble_sdk_2_02_03_08/src/components/hal/src/target/_common" --include_path="C:/ti/simplelink/ble_sdk_2_02_03_08/src/components/hal/src/target" --include_path="C:/ti/simplelink/ble_sdk_2_02_03_08/src/components/hal/src/target/_common/cc26xx" --include_path="C:/ti/simplelink/ble_sdk_2_02_03_08/src/components/hal/src/inc" --include_path="C:/ti/simplelink/ble_sdk_2_02_03_08/src/components/osal/src/inc" --include_path="C:/ti/simplelink/ble_sdk_2_02_03_08/src/components/services/src/saddr" --include_path="C:/ti/simplelink/ble_sdk_2_02_03_08/src/components/services/src/nv/cc26xx" --include_path="C:/ti/simplelink/ble_sdk_2_02_03_08/src/components/services/src/nv" --include_path="C:/ti/simplelink/ble_sdk_2_02_03_08/src/components/icall/src/inc" --include_path="C:/ti/simplelink/ble_sdk_2_02_03_08/src/inc" --include_path="C:/ti/simplelink/ble_sdk_2_02_03_08/src/rom" --include_path="C:/ti/simplelink/ble_sdk_2_02_03_08/src/controller/cc26xx/inc" --include_path="C:/ti/simplelink/ble_sdk_2_02_03_08/src/components/services/src/aes/cc26xx" --include_path="C:/ti/simplelink/ble_sdk_2_02_03_08/src/components/npi/src" --include_path="C:/ti/simplelink/ble_sdk_2_02_03_08/src/common/cc26xx/npi/stack" --include_path="C:/ti/simplelink/ble_sdk_2_02_03_08/src/icall/inc" --include_path="C:/ti/simplelink/ble_sdk_2_02_03_08/src/profiles/roles" --include_path="C:/ti/tirtos_cc13xx_cc26xx_2_21_01_08/products/cc26xxware_2_24_03_17272" --c99 --define=CC26XX --define=CC26XXWARE --define=DATA= --define=EXT_HAL_ASSERT --define=FLASH_ROM_BUILD --define=GATT_NO_CLIENT --define=INCLUDE_AES_DECRYPT --define=NEAR_FUNC= --define=OSAL_CBTIMER_NUM_TASKS=1 --define=OSAL_MAX_NUM_PROXY_TASKS=8 --define=OSAL_SNV=0 --define=POWER_SAVING --define=USE_ICALL --define=xDEBUG --define=xDEBUG_ENC --define=xDEBUG_GPIO --define=xDEBUG_SW_TRACE --define=xNO_BLE_SECURITY --define=xPM_DISABLE_PWRDOWN --define=xTESTMODES --define=xTEST_BLEBOARD --diag_warning=225 --diag_suppress=48 --diag_suppress=16004 --diag_wrap=off --display_error_number --preproc_with_compile --preproc_dependency="TOOLS/$(basename $(<F)).d_raw" --obj_directory="TOOLS" $(GEN_OPTS__FLAG) "$<"
	@echo 'Finished building: "$<"'
	@echo ' '


