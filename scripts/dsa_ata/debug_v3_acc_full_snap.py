#!/usr/bin/env python

import casperfpga, struct, time
import matplotlib.pyplot as plt
import numpy as np
import sys

fpganame = sys.argv[1]

fpga = casperfpga.CasperFpga(fpganame,timeout = 20)

acc_snap1 = struct.unpack('>512Q',fpga.read('acc_full1',512*8))
acc_snap2 = struct.unpack('>512Q',fpga.read('acc_full2',512*8))
acc_snap3 = struct.unpack('>512Q',fpga.read('acc_full3',512*8))
acc_snap4 = struct.unpack('>512Q',fpga.read('acc_full4',512*8))

j=0
acc_snap = np.zeros((2048))
for i in range(0,512):
	acc_snap[j] = acc_snap1[i]
	j=j+1
	acc_snap[j] = acc_snap2[i]
	j=j+1
	acc_snap[j] = acc_snap3[i] 
	j=j+1
	acc_snap[j] = acc_snap4[i] 
	j=j+1


#acc_snap = np.concatenate([acc_snap1, acc_snap2, acc_snap3, acc_snap4])

plt.figure()
plt.semilogy(acc_snap)
#plt.plot(acc_snap)
plt.show()
