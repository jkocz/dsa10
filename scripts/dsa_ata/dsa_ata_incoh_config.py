#!/usr/bin/env python



import struct
import casperfpga
import time
import numpy as np
import datetime
import pause

nfpga_start = 0
nfpga_stop = 1
fpgas = ['dsa-ata-snap-1', 'dsa-ata-snap-2','dsa-ata-snap-3','dsa-ata-snap-4','dsa-ata-snap-5','dsa-ata-snap-6','dsa-ata-snap-7','dsa-ata-snap-8','dsa-ata-snap-9','dsa-ata-snap-10']

fpga_ip = [161,162,163,164,165,166,167,168,169,170]
fpga_list = []

mac_base0 = (2<<40) + (2<<32)
dest_macff= 255*(2**40) + 255*(2**32) + 255*(2**24) + 255*(2**16) + 255*(2**8) + 255
arp_table = [dest_macff for i in range(256)]

fpga_mac = [
        0*(2**40) + 35*(2**32) + 242*(2**24) + 241*(2**16) + 23*(2**8) + 1, # 00:23:f2:f1:17:01 snap-1
	0*(2**40) + 17*(2**32) + 230*(2**24) + 211*(2**16) + 23*(2**8) + 1, # 00:11:e6:d3:17:01 snap-2
	0*(2**40) +  9*(2**32) + 119*(2**24) +   9*(2**16) + 23*(2**8) + 1, # 00:09:77:09:17:01 snap-3
	0*(2**40) + 32*(2**32) + 135*(2**24) +  63*(2**16) + 23*(2**8) + 1, # 00:20:87:3f:17:01 snap-4
	0*(2**40) +  6*(2**32) + 171*(2**24) +  63*(2**16) + 23*(2**8) + 1, # 00:06:ab:3f:17:01 snap-5
	0*(2**40) + 16*(2**32) + 176*(2**24) + 103*(2**16) + 23*(2**8) + 1, # 00:10:b0:67:17:01 snap-6
	0*(2**40) + 19*(2**32) + 168*(2**24) +  59*(2**16) + 23*(2**8) + 1, # 00:13:a8:3b:17:01 snap-7
	0*(2**40) + 35*(2**32) +  46*(2**24) + 157*(2**16) + 23*(2**8) + 1, # 00:23:2e:9d:17:01 snap-8
	0*(2**40) + 21*(2**32) + 107*(2**24) + 215*(2**16) + 23*(2**8) + 1, # 00:15:6b:d7:17:01 snap-9
	0*(2**40) +  7*(2**32) +   1*(2**24) + 112*(2**16) + 23*(2**8) + 1, # 00:07:01:70:17:01 snap-10
]	

arp_table[151] = 228*(2**40) + 29*(2**32) + 45*(2**24) +  7*(2**16) + 63*(2**8) + 224
arp_table[152] = 228*(2**40) + 29*(2**32) + 45*(2**24) + 16*(2**16) + 29*(2**8) + 208 
arp_table[153] = 228*(2**40) + 29*(2**32) + 45*(2**24) + 16*(2**16) + 26*(2**8) +  80 
#arp_table[154] = 228*(2**40) + 29*(2**32) + 45*(2**24) +  7*(2**16) + 63*(2**8) + 224
arp_table[155] = 228*(2**40) + 29*(2**32) + 45*(2**24) + 15*(2**16) + 250*(2**8) + 48 
arp_table[156] = 124*(2**40) + 254*(2**32) + 144*(2**24) + 146*(2**16) + 17*(2**8) + 144 
#
for i in range(nfpga_start,nfpga_stop):
	#send sync pulse through data
	fpga_list.append(casperfpga.CasperFpga(fpgas[i]))

