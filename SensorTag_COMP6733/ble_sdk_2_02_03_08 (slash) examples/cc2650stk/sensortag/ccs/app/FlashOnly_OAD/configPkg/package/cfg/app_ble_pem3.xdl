/*
 * Do not modify this file; it is automatically generated from the template
 * linkcmd.xdt in the ti.platforms.simplelink package and will be overwritten.
 */

/*
 * put '"'s around paths because, without this, the linker
 * considers '-' as minus operator, not a file name character.
 */


-l"C:\ti\simplelink\ble_sdk_2_02_03_08\examples\cc2650stk\sensortag\ccs\app\FlashOnly_OAD\configPkg\package\cfg\app_ble_pem3.oem3"
-l"C:/ti/tirtos_cc13xx_cc26xx_2_21_01_08/products/tidrivers_cc13xx_cc26xx_2_21_01_01/packages/ti/mw/display/lib/display.aem3"
-l"C:/ti/tirtos_cc13xx_cc26xx_2_21_01_08/products/tidrivers_cc13xx_cc26xx_2_21_01_01/packages/ti/mw/lcd/lib/lcd.aem3"
-l"C:/ti/tirtos_cc13xx_cc26xx_2_21_01_08/products/tidrivers_cc13xx_cc26xx_2_21_01_01/packages/ti/mw/grlib/lib/grlib.aem3"
-l"C:/ti/tirtos_cc13xx_cc26xx_2_21_01_08/products/tidrivers_cc13xx_cc26xx_2_21_01_01/packages/ti/drivers/rf/lib/rf_singleMode_cc26xxware.aem3"
-l"C:/ti/tirtos_cc13xx_cc26xx_2_21_01_08/products/tidrivers_cc13xx_cc26xx_2_21_01_01/packages/ti/drivers/lib/drivers_cc26xxware.aem3"
-l"C:/ti/tirtos_cc13xx_cc26xx_2_21_01_08/products/tidrivers_cc13xx_cc26xx_2_21_01_01/packages/ti/drivers/lib/power_cc26xx_tirtos.aem3"
-l"C:/ti/tirtos_cc13xx_cc26xx_2_21_01_08/products/tidrivers_cc13xx_cc26xx_2_21_01_01/packages/ti/drivers/pdm/lib/pdm_cc26xxware.aem3"
-l"C:\ti\tirtos_cc13xx_cc26xx_2_21_01_08\products\tidrivers_cc13xx_cc26xx_2_21_01_01\packages\ti\mw\fatfs\lib\release\ti.mw.fatfs.aem3"
-l"C:/ti/tirtos_cc13xx_cc26xx_2_21_01_08/products/tidrivers_cc13xx_cc26xx_2_21_01_01/packages/ti/drivers/ports/lib/tirtosport.aem3"
-l"C:\ti\simplelink\ble_sdk_2_02_03_08\examples\cc2650stk\sensortag\ccs\config\src\sysbios\sysbios.aem3"
-l"C:\ti\tirtos_cc13xx_cc26xx_2_21_01_08\products\bios_6_46_01_38\packages\ti\targets\arm\rtsarm\lib\boot.aem3"
-l"C:\ti\tirtos_cc13xx_cc26xx_2_21_01_08\products\bios_6_46_01_38\packages\ti\targets\arm\rtsarm\lib\auto_init.aem3"

--retain="*(xdc.meta)"

/* C6x Elf symbols */
--symbol_map __TI_STACK_SIZE=__STACK_SIZE
--symbol_map __TI_STACK_BASE=__stack
--symbol_map _stack=__stack


--args 0x0
-heap  0x0
-stack 0x200

/*
 * Linker command file contributions from all loaded packages:
 */

/* Content from xdc.services.global (null): */

/* Content from xdc (null): */

/* Content from xdc.corevers (null): */

/* Content from xdc.shelf (null): */

/* Content from xdc.services.spec (null): */

/* Content from xdc.services.intern.xsr (null): */

/* Content from xdc.services.intern.gen (null): */

/* Content from xdc.services.intern.cmd (null): */

/* Content from xdc.bld (null): */

/* Content from ti.targets (null): */

/* Content from ti.targets.arm.elf (null): */

/* Content from xdc.rov (null): */

/* Content from xdc.runtime (null): */

/* Content from ti.targets.arm.rtsarm (null): */

/* Content from ti.sysbios.interfaces (null): */

/* Content from ti.sysbios.family (null): */

/* Content from ti.sysbios.family.arm (ti/sysbios/family/arm/linkcmd.xdt): */
--retain "*(.vecs)"

/* Content from xdc.services.getset (null): */

/* Content from ti.sysbios.rts (ti/sysbios/rts/linkcmd.xdt): */

/* Content from xdc.runtime.knl (null): */

/* Content from ti.catalog.arm.cortexm3 (null): */

/* Content from ti.catalog.peripherals.hdvicp2 (null): */

/* Content from ti.catalog (null): */

/* Content from ti.catalog.arm.peripherals.timers (null): */

/* Content from xdc.platform (null): */

/* Content from xdc.cfg (null): */

/* Content from ti.catalog.arm.cortexm4 (null): */

/* Content from ti.platforms.simplelink (null): */

/* Content from ti.sysbios.hal (null): */

/* Content from ti.sysbios (null): */

/* Content from ti.sysbios.family.arm.cc26xx (null): */

/* Content from ti.sysbios.family.arm.m3 (ti/sysbios/family/arm/m3/linkcmd.xdt): */
-u _c_int00
--retain "*(.resetVecs)"
ti_sysbios_family_arm_m3_Hwi_nvic = 0xe000e000;

/* Content from ti.sysbios.knl (null): */

/* Content from ti.drivers.ports (null): */

/* Content from ti.mw.fatfs (null): */

/* Content from ti.sysbios.gates (null): */

/* Content from ti.sysbios.xdcruntime (null): */

/* Content from ti.drivers.pdm (null): */

/* Content from ti.sysbios.utils (null): */

/* Content from ti.drivers (null): */

/* Content from ti.drivers.rf (null): */

/* Content from ti.mw.grlib (null): */

/* Content from ti.mw.lcd (null): */

/* Content from ti.mw.display (null): */

/* Content from ti.mw (null): */

/* Content from configPkg (null): */

/* Content from xdc.services.io (null): */



/*
 * symbolic aliases for static instance objects
 */
xdc_runtime_Startup__EXECFXN__C = 1;
xdc_runtime_Startup__RESETFXN__C = 1;


SECTIONS
{
    .bootVecs:  type = DSECT
    .resetVecs: load > 0x1010
    .vecs: load > 0x20000000, type = NOLOAD



    xdc.meta: type = COPY
    xdc.noload: type = COPY
}
