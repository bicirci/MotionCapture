################################################################################
# Automatically-generated file. Do not edit!
################################################################################

SHELL = cmd.exe

# Each subdirectory must supply rules for building sources it contributes
Middleware/sensortag/SensorTagTest.obj: C:/ti/tirtos_cc13xx_cc26xx_2_21_01_08/products/tidrivers_cc13xx_cc26xx_2_21_01_01/packages/ti/mw/sensortag/SensorTagTest.c $(GEN_OPTS) | $(GEN_FILES) $(GEN_MISC_FILES)
	@echo 'Building file: "$<"'
	@echo 'Invoking: ARM Compiler'
	"C:/ti/ti-cgt-arm_16.9.4.LTS/bin/armcl" --cmd_file="C:/ti/simplelink/ble_sdk_2_02_03_08/examples/cc2650stk/sensortag/ccs/app/../../../../../src/config/build_components.opt" --cmd_file="C:/ti/simplelink/ble_sdk_2_02_03_08/examples/cc2650stk/sensortag/ccs/app/../stack/build_config.opt" --cmd_file="C:/ti/simplelink/ble_sdk_2_02_03_08/examples/cc2650stk/sensortag/ccs/app/../config/ccs_compiler_defines.bcfg"  -mv7M3 --code_state=16 --abi=eabi -me -O4 --opt_for_speed=0 --include_path="C:/ti/ti-cgt-arm_16.9.4.LTS/include" --include_path="C:/ti/simplelink/ble_sdk_2_02_03_08/src/examples/sensortag/cc26xx/app" --include_path="C:/ti/simplelink/ble_sdk_2_02_03_08/src/controller/cc26xx/inc" --include_path="C:/ti/simplelink/ble_sdk_2_02_03_08/src/inc" --include_path="C:/ti/simplelink/ble_sdk_2_02_03_08/src/rom" --include_path="C:/ti/simplelink/ble_sdk_2_02_03_08/src/common/cc26xx" --include_path="C:/ti/simplelink/ble_sdk_2_02_03_08/src/icall/inc" --include_path="C:/ti/simplelink/ble_sdk_2_02_03_08/src/inc" --include_path="C:/ti/simplelink/ble_sdk_2_02_03_08/src/profiles/batt/cc26xx" --include_path="C:/ti/simplelink/ble_sdk_2_02_03_08/src/profiles/dev_info" --include_path="C:/ti/simplelink/ble_sdk_2_02_03_08/src/profiles/hid_dev/cc26xx" --include_path="C:/ti/simplelink/ble_sdk_2_02_03_08/src/profiles/keys" --include_path="C:/ti/simplelink/ble_sdk_2_02_03_08/src/profiles/oad/cc26xx" --include_path="C:/ti/simplelink/ble_sdk_2_02_03_08/src/profiles/roles" --include_path="C:/ti/simplelink/ble_sdk_2_02_03_08/src/profiles/roles/cc26xx" --include_path="C:/ti/simplelink/ble_sdk_2_02_03_08/src/profiles/sensor_profile/cc26xx" --include_path="C:/ti/simplelink/ble_sdk_2_02_03_08/src/components/heapmgr" --include_path="C:/ti/simplelink/ble_sdk_2_02_03_08/src/components/hal/src/inc" --include_path="C:/ti/simplelink/ble_sdk_2_02_03_08/src/components/hal/src/target/_common/cc26xx" --include_path="C:/ti/simplelink/ble_sdk_2_02_03_08/src/components/hal/src/target/_common" --include_path="C:/ti/simplelink/ble_sdk_2_02_03_08/src/target" --include_path="C:/ti/simplelink/ble_sdk_2_02_03_08/src/components/icall/src" --include_path="C:/ti/simplelink/ble_sdk_2_02_03_08/src/components/icall/src/inc" --include_path="C:/ti/simplelink/ble_sdk_2_02_03_08/src/components/osal/src/inc" --include_path="C:/ti/simplelink/ble_sdk_2_02_03_08/src/components/services/src/saddr" --include_path="C:/ti/simplelink/ble_sdk_2_02_03_08/src/components/services/src/sdata" --include_path="C:/ti/tirtos_cc13xx_cc26xx_2_21_01_08/products/cc26xxware_2_24_03_17272" --include_path="C:/ti/tirtos_cc13xx_cc26xx_2_21_01_08/products/tidrivers_cc13xx_cc26xx_2_21_01_01/packages" --include_path="C:/ti/tirtos_cc13xx_cc26xx_2_21_01_08/products/tidrivers_cc13xx_cc26xx_2_21_01_01/packages/ti/mw/extflash" --include_path="C:/ti/tirtos_cc13xx_cc26xx_2_21_01_08/products/tidrivers_cc13xx_cc26xx_2_21_01_01/packages/ti/mw/sensors" --include_path="C:/ti/tirtos_cc13xx_cc26xx_2_21_01_08/products/tidrivers_cc13xx_cc26xx_2_21_01_01/packages/ti/mw/sensortag" --c99 --define=CC2650STK --define=CC26XX --define=Display_DISABLE_ALL --define=EXCLUDE_AUDIO --define=FACTORY_IMAGE --define=FEATURE_OAD --define=GAPROLE_TASK_STACK_SIZE=600 --define=GATT_TI_UUID_128_BIT --define=HEAPMGR_SIZE=0 --define=ICALL_MAX_NUM_ENTITIES=11 --define=ICALL_MAX_NUM_TASKS=8 --define=POWER_SAVING --define=ST_TASK_STACK_SIZE=848 --define=USE_ICALL --define=xdc_runtime_Assert_DISABLE_ALL --define=xdc_runtime_Log_DISABLE_ALL --diag_warning=225 --diag_suppress=48 --diag_wrap=off --display_error_number --gen_func_subsections=on --preproc_with_compile --preproc_dependency="Middleware/sensortag/$(basename $(<F)).d_raw" --obj_directory="Middleware/sensortag" $(GEN_OPTS__FLAG) "$<"
	@echo 'Finished building: "$<"'
	@echo ' '


