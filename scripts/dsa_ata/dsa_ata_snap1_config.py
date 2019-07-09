#!/usr/bin/env python


import struct
import casperfpga
import time
import numpy as np

fpga =casperfpga.CasperFpga('dsa-ata-snap-1')

mac_base0 = (2<<40) + (2<<32)
dest_macff= 255*(2**40) + 255*(2**32) + 255*(2**24) + 255*(2**16) + 255*(2**8) + 255
arp_table = [dest_macff for i in range(256)]

src_ip =  10*(2**24) + 10*(2**16) + 2*(2**8) + 161
src_ip0 =  10*(2**24) + 10*(2**16) + 2*(2**8) + 170+1 

src_mac = 0*(2**40) + 35*(2**32) + 242*(2**24) + 241*(2**16) + 23*(2**8) + 1
src_mac0 = mac_base0 + src_ip0

dest_ip = 10*(2**24) + 10*(2**16) + 2*(2**8) + 151 

dest_port = 4015

src_port = 4000

#fpga.write_int('acc_len',15)
fpga.write_int('snap_index',0)
fpga.write_int('acc_len',127)
fpga.write_int('fft_shift',65535)
fpga.write_int('fft_shift1',65535)
fpga.write_int('fft_del0',5)
fpga.write_int('fft_del1',1029)
fpga.write_int('port1',dest_port)
#fpga.write_int('port',dest_port)
fpga.write_int('ip1',dest_ip)
#fpga.write_int('ip',dest_ip)


#coeff = 2**17-1
#coeffs = np.ones(2048,'I')*coeff
#write_coeffs = struct.pack('>2048I',*coeffs)
#fpga.write('eq_0_coeffs',write_coeffs);
#fpga.write('eq_1_coeffs',write_coeffs);
#fpga.write('eq_2_coeffs',write_coeffs);
#fpga.write('eq_3_coeffs',write_coeffs);


#fpga.write_int('sel1',2)
#fpga.write_int('coeff1',20000)
fpga.write_int('sel1',1)
fpga.write_int('coeff1',7)

#gateway=1
#device_name='eth1_gbe1'
#subnet_mask=0xffff8000
#ctrl_pack=struct.pack('>QLLLLLLBBH',src_mac, 0, gateway, src_ip, 0, 0, 0, 0, 1, src_port)
#subnet_mask_pack=struct.pack('>L',subnet_mask)
#arp_pack=struct.pack('>256Q',*arp_table)
#fpga.blindwrite(device_name,ctrl_pack,offset=0)
#fpga.blindwrite(device_name,subnet_mask_pack,offset=0x38)
#fpga.write(device_name,arp_pack,offset=0x3000)


gateway=1
device_name='eth1_gbe1'
subnet_mask=0xffffff00
ctrl_pack=struct.pack('>QLLLLLLBBH',src_mac0, 0, gateway, src_ip0, 0, 0, 0, 0, 1, src_port)
subnet_mask_pack=struct.pack('>L',subnet_mask)
arp_pack=struct.pack('>256Q',*arp_table)
fpga.blindwrite(device_name,ctrl_pack,offset=0)
fpga.blindwrite(device_name,subnet_mask_pack,offset=0x38)
fpga.write(device_name,arp_pack,offset=0x3000)