for i in range(nfpga_start,nfpga_stop):
	print "Setting up FPGA: " + fpgas[i] 
	#fpga =casperfpga.CasperFpga(fpgas[i])
	
	src_ip =  10*(2**24) + 10*(2**16) + 2*(2**8) + fpga_ip[i]
	src_ip0 =  10*(2**24) + 10*(2**16) + 2*(2**8) + 172 + i
	
	src_mac = fpga_mac[i]
	src_mac0 = mac_base0 + src_ip0
	arp_table[171+i] = src_mac0
	
	dest_ip = 10*(2**24) + 10*(2**16) + 2*(2**8) + 151 
	
	dest_port = 4015
	
	src_port = 4000
	
	fpga_list[i].write_int('snap_index',i)
	fpga_list[i].write_int('acc_len',127)
	fpga_list[i].write_int('fft_shift',65535)
	fpga_list[i].write_int('fft_shift1',65535)
	fpga_list[i].write_int('port1',dest_port)
	#fpga_list.write_int('port',dest_port)
	fpga_list[i].write_int('ip1',dest_ip)
	#fpga_list.write_int('ip',dest_ip)
	fpga_list[i].write_int('sel1',1)
	fpga_list[i].write_int('coeff1',7)
	
	gateway=1
	device_name='eth1_gbe1'
	subnet_mask=0xffffff00
	#subnet_mask=0xffff8000
	ctrl_pack=struct.pack('>QLLLLLLBBH',src_mac0, 0, gateway, src_ip0, 0, 0, 0, 0, 1, src_port)
	subnet_mask_pack=struct.pack('>L',subnet_mask)
	arp_pack=struct.pack('>256Q',*arp_table)
	fpga_list[i].blindwrite(device_name,ctrl_pack,offset=0)
	fpga_list[i].blindwrite(device_name,subnet_mask_pack,offset=0x38)
	fpga_list[i].write(device_name,arp_pack,offset=0x3000)
	
	
	#gateway=1
	#device_name='eth_gbe0'
	#subnet_mask=0xffffff00
	#ctrl_pack=struct.pack('>QLLLLLLBBH',src_mac0, 0, gateway, src_ip0, 0, 0, 0, 0, 1, src_port)
	#subnet_mask_pack=struct.pack('>L',subnet_mask)
	#arp_pack=struct.pack('>256Q',*arp_table)
	#fpga_list[i].blindwrite(device_name,ctrl_pack,offset=0)
	#fpga_list[i].blindwrite(device_name,subnet_mask_pack,offset=0x38)
	#fpga_list[i].write(device_name,arp_pack,offset=0x3000)
	
	#fpga_list[i].write_int('eth_ctrl',1);
	fpga_list[i].write_int('reg_arm',0);
	fpga_list[i].write_int('eth1_ctrl',1);
	time.sleep(0.1)
	#fpga_list[i].write_int('eth_ctrl',0);
	fpga_list[i].write_int('eth1_ctrl',0);
	time.sleep(0.1)
	#fpga_list[i].write_int('eth_ctrl',2);
	fpga_list[i].write_int('eth1_ctrl',2);
	#fpga_list[i].write_int('force_sync',2);
	time.sleep(0.1)
	#fpga_list[i].write_int('force_sync',0);


now = datetime.datetime.now()
micr = now.microsecond
delt = datetime.timedelta(seconds=3,microseconds=1000000-micr)
print 'Pausing until',now+delt
#delt2 = datetime.timedelta(hours=7,seconds=1)
#myt = (now+delt+delt2).isoformat()
#t = Time(myt,format='isot',scale='utc')

pause.until(now+delt)

for i in range(nfpga_start,nfpga_stop):
	fpga_list[i].write_int('reg_arm',1);


	
for i in range(nfpga_start,nfpga_stop):
	# set reset and enable for 10g
	#fpga_list[i].write_int('force_sync',1);
	#time.sleep(0.1)
	#fpga_list[i].write_int('force_sync',0);
	#fpga.write_int('eth_ctrl',1);
	fpga_list[i].write_int('eth1_ctrl',1);
	time.sleep(0.01)
	#fpga.write_int('eth_ctrl',0);
	fpga_list[i].write_int('eth1_ctrl',0);
	time.sleep(0.01)
	#fpga.write_int('eth_ctrl',2);
	fpga_list[i].write_int('eth1_ctrl',2);
	time.sleep(0.01)

