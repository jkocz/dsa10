#!/usr/bin/env python

import casperfpga, struct, time
import matplotlib.pyplot as plt
import numpy as np
import sys

def swap16(x):
	return (((x >> 8) & 0x00FF) | ((x << 8) & 0xFF00))


fpganame = sys.argv[1]

fpga = casperfpga.CasperFpga(fpganame, timeout = 20)

acc_snap = struct.unpack('>2048H',fpga.read('acc_16',2048*2))

#acc1 = acc_snap[0::4]
#acc2 = acc_snap[1::4]
#acc3 = acc_snap[2::4]
#acc4 = acc_snap[3::4]

#acc1a = np.zeros((512))
#acc2a = np.zeros((512))
#acc3a = np.zeros((512))
#acc4a = np.zeros((512))
#
#for i in range(0,512):
#	acc1a[i] = swap16(acc1[i])
#	acc2a[i] = swap16(acc2[i])
#	acc3a[i] = swap16(acc3[i])
#	acc4a[i] = swap16(acc4[i])
#
#acc_final = np.concatenate([acc1a, acc2a, acc3a, acc4a])
#acc_final = np.concatenate([acc1, acc2, acc3, acc4])

plt.figure()
plt.semilogy(acc_snap)
plt.show()
