import os

# toolchains options
ARCH='arc'
CPU='em'
CROSS_TOOL='gcc'

if os.getenv('RTT_CC'):
    CROSS_TOOL = os.getenv('RTT_CC')

if CROSS_TOOL == 'gcc':
    PLATFORM 	= 'gcc'
    EXEC_PATH 	= 'C:/arc_gnu/bin'
elif CROSS_TOOL =='mw':
    PLATFORM 	= 'mw'
    EXEC_PATH 	= 'C:/ARC/MetaWare/arc/bin'

if os.getenv('RTT_EXEC_PATH'):
    EXEC_PATH = os.getenv('RTT_EXEC_PATH')

BUILD = 'debug'

if PLATFORM == 'gcc':
    # toolchains
    PREFIX = 'arc-elf32-'
    CC = PREFIX + 'gcc'
    CXX = PREFIX + 'g++'
    AS = PREFIX + 'gcc'
    AR = PREFIX + 'ar'
    LINK = PREFIX + 'gcc'
    TARGET_EXT = 'elf'
    SIZE = PREFIX + 'size'
    OBJDUMP = PREFIX + 'objdump'
    OBJCPY = PREFIX + 'objcopy'
    DBG = PREFIX + 'gdb'

    OPT_ARGFILE = ' -mno-sdata -Wall -mcpu=em4_fpus -mlittle-endian -mcode-density -mdiv-rem -mswap -mnorm -mmpy-option=6 -mbarrel-shifter -mfpu=fpus_all'
    COMMON_COMPILE_OPT = ' '

    CFLAGS = OPT_ARGFILE + COMMON_COMPILE_OPT + ' -std=gnu99 '
    CXXFLAGS = OPT_ARGFILE + COMMON_COMPILE_OPT
    AFLAGS = ' -c ' + OPT_ARGFILE + COMMON_COMPILE_OPT + ' -x assembler-with-cpp '

    LINK_SCRIPT = 'emsk_em9d_gnu.ld'
    LFLAGS = OPT_ARGFILE + ' -mno-sdata -nostartfiles -Wl,--gc-sections,-Map=emsk_em9d.map,-cref,-u,system_vectors -T %s ' % LINK_SCRIPT

    OPENOCD_SCRIPT_ROOT = EXEC_PATH + '/../share/openocd/scripts'
    OPENOCD_CFG_FILE = OPENOCD_SCRIPT_ROOT + '/board/snps_em_sk_v2.2.cfg'

    OPENOCD_OPTIONS  = '-s %s -f %s' % (OPENOCD_SCRIPT_ROOT, OPENOCD_CFG_FILE)

    DBG_HW_FLAGS = ''' -ex "target remote | openocd --pipe %s" -ex "load" ''' % OPENOCD_OPTIONS

    TARGET = 'rtthread_snps_emsk_em9d.' + TARGET_EXT

    CPATH = ''
    LPATH = ''

    if BUILD == 'debug':
        CFLAGS += ' -O0 -gdwarf-2'
        AFLAGS += ' -gdwarf-2'
    else:
        CFLAGS += ' -O2'

    POST_ACTION = OBJCPY + ' -O binary $TARGET rtthread.bin\n' +\
            SIZE + ' $TARGET \n'

elif PLATFORM == 'mw':
    # toolchains
    CC = 'ccac'
    CXX = 'ccac'
    AS = 'ccac'
    AR = 'arac'
    LINK = 'ccac'
    TARGET_EXT = 'elf'
    SIZE = 'sizeac'
    OBJDUMP = 'elfdumpac'
    OBJCPY = 'elf2bin'
    DBG = 'mdb'
    OPT_ARGFILE = ' -arcv2em -core2 -Hrgf_banked_regs=32 -HL -Xunaligned -Xcode_density -Xdiv_rem=radix2 -Xswap -Xbitscan -Xmpy_option=mpyd -Xshift_assist -Xbarrel_shifter -Xdsp2 -Xdsp_complex -Xdsp_divsqrt=radix2 -Xdsp_itu \
             -Xdsp_accshift=full -Xagu_large -Xxy -Xbitstream -Xfpus_div -Xfpu_mac -Xfpuda -Xfpus_mpy_slow -Xfpus_div_slow -Xtimer0 -Xtimer1 -Xstack_check -Hccm -Xdmac '
    COMMON_COMPILE_OPT = ' -Hnoccm -Hnosdata -Wincompatible-pointer-types -Hnocopyr '

    if BUILD == 'debug':
        COMMON_COMPILE_OPT += ' -g -O0 '
    else:
        COMMON_COMPILE_OPT += ' -O2 '

    CFLAGS = OPT_ARGFILE + COMMON_COMPILE_OPT + ' -Hnocplus '
    CXXFLAGS = OPT_ARGFILE + COMMON_COMPILE_OPT
    AFLAGS = ' -c ' + OPT_ARGFILE + COMMON_COMPILE_OPT + ' -Hasmcpp '

    LINK_SCRIPT = 'emsk_em9d_mw.ld'
    LFLAGS = OPT_ARGFILE + ' -Hnocopyr -Hnosdata -Hnocrt -Hldopt=-Coutput=emsk_em9d.map -Hldopt=-Csections -Hldopt=-Ccrossfunc -Hldopt=-Csize -zstdout %s' % LINK_SCRIPT

    TARGET = 'rtthread_snps_emsk_em9d.' + TARGET_EXT

    CPATH = ''
    LPATH = ''

    POST_ACTION = OBJCPY + ' $TARGET rtthread.bin\n' +\
            SIZE + ' $TARGET \n'
