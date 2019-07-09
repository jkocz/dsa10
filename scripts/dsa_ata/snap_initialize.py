#! /usr/bin/env python
import argparse
import adc5g
import casperfpga
import time
import numpy as np
import struct
import socket
import sys

fpgahost = sys.argv[1]


snap = casperfpga.CasperFpga(fpgahost, timeout = 20)
snap.get_system_information('dsa_ata_v3.fpg')

print "Configuring ADC->FPGA interface"
chosen_phase, glitches = adc5g.calibrate_mmcm_phase(snap, 0, ['ss_adc'])

print "Configuring ADCs for dual-input mode"
adc5g.spi.set_spi_control(snap, 0, adcmode=0b0100, stdby=0, dmux=1, bg=1, bdw=0b11, fs=0, test=0)
