################################################################################
# Automatically-generated file. Do not edit!
################################################################################

SHELL = cmd.exe

# Each subdirectory must supply rules for building sources it contributes
build-2106586031:
	@$(MAKE) --no-print-directory -Onone -f TOOLS/subdir_rules.mk build-2106586031-inproc

build-2106586031-inproc: C:/ti/simplelink/ble_sdk_2_02_03_08/examples/cc2650stk/sensortag/ccs/config/app_ble.cfg
	@echo 'Building file: "$<"'
	@echo 'Invoking: XDCtools'
	"C:/ti/xdctools_3_32_00_06_core/xs" --xdcpath="C:/ti/tirtos_cc13xx_cc26xx_2_21_01_08/packages;C:/ti/tirtos_cc13xx_cc26xx_2_21_01_08/products/tidrivers_cc13xx_cc26xx_2_21_01_01/packages;C:/ti/tirtos_cc13xx_cc26xx_2_21_01_08/products/bios_6_46_01_38/packages;C:/ti/tirtos_cc13xx_cc26xx_2_21_01_08/products/uia_2_01_00_01/packages;C:/ti/ccs920/ccs/ccs_base;" xdc.tools.configuro -o configPkg -t ti.targets.arm.elf.M3 -p ti.platforms.simplelink:CC2650F128 -r release -c "C:/ti/ti-cgt-arm_16.9.4.LTS" --cfgArgs "NO_ROM=1,OAD_IMG_E=1" --compileOptions "-mv7M3 --code_state=16 --abi=eabi -me -O4 --opt_for_speed=0 --include_path=\"C:/ti/ti-cgt-arm_16.9.4.LTS/include\" --include_path=\"C:/ti/simplelink/ble_sdk_2_02_03_08/src/examples/sensortag/cc26xx/app\" --include_path=\"C:/ti/simplelink/ble_sdk_2_02_03_08/src/controller/cc26xx/inc\" --include_path=\"C:/ti/simplelink/ble_sdk_2_02_03_08/src/inc\" --include_path=\"C:/ti/simplelink/ble_sdk_2_02_03_08/src/rom\" --include_path=\"C:/ti/simplelink/ble_sdk_2_02_03_08/src/common/cc26xx\" --include_path=\"C:/ti/simplelink/ble_sdk_2_02_03_08/src/icall/inc\" --include_path=\"C:/ti/simplelink/ble_sdk_2_02_03_08/src/inc\" --include_path=\"C:/ti/simplelink/ble_sdk_2_02_03_08/src/profiles/batt/cc26xx\" --include_path=\"C:/ti/simplelink/ble_sdk_2_02_03_08/src/profiles/dev_info\" --include_path=\"C:/ti/simplelink/ble_sdk_2_02_03_08/src/profiles/hid_dev/cc26xx\" --include_path=\"C:/ti/simplelink/ble_sdk_2_02_03_08/src/profiles/keys\" --include_path=\"C:/ti/simplelink/ble_sdk_2_02_03_08/src/profiles/oad/cc26xx\" --include_path=\"C:/ti/simplelink/ble_sdk_2_02_03_08/src/profiles/roles\" --include_path=\"C:/ti/simplelink/ble_sdk_2_02_03_08/src/profiles/roles/cc26xx\" --include_path=\"C:/ti/simplelink/ble_sdk_2_02_03_08/src/profiles/sensor_profile/cc26xx\" --include_path=\"C:/ti/simplelink/ble_sdk_2_02_03_08/src/components/heapmgr\" --include_path=\"C:/ti/simplelink/ble_sdk_2_02_03_08/src/components/hal/src/inc\" --include_path=\"C:/ti/simplelink/ble_sdk_2_02_03_08/src/components/hal/src/target/_common/cc26xx\" --include_path=\"C:/ti/simplelink/ble_sdk_2_02_03_08/src/components/hal/src/target/_common\" --include_path=\"C:/ti/simplelink/ble_sdk_2_02_03_08/src/target\" --include_path=\"C:/ti/simplelink/ble_sdk_2_02_03_08/src/components/icall/src\" --include_path=\"C:/ti/simplelink/ble_sdk_2_02_03_08/src/components/icall/src/inc\" --include_path=\"C:/ti/simplelink/ble_sdk_2_02_03_08/src/components/osal/src/inc\" --include_path=\"C:/ti/simplelink/ble_sdk_2_02_03_08/src/components/services/src/saddr\" --include_path=\"C:/ti/simplelink/ble_sdk_2_02_03_08/src/components/services/src/sdata\" --include_path=\"C:/ti/tirtos_cc13xx_cc26xx_2_21_01_08/products/cc26xxware_2_24_03_17272\" --include_path=\"C:/ti/tirtos_cc13xx_cc26xx_2_21_01_08/products/tidrivers_cc13xx_cc26xx_2_21_01_01/packages\" --include_path=\"C:/ti/tirtos_cc13xx_cc26xx_2_21_01_08/products/tidrivers_cc13xx_cc26xx_2_21_01_01/packages/ti/mw/extflash\" --include_path=\"C:/ti/tirtos_cc13xx_cc26xx_2_21_01_08/products/tidrivers_cc13xx_cc26xx_2_21_01_01/packages/ti/mw/sensors\" --include_path=\"C:/ti/tirtos_cc13xx_cc26xx_2_21_01_08/products/tidrivers_cc13xx_cc26xx_2_21_01_01/packages/ti/mw/sensortag\" --c99 --define=CC2650STK --define=CC26XX --define=Display_DISABLE_ALL --define=EXCLUDE_AUDIO --define=FACTORY_IMAGE --define=FEATURE_OAD --define=GAPROLE_TASK_STACK_SIZE=600 --define=GATT_TI_UUID_128_BIT --define=HEAPMGR_SIZE=0 --define=ICALL_MAX_NUM_ENTITIES=11 --define=ICALL_MAX_NUM_TASKS=8 --define=POWER_SAVING --define=ST_TASK_STACK_SIZE=848 --define=USE_ICALL --define=xdc_runtime_Assert_DISABLE_ALL --define=xdc_runtime_Log_DISABLE_ALL --diag_warning=225 --diag_suppress=48 --diag_wrap=off --display_error_number --gen_func_subsections=on " "$<"
	@echo 'Finished building: "$<"'
	@echo ' '

configPkg/linker.cmd: build-2106586031 C:/ti/simplelink/ble_sdk_2_02_03_08/examples/cc2650stk/sensortag/ccs/config/app_ble.cfg
configPkg/compiler.opt: build-2106586031
configPkg/: build-2106586031


