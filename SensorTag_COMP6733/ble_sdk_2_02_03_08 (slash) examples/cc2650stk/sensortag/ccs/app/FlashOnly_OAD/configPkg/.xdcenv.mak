#
_XDCBUILDCOUNT = 
ifneq (,$(findstring path,$(_USEXDCENV_)))
override XDCPATH = C:/ti/tirtos_cc13xx_cc26xx_2_21_01_08/packages;C:/ti/tirtos_cc13xx_cc26xx_2_21_01_08/products/tidrivers_cc13xx_cc26xx_2_21_01_01/packages;C:/ti/tirtos_cc13xx_cc26xx_2_21_01_08/products/bios_6_46_01_38/packages;C:/ti/tirtos_cc13xx_cc26xx_2_21_01_08/products/uia_2_01_00_01/packages;C:/ti/ccs920/ccs/ccs_base
override XDCROOT = C:/ti/xdctools_3_32_00_06_core
override XDCBUILDCFG = ./config.bld
endif
ifneq (,$(findstring args,$(_USEXDCENV_)))
override XDCARGS = 
override XDCTARGETS = 
endif
#
ifeq (0,1)
PKGPATH = C:/ti/tirtos_cc13xx_cc26xx_2_21_01_08/packages;C:/ti/tirtos_cc13xx_cc26xx_2_21_01_08/products/tidrivers_cc13xx_cc26xx_2_21_01_01/packages;C:/ti/tirtos_cc13xx_cc26xx_2_21_01_08/products/bios_6_46_01_38/packages;C:/ti/tirtos_cc13xx_cc26xx_2_21_01_08/products/uia_2_01_00_01/packages;C:/ti/ccs920/ccs/ccs_base;C:/ti/xdctools_3_32_00_06_core/packages;..
HOSTOS = Windows
endif
